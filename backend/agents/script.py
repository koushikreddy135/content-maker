import logging
from typing import Optional, List
from backend.models.schemas import ResearchBrief, ScriptDraft, ScriptSection, CriticEvaluation
from backend.services.llm import LLMService

logger = logging.getLogger(__name__)

SCRIPT_SYSTEM_PROMPT = """You are a world-class YouTube Head of Scriptwriting for high-retention video essays and technical breakdowns.
Your mission is to transform a structured ResearchBrief into a full, production-ready video script with embedded visual/B-roll directions.

CRITICAL YOUTUBE RETENTION RULES:
1. THE FIRST 15 SECONDS (COLD OPEN):
   - ABSOLUTELY NO throat-clearing intro (e.g. NEVER say "Hey guys welcome back", "Today we're talking about...", "In this video...").
   - Open immediately with a high-stakes contrast, an unexpected counterintuitive statistic, or an urgent problem.
   - Plant a curiosity gap or clear promise of value within the first 10 seconds.
2. BODY PACING:
   - Provide concrete spoken dialogue for each section.
   - For every spoken segment, provide explicit VISUAL CUES (camera switches, on-screen graphics, animated diagrams, split screens, B-roll).
3. RETENTION RESETS:
   - Inject mini-hooks and visual resets every 90-120 seconds to prevent viewer drop-off.
4. OUTRO & CTA:
   - Make the CTA fast and organic (last 30 seconds), linked directly to resources or next steps.

IF REVISION DIRECTIVES ARE PROVIDED:
- You MUST directly address every single critique from the Critic Agent.
- If the critic flagged a weak hook, rewrite the cold open completely.
- Document in `revision_notes` exactly how you resolved the critique.

Return ONLY a structured JSON object matching the ScriptDraft schema."""

class ScriptAgent:
    async def run(
        self,
        brief: ResearchBrief,
        duration_target: str = "8-10 mins",
        tone: str = "authoritative, dynamic, and educational",
        previous_draft: Optional[ScriptDraft] = None,
        critic_evaluation: Optional[CriticEvaluation] = None
    ) -> ScriptDraft:
        """
        Generates or revises a video script from a ResearchBrief.
        """
        current_version = (previous_draft.version + 1) if previous_draft else 1
        logger.info(f"ScriptAgent generating Script Draft v{current_version} for '{brief.topic}'")

        # Build prompt
        prompt_parts = [
            f"TOPIC: {brief.topic}",
            f"TARGET AUDIENCE: {brief.target_audience}",
            f"CORE THESIS: {brief.core_thesis}",
            f"TARGET DURATION: {duration_target}",
            f"TONE: {tone}",
            "\nKEY POINTS TO COVER:",
            "\n".join([f"- {kp}" for kp in brief.key_points]),
            "\nDIFFERENTIATION HOOK ANGLE:",
            f"- {brief.competitive_angle.differentiation_hook}",
            "\nTARGET KEYWORDS TO WEAVE NATURALLY:",
            f"- {', '.join(brief.target_keywords)}"
        ]

        if previous_draft and critic_evaluation:
            prompt_parts.extend([
                f"\n=== PREVIOUS DRAFT CRITIQUE (v{previous_draft.version}) ===",
                f"Critic Decision: {critic_evaluation.decision}",
                f"Critic Overall Score: {critic_evaluation.overall_score}/5.0",
                f"Summary Feedback: {critic_evaluation.summary_feedback}",
                "\nCRITICAL MANDATORY REVISION DIRECTIVES:",
                "\n".join([f"  * {d}" for d in critic_evaluation.specific_directives]),
                f"\nPrevious Hook Dialogue:\n\"{previous_draft.hook_segment.spoken_dialogue}\""
            ])

        prompt = "\n".join(prompt_parts)

        script_draft = await LLMService.generate_structured(
            prompt=prompt,
            system_prompt=SCRIPT_SYSTEM_PROMPT,
            response_model=ScriptDraft,
            temperature=0.6
        )

        script_draft.version = current_version
        script_draft.duration_target = duration_target
        script_draft.tone = tone

        # Assemble full markdown teleprompter script if not assembled
        if not script_draft.full_text_markdown or len(script_draft.full_text_markdown) < 50:
            md_lines = [
                f"# YouTube Script: {brief.topic}",
                f"**Target Duration:** {duration_target} | **Version:** {current_version} | **Tone:** {tone}\n",
                f"## 🎬 {script_draft.hook_segment.section_title} ({script_draft.hook_segment.timestamp_estimate})",
                f"**Visual:** _{script_draft.hook_segment.visual_cues}_",
                f"{script_draft.hook_segment.spoken_dialogue}\n"
            ]
            for sec in script_draft.body_sections:
                md_lines.extend([
                    f"## 📌 {sec.section_title} ({sec.timestamp_estimate})",
                    f"**Visual:** _{sec.visual_cues}_",
                    f"{sec.spoken_dialogue}\n"
                ])
            md_lines.extend([
                f"## 🎯 {script_draft.cta_section.section_title} ({script_draft.cta_section.timestamp_estimate})",
                f"**Visual:** _{script_draft.cta_section.visual_cues}_",
                f"{script_draft.cta_section.spoken_dialogue}\n"
            ])
            script_draft.full_text_markdown = "\n".join(md_lines)

        logger.info(f"ScriptAgent successfully produced Script Draft v{current_version} with {len(script_draft.body_sections)} body sections.")
        return script_draft
