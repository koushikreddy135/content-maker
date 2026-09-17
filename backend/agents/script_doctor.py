import logging
from typing import Optional, List
from backend.models.schemas import (
    ResearchBrief, ScriptDraft, ScriptSection,
    CriticEvaluation, ScriptDoctorPrescription
)
from backend.services.llm import LLMService

logger = logging.getLogger(__name__)

SCRIPT_DOCTOR_SYSTEM_PROMPT = """You are an elite Hollywood Script Doctor and Head of Retention Engineering for Tier-1 YouTube Creators (10M+ subscribers).
Your mission is to perform SURGICAL EDITORIAL REFACTORING on a deficient video script that was flagged by the Quality Auditor.

WHY YOU EXIST (THE DECOUPLED VERIFICATION PRINCIPLE):
The original Script Writer cannot objectively evaluate their own draft due to author anchoring bias.
You operate as an independent, objective master refiner. You consume the draft + the Auditor's diagnostic failure report and surgically rewrite the weak areas without altering verified core facts.

YOUR EDITORIAL RULES:
1. SURGICAL COLD OPEN RESTRUCTURING:
   - Completely erase all introductory pleasantries ("Hey guys", "Welcome back", "Today we are going to explore...").
   - Open in medias res: Drop the viewer immediately into a high-stakes contrast, an urgent mistake costing them time/money, or a shocking counterintuitive statistic within the first 3 seconds.
   - Establish a concrete "curiosity gap" or high-value promise within 10 seconds.
2. RETENTION RESETS & VISUAL DENSITY:
   - Inject rich visual cue annotations: DYNAMIC SPLIT SCREEN, MACRO CLOSE-UP, KINETIC ON-SCREEN GRAPHICS, CAMERA PULL-BACK.
   - Ensure a visual reset or pattern interrupt occurs every 60-90 seconds.
3. CONCRETE RESOLUTION:
   - Directly resolve every single item listed in the Auditor's `specific_directives`.
   - Explain your surgical intervention in `addressed_critique_summary` and `hook_refactor_notes`.

Return ONLY a valid JSON object matching the ScriptDoctorPrescription schema."""

class ScriptDoctorAgent:
    """
    Independent editorial refiner that eliminates self-evaluation redundancy
    by acting as a separate agent from both the Script Writer and the Auditor.
    """
    async def prescribe_and_refactor(
        self,
        brief: ResearchBrief,
        current_script: ScriptDraft,
        auditor_evaluation: CriticEvaluation,
        iteration: int = 1
    ) -> ScriptDoctorPrescription:
        logger.info(
            f"ScriptDoctorAgent intervening on Script Draft v{current_script.version} "
            f"(Auditor Score: {auditor_evaluation.overall_score}/5.0 | Iteration #{iteration})"
        )

        next_version = current_script.version + 1

        prompt = f"""SURGICAL INTERVENTION REQUIRED: REFACTOR SCRIPT DRAFT (v{current_script.version} -> v{next_version})
LOOP ITERATION: {iteration}

TOPIC: {brief.topic}
TARGET AUDIENCE: {brief.target_audience}
CORE THESIS: {brief.core_thesis}
TARGET KEYWORDS: {', '.join(brief.target_keywords)}

=== AUDITOR FAILURE DIAGNOSTIC ===
Auditor Overall Score: {auditor_evaluation.overall_score}/5.0
Auditor Summary Feedback: {auditor_evaluation.summary_feedback}
Hook Strength Score: {auditor_evaluation.rubric.hook_strength.score}/5.0 (Reason: {auditor_evaluation.rubric.hook_strength.justification})
Pacing Score: {auditor_evaluation.rubric.pacing_and_engagement.score}/5.0 (Reason: {auditor_evaluation.rubric.pacing_and_engagement.justification})

MANDATORY SURGICAL DIRECTIVES:
""" + "\n".join([f"- {d}" for d in auditor_evaluation.specific_directives]) + f"""

=== ORIGINAL DEFICIENT SCRIPT (v{current_script.version}) ===
HOOK ({current_script.hook_segment.timestamp_estimate}):
Dialogue: "{current_script.hook_segment.spoken_dialogue}"
Visual Cues: "{current_script.hook_segment.visual_cues}"

BODY SECTIONS:
""" + "\n".join([
            f"- [{s.section_title} | {s.timestamp_estimate}]\n  Dialogue: {s.spoken_dialogue}\n  Visual: {s.visual_cues}"
            for s in current_script.body_sections
        ]) + f"""

CTA ({current_script.cta_section.timestamp_estimate}):
Dialogue: "{current_script.cta_section.spoken_dialogue}"
Visual Cues: "{current_script.cta_section.visual_cues}"

Perform complete surgical restructuring. Generate a pristine ScriptDoctorPrescription with the refactored ScriptDraft (v{next_version})."""

        prescription = await LLMService.generate_structured(
            prompt=prompt,
            system_prompt=SCRIPT_DOCTOR_SYSTEM_PROMPT,
            response_model=ScriptDoctorPrescription,
            temperature=0.4
        )

        # Enforce version continuity and ensure full markdown formatting
        prescription.target_draft_version = current_script.version
        prescription.new_draft_version = next_version
        prescription.revised_script.version = next_version
        prescription.revised_script.duration_target = current_script.duration_target
        prescription.revised_script.tone = current_script.tone

        if not prescription.revised_script.cta_section:
            prescription.revised_script.cta_section = current_script.cta_section

        if not prescription.revised_script.full_text_markdown or len(prescription.revised_script.full_text_markdown) < 50:
            md_lines = [
                f"# YouTube Script: {brief.topic}",
                f"**Target Duration:** {current_script.duration_target} | **Version:** {next_version} (Doctor Refactored) | **Tone:** {current_script.tone}\n",
                f"## 🎬 {prescription.revised_script.hook_segment.section_title} ({prescription.revised_script.hook_segment.timestamp_estimate})",
                f"**Visual:** _{prescription.revised_script.hook_segment.visual_cues}_",
                f"{prescription.revised_script.hook_segment.spoken_dialogue}\n"
            ]
            for sec in prescription.revised_script.body_sections:
                md_lines.extend([
                    f"## 📌 {sec.section_title} ({sec.timestamp_estimate})",
                    f"**Visual:** _{sec.visual_cues}_",
                    f"{sec.spoken_dialogue}\n"
                ])
            md_lines.extend([
                f"## 🎯 {prescription.revised_script.cta_section.section_title} ({prescription.revised_script.cta_section.timestamp_estimate})",
                f"**Visual:** _{prescription.revised_script.cta_section.visual_cues}_",
                f"{prescription.revised_script.cta_section.spoken_dialogue}\n"
            ])
            prescription.revised_script.full_text_markdown = "\n".join(md_lines)

        logger.info(
            f"ScriptDoctorAgent successfully refactored Draft v{current_script.version} -> v{next_version}. "
            f"Addressed directives: {prescription.addressed_critique_summary[:100]}..."
        )
        return prescription
