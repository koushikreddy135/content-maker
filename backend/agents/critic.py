import logging
from typing import Optional, List
from backend.config import settings
from backend.models.schemas import (
    ResearchBrief, ScriptDraft, SEOMetadata, ThumbnailPackage,
    CriticEvaluation, CriticRubric, DimensionScore
)
from backend.services.llm import LLMService

logger = logging.getLogger(__name__)

CRITIC_SYSTEM_PROMPT = """You are a ruthless, expert Chief Content Officer and YouTube Algorithm Director.
Your mission is to perform an uncompromising, quality-gated evaluation of a YouTube video package.

EVALUATION RUBRIC (Score 1 to 5 for each dimension):
1. HOOK STRENGTH (First 5-15 seconds):
   - Score 1-2: Generic greeting ("Hey guys welcome back"), throat-clearing, no urgency or curiosity gap.
   - Score 3: Acceptable topic statement, but lacks high stakes or emotional tension.
   - Score 4-5: Stops the scroll instantly. High-stakes contrast, bold insight, or urgent problem within 3 seconds.
2. CLARITY & FLOW:
   - Score 1-2: Disjointed arguments, confusing jargon without explanation, abrupt transitions.
   - Score 3: Comprehensible but requires viewer mental effort to follow the progression.
   - Score 4-5: Crystal clear narrative arc. Complex concepts explained with effortless analogies.
3. PACING & ENGAGEMENT:
   - Score 1-2: Static talking head, monologue without visual resets or B-roll cues.
   - Score 3: Basic visual cues present, but pacing drags in middle sections.
   - Score 4-5: Rich visual cue density, animated diagrams, pattern interrupts every 90-120 seconds.
4. SEO KEYWORD ALIGNMENT:
   - Score 1-2: Target keywords ignored or clumsily stuffed.
   - Score 3: Keywords present but poorly distributed across title, chapters, and dialogue.
   - Score 4-5: Seamless, organic integration of primary and secondary search terms.
5. THUMBNAIL CLICK-WORTHINESS:
   - Score 1-2: Cluttered, low contrast, more than 5 words of text, duplicates title.
   - Score 3: Decent concept, but lacks punchy emotional trigger or mobile readability.
   - Score 4-5: Immediate visual contrast, 2-4 punchy words, powerful psychological trigger.
6. BRAND & TONE FIT:
   - Score 1-2: Overly salesy, dry academic, or hype without substance.
   - Score 3: Appropriate tone but slightly generic delivery.
   - Score 4-5: Highly authoritative, educational, dynamic, and trustworthy.

SCORING & DECISION RULES:
- An item PASSES only if overall_score >= 4.0 AND no individual dimension < 3.0.
- If evaluating script alone, return `APPROVED` (to proceed to metadata/thumbnail) or `REVISE_SCRIPT`.
- If evaluating the complete package, return `APPROVED`, `REVISE_SCRIPT`, `REVISE_METADATA`, or `REVISE_THUMBNAIL`.
- Provide concrete line citations in your justifications and surgical bullet points in `specific_directives`.

Return ONLY a structured JSON object matching the CriticEvaluation schema."""

