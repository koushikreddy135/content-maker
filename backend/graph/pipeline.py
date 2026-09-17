import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Callable, Optional
from langgraph.graph import StateGraph, END

from backend.config import settings
from backend.graph.state import ContentMakerState, ContentForgeState
from backend.agents.research import ResearchAgent
from backend.agents.script import ScriptAgent
from backend.agents.script_doctor import ScriptDoctorAgent
from backend.agents.metadata import SEOAgent
from backend.agents.thumbnail import ThumbnailAgent
from backend.agents.critic import AuditorCriticAgent, PackagingAuditorAgent, CriticAgent
from backend.agents.repurpose import RepurposeAndBRollAgent
from backend.models.schemas import CompleteVideoPackage

logger = logging.getLogger(__name__)

# Initialize singletons for agents
research_agent = ResearchAgent()
script_writer_agent = ScriptAgent()
script_doctor_agent = ScriptDoctorAgent()
auditor_agent = AuditorCriticAgent()
seo_agent = SEOAgent()
thumbnail_agent = ThumbnailAgent()
packaging_auditor_agent = PackagingAuditorAgent()
repurpose_agent = RepurposeAndBRollAgent()

# Unified agent for backward-compatible calls
critic_agent = CriticAgent()

# Broadcast callback for live SSE / UI streaming
_event_listeners = []

def register_listener(cb: Callable[[Dict[str, Any]], None]):
    _event_listeners.append(cb)

def emit_event(event_type: str, data: Dict[str, Any]):
    payload = {
        "event": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data
    }
    for cb in _event_listeners:
        try:
            cb(payload)
        except Exception as e:
            logger.error(f"Event broadcast failed: {e}")


# === GRAPH NODES ===

