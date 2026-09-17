import asyncio
import sys
import uuid

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from backend.graph.pipeline import contentmaker_pipeline
from backend.graph.state import ContentMakerState

async def test_full_cyclic_pipeline():
    print("=" * 80)
    print("CONTENTMAKER: TESTING DECOUPLED TRI-AGENT MULTI-AGENT WORKFLOW")
    print("Writer ➔ Auditor ➔ Script Doctor ➔ Packaging ➔ B-Roll & Repurposing ➔ Clearance")
    print("=" * 80)

    job_id = f"job_test_{uuid.uuid4().hex[:8]}"
    topic = "Building Cyclic Multi-Agent Systems with LangGraph"

    initial_state: ContentMakerState = {
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

    print(f"\n[1] Starting ContentMaker LangGraph invocation for Job: {job_id} | Topic: '{topic}'\n")

    # Run the decoupled pipeline
    final_state = await contentmaker_pipeline.ainvoke(initial_state)

    print("\n" + "=" * 80)
    print("EXECUTION SUMMARY & METRICS")
    print("=" * 80)
    print(f"Final Status: {final_state['status'].upper()}")
    print(f"Total Script Drafts Generated: {len(final_state['script_drafts'])}")
    print(f"Total Auditor Evaluations Logged: {len(final_state['critic_evaluations'])}")
    print(f"Total Doctor Interventions: {len(final_state.get('doctor_prescriptions', []))}")
    print(f"Total Revisions Triggered: {final_state['revision_count']}")

    print("\n--- VERSION HISTORY & SCRIPT DOCTOR TRACE ---")
    for i, script in enumerate(final_state['script_drafts'], 1):
        print(f"\n[Draft v{script.version}] Hook Dialogue:")
        print(f"\"{script.hook_segment.spoken_dialogue}\"")
        print(f"Visual Cue: \"{script.hook_segment.visual_cues}\"")
        if script.revision_notes:
            print(f"Revision Notes: {script.revision_notes}")

    if final_state.get("doctor_prescriptions"):
        print("\n--- SCRIPT DOCTOR EDITORIAL PRESCRIPTIONS (Zero Self-Evaluation Bias) ---")
        for p in final_state["doctor_prescriptions"]:
            print(f"Prescription for Draft v{p.target_draft_version} -> v{p.new_draft_version}:")
            print(f"  Summary: {p.addressed_critique_summary}")
            print(f"  Hook Notes: {p.hook_refactor_notes}")
            print(f"  Interventions: {p.pacing_interventions}")

    print("\n--- AUDITOR EVALUATION LOGS ---")
    for i, ev in enumerate(final_state['critic_evaluations'], 1):
        print(f"\nEvaluation #{i} (Target: {ev.target_agent.upper()}):")
        print(f"  Decision: {ev.decision}")
        print(f"  Overall Score: {ev.overall_score}/5.0")
        print(f"  Hook Strength Score: {ev.rubric.hook_strength.score}/5")
        print(f"  Summary: {ev.summary_feedback}")

    print("\n--- FINAL DELIVERABLES ---")
    meta = final_state['current_metadata']
    thumbs = final_state['current_thumbnails']
    broll = final_state['broll_shot_list']
    repurposed = final_state['repurposed_content']

    print(f"Primary Title: {meta.primary_title}")
    print(f"Chapters Count: {len(meta.chapters)}")
    print(f"Thumbnail Concepts: {len(thumbs.concepts)} concepts (Recommended: #{thumbs.recommended_concept_id})")
    if broll:
        print(f"AI B-Roll Shots: {broll.total_shots} shots with Midjourney/Runway prompts generated")
    if repurposed:
        print(f"Shorts Script: {repurposed.short_form.platform} ({repurposed.short_form.estimated_duration})")
        print(f"X Thread: {len(repurposed.twitter_thread)} posts generated")

    # Verification assertions
    assert final_state["status"] == "approved"
    assert len(final_state["script_drafts"]) >= 2, "Must demonstrate cyclic revision loop with at least 2 drafts!"
    assert len(final_state["critic_evaluations"]) >= 2, "Must have recorded auditor evaluations"
    assert len(final_state["doctor_prescriptions"]) >= 1, "Script Doctor must intervene on rejected drafts"
    assert final_state["broll_shot_list"] is not None, "B-Roll Shot List must be generated"
    assert (
        final_state["script_drafts"][1].hook_segment.spoken_dialogue != final_state["script_drafts"][0].hook_segment.spoken_dialogue
        or final_state["script_drafts"][1].full_text_markdown != final_state["script_drafts"][0].full_text_markdown
    ), "Draft 2 must contain concrete refactored content from Script Doctor"

    print("\n" + "=" * 80)
    print("SUCCESS: CONTENTMAKER DECOUPLED PIPELINE FULLY VALIDATED WITH ZERO SELF-EVAL REDUNDANCY!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_full_cyclic_pipeline())