class AuditorCriticAgent:
    """
    Independent Adversarial Quality Auditor for YouTube Scripts.
    Evaluates cold-open hook retention, narrative pacing, and structure
    against the 6-dimension rubric. Does not rewrite content.
    """
    def __init__(
        self,
        min_overall_score: float = settings.CRITIC_MIN_OVERALL_SCORE,
        min_individual_score: float = settings.CRITIC_MIN_INDIVIDUAL_SCORE,
        max_revisions: int = settings.MAX_REVISION_LOOPS
    ):
        self.min_overall = min_overall_score
        self.min_individual = min_individual_score
        self.max_revisions = max_revisions

    async def evaluate_script(
        self,
        brief: ResearchBrief,
        script: ScriptDraft,
        iteration: int = 1
    ) -> CriticEvaluation:
        """
        Adversarially evaluates a ScriptDraft and outputs objective pass/fail
        diagnostics with surgical directives for the ScriptDoctorAgent.
        """
        logger.info(f"AuditorCriticAgent evaluating Script Draft v{script.version} (Loop Iteration #{iteration})")

        prompt = f"""EVALUATION TARGET: SCRIPT DRAFT (v{script.version})
LOOP ITERATION: {iteration} of max {self.max_revisions}

TOPIC: {brief.topic}
CORE THESIS: {brief.core_thesis}
TARGET AUDIENCE: {brief.target_audience}
TARGET KEYWORDS: {', '.join(brief.target_keywords)}

=== SCRIPT DRAFT CONTENT ===
HOOK SECTION ({script.hook_segment.timestamp_estimate}):
Dialogue: "{script.hook_segment.spoken_dialogue}"
Visual Cues: "{script.hook_segment.visual_cues}"

BODY SECTIONS:
"""
        for s in script.body_sections:
            prompt += f"\n- [{s.section_title} | {s.timestamp_estimate}]\n  Dialogue: {s.spoken_dialogue[:200]}...\n  Visual: {s.visual_cues}\n"

        prompt += f"""
CTA SECTION ({script.cta_section.timestamp_estimate}):
Dialogue: "{script.cta_section.spoken_dialogue}"
Visual Cues: "{script.cta_section.visual_cues}"

Carefully score all 6 dimensions. If Hook or Pacing is weak, assign scores <= 2 and specify exact surgical directives for the Script Doctor."""

        evaluation = await LLMService.generate_structured(
            prompt=prompt,
            system_prompt=CRITIC_SYSTEM_PROMPT,
            response_model=CriticEvaluation,
            temperature=0.3
        )

        evaluation.iteration = iteration
        evaluation.target_agent = "script"

        # Thumbnail is evaluated downstream in Packaging stage; assign neutral pass for script stage
        evaluation.rubric.thumbnail_click_worthiness.score = 5
        evaluation.rubric.thumbnail_click_worthiness.justification = "Thumbnail evaluation is conducted downstream in Packaging stage."

        # Calculate exact mean score across script-relevant dimensions
        script_scores = [
            evaluation.rubric.hook_strength.score,
            evaluation.rubric.clarity_and_flow.score,
            evaluation.rubric.pacing_and_engagement.score,
            evaluation.rubric.seo_keyword_alignment.score,
            evaluation.rubric.brand_and_tone_fit.score
        ]
        evaluation.overall_score = round(sum(script_scores) / len(script_scores), 2)

        # Enforce threshold and revision cap logic
        has_critical_failure = any(s < self.min_individual for s in script_scores)
        is_failing = evaluation.overall_score < self.min_overall or has_critical_failure

        if is_failing:
            if iteration >= self.max_revisions:
                evaluation.decision = "ESCALATE_HUMAN"
                evaluation.summary_feedback = (
                    f"Max revision cap ({self.max_revisions}) reached without meeting quality threshold "
                    f"(Score: {evaluation.overall_score}/5.0). Escalating to human creator with diagnostic log."
                )
            else:
                evaluation.decision = "REVISE_SCRIPT"
        else:
            evaluation.decision = "APPROVED"

        logger.info(
            f"AuditorCriticAgent Evaluation Result: {evaluation.decision} | "
            f"Overall Score: {evaluation.overall_score}/5.0 | Hook: {evaluation.rubric.hook_strength.score}/5"
        )
        return evaluation