async def research_node(state: ContentMakerState) -> Dict[str, Any]:
    logger.info(f"--- [Node 1: Research] Starting for topic '{state['topic']}' ---")
    emit_event("node_start", {"node": "research", "job_id": state["job_id"], "topic": state["topic"]})
    
    brief = await research_agent.run(state["topic"])
    
    log_entry = {
        "step": "research",
        "message": f"Generated Research Brief with {len(brief.key_points)} core points and competitor angle.",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    emit_event("node_finish", {"node": "research", "job_id": state["job_id"], "brief": brief.model_dump()})
    return {
        "research_brief": brief,
        "current_step": "research_complete",
        "step_logs": state.get("step_logs", []) + [log_entry]
    }


async def script_writer_node(state: ContentMakerState) -> Dict[str, Any]:
    """
    Initial Script Drafter. Operates cleanly from the research brief
    without being forced to self-evaluate previous drafts.
    """
    logger.info(f"--- [Node 2: Script Writer] Generating Initial Draft v1 for '{state['topic']}' ---")
    emit_event("node_start", {
        "node": "script",
        "job_id": state["job_id"],
        "revision_count": 0,
        "agent": "ScriptWriterAgent"
    })

    script = await script_writer_agent.run(
        brief=state["research_brief"],
        duration_target=state.get("duration_target", "8-10 mins"),
        tone=state.get("tone", "authoritative, dynamic")
    )

    drafts = list(state.get("script_drafts", []))
    drafts.append(script)

    log_entry = {
        "step": "script",
        "message": f"ScriptWriterAgent produced Draft v{script.version} ({script.hook_segment.section_title})",
        "version": script.version,
        "timestamp": datetime.utcnow().isoformat()
    }

    emit_event("node_finish", {
        "node": "script",
        "job_id": state["job_id"],
        "version": script.version,
        "script": script.model_dump()
    })

    return {
        "script_drafts": drafts,
        "current_script": script,
        "current_step": f"script_v{script.version}_ready",
        "step_logs": state.get("step_logs", []) + [log_entry]
    }


async def auditor_critic_node(state: ContentMakerState) -> Dict[str, Any]:
    """
    Independent Adversarial Quality Auditor.
    Assesses hook retention and narrative pacing without editing authority.
    """
    rev_count = state.get("revision_count", 0)
    current_script = state["current_script"]
    brief = state["research_brief"]
    
    logger.info(f"--- [Node 3: Auditor Critic] Evaluating Script v{current_script.version} (Iter #{rev_count + 1}) ---")
    emit_event("node_start", {
        "node": "critic_script",
        "job_id": state["job_id"],
        "iteration": rev_count + 1,
        "evaluating_version": current_script.version
    })

    evaluation = await auditor_agent.evaluate_script(
        brief=brief,
        script=current_script,
        iteration=rev_count + 1
    )

    evals = list(state.get("critic_evaluations", []))
    evals.append(evaluation)

    new_rev_count = rev_count + 1 if evaluation.decision == "REVISE_SCRIPT" else rev_count

    log_entry = {
        "step": "critic_script",
        "decision": evaluation.decision,
        "score": evaluation.overall_score,
        "summary": evaluation.summary_feedback,
        "timestamp": datetime.utcnow().isoformat()
    }

    emit_event("node_finish", {
        "node": "critic_script",
        "job_id": state["job_id"],
        "evaluation": evaluation.model_dump(),
        "decision": evaluation.decision
    })

    return {
        "critic_evaluations": evals,
        "latest_critic_eval": evaluation,
        "revision_count": new_rev_count,
        "current_step": f"critic_script_{evaluation.decision.lower()}",
        "step_logs": state.get("step_logs", []) + [log_entry]
    }


def router_after_auditor(state: ContentMakerState) -> str:
    decision = state["latest_critic_eval"].decision
    logger.info(f"Router after Script Auditor: Decision = {decision}")
    
    if decision == "APPROVED":
        return "metadata_and_thumbnails"
    elif decision == "REVISE_SCRIPT":
        # DECOUPLED ARCHITECTURE: Route to ScriptDoctorAgent (NOT back to writer!)
        return "script_doctor"
    elif decision == "ESCALATE_HUMAN":
        return "escalate"
    return "script_doctor"


async def script_doctor_node(state: ContentMakerState) -> Dict[str, Any]:
    """
    Dedicated Script Doctor Refiner. Intervenes when Auditor rejects draft.
    Performs surgical cold-open punch-up, pattern interrupt insertion,
    and pacing refactoring without author anchoring bias.
    """
    rev_count = state.get("revision_count", 1)
    current_script = state["current_script"]
    brief = state["research_brief"]
    latest_eval = state["latest_critic_eval"]

    logger.info(f"--- [Node 3b: Script Doctor] Intervening on Draft v{current_script.version} (Iter #{rev_count}) ---")
    emit_event("node_start", {
        "node": "script_doctor",
        "job_id": state["job_id"],
        "intervening_version": current_script.version
    })

    prescription = await script_doctor_agent.prescribe_and_refactor(
        brief=brief,
        current_script=current_script,
        auditor_evaluation=latest_eval,
        iteration=rev_count
    )

    prescriptions = list(state.get("doctor_prescriptions", []))
    prescriptions.append(prescription)

    drafts = list(state.get("script_drafts", []))
    drafts.append(prescription.revised_script)

    log_entry = {
        "step": "script_doctor",
        "message": f"ScriptDoctorAgent refactored Draft v{prescription.revised_script.version}. Notes: {prescription.addressed_critique_summary[:120]}...",
        "version": prescription.revised_script.version,
        "timestamp": datetime.utcnow().isoformat()
    }

    emit_event("node_finish", {
        "node": "script_doctor",
        "job_id": state["job_id"],
        "prescription": prescription.model_dump(),
        "revised_script": prescription.revised_script.model_dump()
    })

    return {
        "script_drafts": drafts,
        "current_script": prescription.revised_script,
        "doctor_prescriptions": prescriptions,
        "current_step": f"script_v{prescription.revised_script.version}_doctor_refactored",
        "step_logs": state.get("step_logs", []) + [log_entry]
    }


async def metadata_and_thumbnails_node(state: ContentMakerState) -> Dict[str, Any]:
    logger.info("--- [Node 4: SEO Metadata & Thumbnail Concepts (Parallel)] ---")
    emit_event("node_start", {"node": "metadata_and_thumbnails", "job_id": state["job_id"]})

    brief = state["research_brief"]
    script = state["current_script"]

    # Concurrently execute SEO and Thumbnail generation
    metadata_task = seo_agent.run(brief, script)
    thumbnail_task = thumbnail_agent.run(brief, script)

    metadata, thumbnails = await asyncio.gather(metadata_task, thumbnail_task)

    meta_drafts = list(state.get("metadata_drafts", [])) + [metadata]
    thumb_drafts = list(state.get("thumbnail_drafts", [])) + [thumbnails]

    log_entry = {
        "step": "metadata_and_thumbnails",
        "message": f"Generated SEO metadata ('{metadata.primary_title}') and {len(thumbnails.concepts)} high-CTR thumbnail concepts.",
        "timestamp": datetime.utcnow().isoformat()
    }

    emit_event("node_finish", {
        "node": "metadata_and_thumbnails",
        "job_id": state["job_id"],
        "metadata": metadata.model_dump(),
        "thumbnails": thumbnails.model_dump()
    })

    return {
        "metadata_drafts": meta_drafts,
        "current_metadata": metadata,
        "thumbnail_drafts": thumb_drafts,
        "current_thumbnails": thumbnails,
        "current_step": "metadata_and_thumbnails_ready",
        "step_logs": state.get("step_logs", []) + [log_entry]
    }


async def packaging_auditor_node(state: ContentMakerState) -> Dict[str, Any]:
    """
    Dedicated Packaging Auditor evaluating SEO and Thumbnail visual synergy.
    """
    rev_count = state.get("revision_count", 0)
    logger.info(f"--- [Node 5: Packaging Auditor] Iteration #{rev_count + 1} ---")
    emit_event("node_start", {"node": "critic_package", "job_id": state["job_id"]})

    evaluation = await packaging_auditor_agent.evaluate_package(
        brief=state["research_brief"],
        script=state["current_script"],
        metadata=state["current_metadata"],
        thumbnails=state["current_thumbnails"],
        iteration=rev_count + 1
    )

    evals = list(state.get("critic_evaluations", []))
    evals.append(evaluation)

    log_entry = {
        "step": "critic_package",
        "decision": evaluation.decision,
        "score": evaluation.overall_score,
        "summary": evaluation.summary_feedback,
        "timestamp": datetime.utcnow().isoformat()
    }

    emit_event("node_finish", {
        "node": "critic_package",
        "job_id": state["job_id"],
        "evaluation": evaluation.model_dump(),
        "decision": evaluation.decision
    })

    return {
        "critic_evaluations": evals,
        "latest_critic_eval": evaluation,
        "current_step": f"critic_package_{evaluation.decision.lower()}",
        "step_logs": state.get("step_logs", []) + [log_entry]
    }


def router_after_packaging_auditor(state: ContentMakerState) -> str:
    decision = state["latest_critic_eval"].decision
    logger.info(f"Router after Packaging Auditor: Decision = {decision}")
    
    if decision == "APPROVED":
        return "repurpose_and_broll"
    elif decision == "ESCALATE_HUMAN":
        return "escalate"
    elif decision == "REVISE_SCRIPT":
        return "script_doctor"
    elif decision in ["REVISE_METADATA", "REVISE_THUMBNAIL"]:
        return "metadata_and_thumbnails"
    return "repurpose_and_broll"


async def repurpose_and_broll_node(state: ContentMakerState) -> Dict[str, Any]:
    """
    Autonomous node generating B-Roll shot lists (with generative prompts)
    and multi-platform social repurposing (60s vertical Shorts + X thread).
    """
    logger.info("--- [Node 6: AI B-Roll Shot List & Multi-Platform Repurposing] ---")
    emit_event("node_start", {"node": "repurpose_and_broll", "job_id": state["job_id"]})

    brief = state["research_brief"]
    script = state["current_script"]
    metadata = state.get("current_metadata")

    broll_task = repurpose_agent.generate_broll_shot_list(brief, script)
    repurpose_task = repurpose_agent.generate_repurposed_content(brief, script, metadata)

    broll_shots, repurposed = await asyncio.gather(broll_task, repurpose_task)

    log_entry = {
        "step": "repurpose_and_broll",
        "message": f"Generated {broll_shots.total_shots} AI B-Roll shots, 60s vertical Shorts script, and 5-tweet X thread.",
        "timestamp": datetime.utcnow().isoformat()
    }

    emit_event("node_finish", {
        "node": "repurpose_and_broll",
        "job_id": state["job_id"],
        "broll_shots": broll_shots.model_dump(),
        "repurposed": repurposed.model_dump()
    })

    return {
        "broll_shot_list": broll_shots,
        "repurposed_content": repurposed,
        "current_step": "repurpose_and_broll_ready",
        "step_logs": state.get("step_logs", []) + [log_entry]
    }


async def approve_node(state: ContentMakerState) -> Dict[str, Any]:
    logger.info(f"--- [Terminal Node: APPROVE] ContentMaker video package for '{state['topic']}' passed all quality gates! ---")
    
    final_score = state["latest_critic_eval"].overall_score if state.get("latest_critic_eval") else 5.0
    
    log_entry = {
        "step": "approve",
        "message": f"Video package fully approved with quality score {final_score}/5.0 across all dimensions.",
        "timestamp": datetime.utcnow().isoformat()
    }

    emit_event("job_complete", {
        "job_id": state["job_id"],
        "status": "approved",
        "final_score": final_score
    })

    return {
        "status": "approved",
        "current_step": "completed",
        "step_logs": state.get("step_logs", []) + [log_entry]
    }


async def escalate_node(state: ContentMakerState) -> Dict[str, Any]:
    logger.warning("--- [Terminal Node: ESCALATE] Hit max revisions or unresolvable rubric violation ---")
    
    reason = (
        state["latest_critic_eval"].summary_feedback
        if state.get("latest_critic_eval")
        else "Exceeded maximum revision cycles without meeting score threshold."
    )

    log_entry = {
        "step": "escalate",
        "message": f"Escalated to human review. Reason: {reason}",
        "timestamp": datetime.utcnow().isoformat()
    }

    emit_event("job_complete", {
        "job_id": state["job_id"],
        "status": "escalated_to_human",
        "reason": reason
    })

    return {
        "status": "escalated_to_human",
        "escalation_reason": reason,
        "current_step": "escalated",
        "step_logs": state.get("step_logs", []) + [log_entry]
    }


# === BUILD AND COMPILE LANGGRAPH STATE GRAPH ===

def build_contentmaker_graph():
    """
    Constructs the decoupled cyclic multi-agent LangGraph workflow.
    Decouples Generator, Auditor, and Refiner to eliminate self-evaluation bias.
    """
    workflow = StateGraph(ContentMakerState)

    # Add Nodes
    workflow.add_node("research", research_node)
    workflow.add_node("script", script_writer_node)
    workflow.add_node("critic_script", auditor_critic_node)
    workflow.add_node("script_doctor", script_doctor_node)
    workflow.add_node("metadata_and_thumbnails", metadata_and_thumbnails_node)
    workflow.add_node("critic_package", packaging_auditor_node)
    workflow.add_node("repurpose_and_broll", repurpose_and_broll_node)
    workflow.add_node("approve", approve_node)
    workflow.add_node("escalate", escalate_node)

    # Set Entry Point
    workflow.set_entry_point("research")

    # Add Flow Edges
    workflow.add_edge("research", "script")
    workflow.add_edge("script", "critic_script")

    # Conditional Routing 1: Auditor -> Script Doctor (Revision) / Packaging / Escalate
    workflow.add_conditional_edges(
        "critic_script",
        router_after_auditor,
        {
            "script_doctor": "script_doctor",  # DECOUPLED REVISION
            "metadata_and_thumbnails": "metadata_and_thumbnails",
            "escalate": "escalate"
        }
    )

    # Script Doctor passes refactored draft back to Auditor for objective re-evaluation
    workflow.add_edge("script_doctor", "critic_script")

    # Packaging flow
    workflow.add_edge("metadata_and_thumbnails", "critic_package")

    # Conditional Routing 2: Packaging Auditor -> Repurpose / Revise / Escalate
    workflow.add_conditional_edges(
        "critic_package",
        router_after_packaging_auditor,
        {
            "repurpose_and_broll": "repurpose_and_broll",
            "metadata_and_thumbnails": "metadata_and_thumbnails",
            "script_doctor": "script_doctor",
            "escalate": "escalate"
        }
    )

    # Repurpose & B-Roll flows into Approve
    workflow.add_edge("repurpose_and_broll", "approve")

    # Terminal edges
    workflow.add_edge("approve", END)
    workflow.add_edge("escalate", END)

    return workflow.compile()

# Global compiled graph instance
contentmaker_pipeline = build_contentmaker_graph()

# Backward compatibility alias
contentforge_pipeline = contentmaker_pipeline
