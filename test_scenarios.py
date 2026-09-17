import asyncio
import sys
import uuid

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from backend.graph.pipeline import contentmaker_pipeline
from backend.graph.state import ContentMakerState
from backend.models.schemas import ScriptDraft, ScriptSection, ResearchBrief, CompetitorAngle

async def run_scenario_a():
    """
    Scenario A: Clean Pass — Single-iteration approval with high quality throughout.
    """
    print("\n" + "=" * 80)
    print("DEMO SCENARIO A: CLEAN PASS (Single-Iteration Approval)")
    print("=" * 80)

    job_id = f"scen_a_{uuid.uuid4().hex[:6]}"
    topic = "How to Optimize Next.js App Router for Sub-Second Load Times"
    
    state: ContentMakerState = {
        "job_id": job_id,
        "topic": topic,
        "duration_target": "8-10 mins",
        "tone": "authoritative, dynamic, and educational",
        "research_brief": None,
        "script_drafts": [],
        "current_script": None,
        "doctor_prescriptions": [],
        "metadata_drafts": [],
        "current_metadata": None,
        "thumbnail_drafts": [],
        "current_thumbnails": None,
        "critic_evaluations": [],
        "latest_critic_eval": None,
        "broll_shot_list": None,
        "repurposed_content": None,
        "revision_count": 0,
        "max_revisions": 3,
        "status": "in_progress",
        "current_step": "start",
        "step_logs": [],
        "escalation_reason": None
    }

    result = await contentmaker_pipeline.ainvoke(state)
    print(f" -> Scenario A Status: {result['status'].upper()}")
    print(f" -> Total Drafts: {len(result['script_drafts'])}")
    print(f" -> Critic Decision: {result['latest_critic_eval'].decision}")
    print(f" -> Overall Score: {result['latest_critic_eval'].overall_score}/5.0")
    assert result['status'] == "approved"
    print(" [OK] Scenario A successfully passed.")


async def run_scenario_b():
    """
    Scenario B: Core Differentiator — Draft 1 rejected due to weak hook,
    Script Doctor auto-revises into Draft 2 (zero self-eval bias),
    Auditor approves with score jump.
    """
    print("\n" + "=" * 80)
    print("DEMO SCENARIO B: SCRIPT DOCTOR REVISION (Draft 1 Rejected -> Script Doctor -> Draft 2 Approved)")
    print("=" * 80)

    job_id = f"scen_b_{uuid.uuid4().hex[:6]}"
    topic = "Building Cyclic Multi-Agent Systems with LangGraph"

    state: ContentMakerState = {
        "job_id": job_id,
        "topic": topic,
        "duration_target": "8-10 mins",
        "tone": "authoritative, dynamic, and educational",
        "research_brief": None,
        "script_drafts": [],
        "current_script": None,
        "doctor_prescriptions": [],
        "metadata_drafts": [],
        "current_metadata": None,
        "thumbnail_drafts": [],
        "current_thumbnails": None,
        "critic_evaluations": [],
        "latest_critic_eval": None,
        "broll_shot_list": None,
        "repurposed_content": None,
        "revision_count": 0,
        "max_revisions": 3,
        "status": "in_progress",
        "current_step": "start",
        "step_logs": [],
        "escalation_reason": None
    }

    result = await contentmaker_pipeline.ainvoke(state)
    print(f" -> Scenario B Status: {result['status'].upper()}")
    print(f" -> Total Script Drafts: {len(result['script_drafts'])}")
    print(f" -> Total Doctor Prescriptions: {len(result['doctor_prescriptions'])}")
    print(f" -> Total Revisions: {result['revision_count']}")
    print(f" -> Draft 1 Hook: \"{result['script_drafts'][0].hook_segment.spoken_dialogue[:70]}...\"")
    print(f" -> Draft 2 Hook: \"{result['script_drafts'][1].hook_segment.spoken_dialogue[:70]}...\"")
    print(f" -> Draft 1 Auditor Score: {result['critic_evaluations'][0].rubric.hook_strength.score}/5 (Decision: {result['critic_evaluations'][0].decision})")
    print(f" -> Draft 2 Auditor Score: {result['critic_evaluations'][1].rubric.hook_strength.score}/5 (Decision: {result['critic_evaluations'][1].decision})")
    assert result['status'] == "approved"
    assert len(result['doctor_prescriptions']) >= 1, "Script Doctor must intervene on Scenario B"
    print(" [OK] Scenario B successfully demonstrated decoupled script doctor revision!")


async def run_scenario_c():
    """
    Scenario C: Adversarial / Hard-Cap Escalation — Exceeds max revisions (3 loops)
    and gracefully escalates to human review with diagnostic reasons.
    """
    print("\n" + "=" * 80)
    print("DEMO SCENARIO C: MAX REVISION CAP & HUMAN ESCALATION")
    print("=" * 80)

    from backend.agents.critic import AuditorCriticAgent
    strict_auditor = AuditorCriticAgent(min_overall_score=4.5, min_individual_score=4.0, max_revisions=3)
    
    brief = ResearchBrief(
        topic="Cryptocurrency Guaranteed 100x Pump Scheme",
        target_audience="Speculative retail investors",
        core_thesis="Guaranteed wealth generation in 24 hours",
        key_points=["Deposit funds immediately", "No risk guarantee"],
        hook_angles=["Get rich tonight with this secret bot"],
        competitive_angle=CompetitorAngle(existing_coverage="Scams", differentiation_hook="Higher yield claim"),
        target_keywords=["crypto pump", "get rich quick"],
        sources_cited=[]
    )

    failing_draft = ScriptDraft(
        version=3,
        duration_target="5 mins",
        tone="hype",
        hook_segment=ScriptSection(
            section_title="Intro",
            timestamp_estimate="0:00 - 0:15",
            spoken_dialogue="Hey guys, deposit money into this link right now for guaranteed 100x returns.",
            visual_cues="Static stock chart."
        ),
        body_sections=[
            ScriptSection(
                section_title="Body",
                timestamp_estimate="0:15 - 2:00",
                spoken_dialogue="This system never loses money.",
                visual_cues="No visual cue."
            )
        ],
        cta_section=ScriptSection(
            section_title="CTA",
            timestamp_estimate="2:00 - 2:30",
            spoken_dialogue="Click link below now.",
            visual_cues="URL"
        ),
        full_text_markdown="# Failing Script"
    )

    eval_result = await strict_auditor.evaluate_script(brief, failing_draft, iteration=3)
    print(f" -> Iteration: {eval_result.iteration} / Max 3")
    print(f" -> Auditor Decision: {eval_result.decision}")
    print(f" -> Overall Score: {eval_result.overall_score}/5.0")
    print(f" -> Escalation Reason: {eval_result.summary_feedback}")

    assert eval_result.decision == "ESCALATE_HUMAN", "Must gracefully escalate on hitting revision cap"
    print(" [OK] Scenario C successfully verified human escalation safety gate!")


async def main():
    await run_scenario_a()
    await run_scenario_b()
    await run_scenario_c()
    print("\n" + "=" * 80)
    print("ALL 3 DEMO SCENARIOS VERIFIED SUCCESSFULLY ON CONTENTMAKER!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