class PackagingAuditorAgent:
    """
    Dedicated Growth & Packaging Auditor evaluating SEO titles, chapters,
    and thumbnail CTR visual synergy.
    """
    def __init__(
        self,
        min_overall_score: float = settings.CRITIC_MIN_OVERALL_SCORE,
        min_individual_score: float = settings.CRITIC_MIN_INDIVIDUAL_SCORE,
        max_revisions: int = settings.MAX_REVISION_LOOPS
    ):
        self.min_overall = min_overall_score
        self.min_individual = min_individual_score
        self.max_revisions = max_revisions

    async def evaluate_package(
        self,
        brief: ResearchBrief,
        script: ScriptDraft,
        metadata: SEOMetadata,
        thumbnails: ThumbnailPackage,
        iteration: int = 1
    ) -> CriticEvaluation:
        """
        Evaluates the complete video package (script + SEO metadata + thumbnails).
        """
        logger.info(f"PackagingAuditorAgent evaluating Full Package (Iteration #{iteration})")

        prompt = f"""EVALUATION TARGET: COMPLETE VIDEO PACKAGE
LOOP ITERATION: {iteration} of max {self.max_revisions}

TOPIC: {brief.topic}
TARGET KEYWORDS: {', '.join(brief.target_keywords)}

=== SCRIPT (v{script.version}) ===
Hook: "{script.hook_segment.spoken_dialogue[:150]}"
Body Sections: {len(script.body_sections)} sections

=== SEO METADATA (v{metadata.version}) ===
Primary Title: "{metadata.primary_title}"
Alternative Titles: {metadata.alternative_titles}
Description Preview: "{metadata.description[:200]}..."
Tags: {metadata.tags[:8]}
Chapters: {len(metadata.chapters)} chapters

=== THUMBNAIL CONCEPTS (v{thumbnails.version}) ===
Recommended Concept #{thumbnails.recommended_concept_id}:
"""
        for c in thumbnails.concepts:
            prompt += f"- Concept #{c.concept_id} ({c.title_concept}): Text='{c.text_overlay}' | Visual='{c.visual_composition}' | Palette='{c.color_palette}'\n"

        evaluation = await LLMService.generate_structured(
            prompt=prompt,
            system_prompt=CRITIC_SYSTEM_PROMPT,
            response_model=CriticEvaluation,
            temperature=0.3
        )

        evaluation.iteration = iteration
        evaluation.target_agent = "all"

        scores = [
            evaluation.rubric.hook_strength.score,
            evaluation.rubric.clarity_and_flow.score,
            evaluation.rubric.pacing_and_engagement.score,
            evaluation.rubric.seo_keyword_alignment.score,
            evaluation.rubric.thumbnail_click_worthiness.score,
            evaluation.rubric.brand_and_tone_fit.score
        ]
        evaluation.overall_score = round(sum(scores) / len(scores), 2)

        has_critical_failure = any(s < self.min_individual for s in scores)
        is_failing = evaluation.overall_score < self.min_overall or has_critical_failure

        if is_failing:
            if iteration >= self.max_revisions:
                evaluation.decision = "ESCALATE_HUMAN"
            else:
                if evaluation.rubric.hook_strength.score < 3 or evaluation.rubric.pacing_and_engagement.score < 3:
                    evaluation.decision = "REVISE_SCRIPT"
                elif evaluation.rubric.seo_keyword_alignment.score < 3:
                    evaluation.decision = "REVISE_METADATA"
                elif evaluation.rubric.thumbnail_click_worthiness.score < 3:
                    evaluation.decision = "REVISE_THUMBNAIL"
                else:
                    evaluation.decision = "REVISE_SCRIPT"
        else:
            evaluation.decision = "APPROVED"

        return evaluation


class CriticAgent:
    """
    Unified / Backward-Compatible Critic Agent orchestrating both
    AuditorCriticAgent and PackagingAuditorAgent.
    """
    def __init__(
        self,
        min_overall_score: float = settings.CRITIC_MIN_OVERALL_SCORE,
        min_individual_score: float = settings.CRITIC_MIN_INDIVIDUAL_SCORE,
        max_revisions: int = settings.MAX_REVISION_LOOPS
    ):
        self.script_auditor = AuditorCriticAgent(min_overall_score, min_individual_score, max_revisions)
        self.package_auditor = PackagingAuditorAgent(min_overall_score, min_individual_score, max_revisions)
        self.min_overall = min_overall_score
        self.min_individual = min_individual_score
        self.max_revisions = max_revisions

    async def evaluate_script(self, brief: ResearchBrief, script: ScriptDraft, iteration: int = 1) -> CriticEvaluation:
        return await self.script_auditor.evaluate_script(brief, script, iteration)

    async def evaluate_package(
        self, brief: ResearchBrief, script: ScriptDraft,
        metadata: SEOMetadata, thumbnails: ThumbnailPackage, iteration: int = 1
    ) -> CriticEvaluation:
        return await self.package_auditor.evaluate_package(brief, script, metadata, thumbnails, iteration)

