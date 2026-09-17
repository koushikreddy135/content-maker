import logging
from typing import Optional
from backend.models.schemas import ResearchBrief, ScriptDraft, ThumbnailPackage, ThumbnailConcept, CriticEvaluation
from backend.services.llm import LLMService

logger = logging.getLogger(__name__)

THUMBNAIL_SYSTEM_PROMPT = """You are a master YouTube Creative Director and Thumbnail Packaging Specialist.
Your mission is to formulate 2-3 high-CTR, scroll-stopping thumbnail concepts for a YouTube video.

THUMBNAIL DESIGN PHILOSOPHY:
1. RULE OF THIRDS & MOBILE CLARITY:
   - Must be instantly readable and striking on a 2-inch phone screen.
   - Text overlay MUST be 2 to 4 words max. NEVER repeat the title verbatim.
2. VISUAL CONTRAST & COLOR PALETTES:
   - Specify bold, high-contrast palettes (e.g. Neon Yellow on Obsidian, Cyberpunk Cyan on Deep Navy).
3. EMOTIONAL TRIGGER:
   - Provide concrete facial expressions, 3D object focal points, or before/after visual tension.
   - Clear synergy with the video thesis without deceptive clickbait.

Return ONLY a structured JSON object matching the ThumbnailPackage schema."""

class ThumbnailAgent:
    async def run(
        self,
        brief: ResearchBrief,
        script: ScriptDraft,
        previous_package: Optional[ThumbnailPackage] = None,
        critic_evaluation: Optional[CriticEvaluation] = None
    ) -> ThumbnailPackage:
        """
        Generates or revises 2-3 structured thumbnail concepts.
        """
        current_version = (previous_package.version + 1) if previous_package else 1
        logger.info(f"ThumbnailAgent generating Thumbnail Package v{current_version} for '{brief.topic}'")

        prompt_parts = [
            f"TOPIC: {brief.topic}",
            f"CORE THESIS: {brief.core_thesis}",
            f"DIFFERENTIATION ANGLE: {brief.competitive_angle.differentiation_hook}",
            f"HOOK SUMMARY: \"{script.hook_segment.spoken_dialogue[:150]}\"",
            f"HOOK VISUAL CUE: \"{script.hook_segment.visual_cues}\""
        ]

        if previous_package and critic_evaluation:
            prompt_parts.extend([
                f"\n=== PREVIOUS THUMBNAIL CRITIQUE (v{previous_package.version}) ===",
                f"Critic Decision: {critic_evaluation.decision}",
                f"Summary Feedback: {critic_evaluation.summary_feedback}",
                "\nMANDATORY REVISION DIRECTIVES:",
                "\n".join([f"  * {d}" for d in critic_evaluation.specific_directives])
            ])

        prompt = "\n".join(prompt_parts)

        pkg = await LLMService.generate_structured(
            prompt=prompt,
            system_prompt=THUMBNAIL_SYSTEM_PROMPT,
            response_model=ThumbnailPackage,
            temperature=0.7
        )

        pkg.version = current_version
        logger.info(f"ThumbnailAgent generated {len(pkg.concepts)} thumbnail concepts. Recommended: #{pkg.recommended_concept_id}")
        return pkg
