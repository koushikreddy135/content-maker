import logging
from typing import Optional
from backend.models.schemas import ResearchBrief, ScriptDraft, SEOMetadata, ChapterMarker, CriticEvaluation
from backend.services.llm import LLMService

logger = logging.getLogger(__name__)

SEO_SYSTEM_PROMPT = """You are a top-tier YouTube Algorithm & SEO Optimization Specialist.
Your mission is to generate YouTube metadata (titles, descriptions, tags, chapters) that maximize click-through rate (CTR), search discovery, and viewer retention.

OPTIMIZATION PRINCIPLES:
1. TITLES:
   - Primary title must balance high search volume with emotional curiosity (under 60 characters for mobile display).
   - Provide 2-3 alternative title angles (e.g. Question format, High-Stakes Intrigue, Authority/Case Study).
2. DESCRIPTION:
   - First 2 lines must contain high-intent keywords and a compelling value hook before the "Show More" fold.
   - Include accurate, formatted chapter timestamps (00:00 format) reflecting the script's actual sections.
3. TAGS & HASHTAGS:
   - 10-15 targeted tags covering broad topic, specific terminology, and common search phrases.
   - 3-5 high-relevance hashtags.

If revision directives are provided, refine the metadata accordingly and record `revision_notes`.

Return ONLY a structured JSON object matching the SEOMetadata schema."""

class SEOAgent:
    async def run(
        self,
        brief: ResearchBrief,
        script: ScriptDraft,
        previous_metadata: Optional[SEOMetadata] = None,
        critic_evaluation: Optional[CriticEvaluation] = None
    ) -> SEOMetadata:
        """
        Generates or revises YouTube SEO metadata from brief and script.
        """
        current_version = (previous_metadata.version + 1) if previous_metadata else 1
        logger.info(f"SEOAgent generating SEO Metadata v{current_version} for '{brief.topic}'")

        script_summary_points = [f"- {s.section_title} ({s.timestamp_estimate})" for s in script.body_sections]
        
        prompt_parts = [
            f"TOPIC: {brief.topic}",
            f"TARGET AUDIENCE: {brief.target_audience}",
            f"CORE THESIS: {brief.core_thesis}",
            f"TARGET KEYWORDS: {', '.join(brief.target_keywords)}",
            f"SCRIPT HOOK: \"{script.hook_segment.spoken_dialogue[:150]}...\"",
            "\nSCRIPT CHAPTER BREAKDOWN:",
            f"- {script.hook_segment.section_title} ({script.hook_segment.timestamp_estimate})",
            "\n".join(script_summary_points),
            f"- {script.cta_section.section_title} ({script.cta_section.timestamp_estimate})"
        ]

        if previous_metadata and critic_evaluation:
            prompt_parts.extend([
                f"\n=== PREVIOUS METADATA CRITIQUE (v{previous_metadata.version}) ===",
                f"Critic Decision: {critic_evaluation.decision}",
                f"Summary Feedback: {critic_evaluation.summary_feedback}",
                "\nMANDATORY REVISION DIRECTIVES:",
                "\n".join([f"  * {d}" for d in critic_evaluation.specific_directives])
            ])

        prompt = "\n".join(prompt_parts)

        metadata = await LLMService.generate_structured(
            prompt=prompt,
            system_prompt=SEO_SYSTEM_PROMPT,
            response_model=SEOMetadata,
            temperature=0.5
        )

        metadata.version = current_version
        logger.info(f"SEOAgent generated title: '{metadata.primary_title}' and {len(metadata.tags)} tags.")
        return metadata
