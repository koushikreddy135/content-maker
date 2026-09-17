import logging
from typing import Optional
from backend.models.schemas import (
    ResearchBrief, ScriptDraft, SEOMetadata,
    BRollShotList, BRollShot, RepurposedContent,
    RepurposedShort, TwitterThreadPost
)
from backend.services.llm import LLMService

logger = logging.getLogger(__name__)

BROLL_SYSTEM_PROMPT = """You are a senior Director of Photography and AI VFX Prompt Engineer for high-end YouTube video essays.
Your mission is to analyze an approved YouTube script and generate a structured, production-ready B-Roll Shot List with actionable generative AI prompts (for Midjourney v6, Runway Gen-3, Sora) and stock footage search queries.

SHOT REQUIREMENTS:
- Produce 4 to 8 high-impact B-roll shots spanning the entire video timeline.
- Assign diverse shot types (Extreme Close-Up, Dynamic Split Screen, 3D Kinetic Motion Graphic, POV Dolly Zoom, Macro Lens).
- For each shot, write an evocative, photorealistic generative prompt specifying lighting, camera movement, composition, and mood.
- Include 3-5 precise stock footage search tags per shot.

Return ONLY a valid JSON object matching the BRollShotList schema."""

REPURPOSE_SYSTEM_PROMPT = """You are a viral social media strategist specializing in multi-platform content repurposing for top digital creators.
Your mission is to transform an approved long-form YouTube video script into:
1. A 60-second viral vertical video script for YouTube Shorts, TikTok, and Instagram Reels (9:16).
   - Instant 1.5-second scroll-stopping text overlay hook.
   - Rapid spoken script with cadence cues.
   - Pacing resets and caption sync.
2. A 5-post high-engagement X/Twitter Thread that hooks the timeline, delivers the core insight concisely, and drives clicks to the full video.
3. 3-4 executive takeaways suitable for LinkedIn or newsletter syndication.

Return ONLY a valid JSON object matching the RepurposedContent schema."""

class RepurposeAndBRollAgent:
    """
    Autonomous agent generating B-Roll shot lists with generative video prompts
    and multi-platform social repurposing (Shorts + X Thread).
    """
    async def generate_broll_shot_list(
        self,
        brief: ResearchBrief,
        script: ScriptDraft
    ) -> BRollShotList:
        logger.info(f"RepurposeAndBRollAgent generating B-Roll Shot List for '{brief.topic}'")

        prompt = f"""TOPIC: {brief.topic}
TARGET AUDIENCE: {brief.target_audience}
CORE THESIS: {brief.core_thesis}

=== APPROVED SCRIPT VISUAL CUES ===
Hook Visual: {script.hook_segment.visual_cues}
""" + "\n".join([f"Section '{s.section_title}': {s.visual_cues}" for s in script.body_sections]) + f"""
CTA Visual: {script.cta_section.visual_cues}

Create a structured production B-Roll Shot List with detailed camera directions and generative AI prompts."""

        return await LLMService.generate_structured(
            prompt=prompt,
            system_prompt=BROLL_SYSTEM_PROMPT,
            response_model=BRollShotList,
            temperature=0.4
        )

    async def generate_repurposed_content(
        self,
        brief: ResearchBrief,
        script: ScriptDraft,
        metadata: Optional[SEOMetadata] = None
    ) -> RepurposedContent:
        logger.info(f"RepurposeAndBRollAgent generating multi-platform repurposing for '{brief.topic}'")

        title_info = metadata.primary_title if metadata else brief.topic
        prompt = f"""TOPIC: {brief.topic}
PRIMARY TITLE: {title_info}
CORE THESIS: {brief.core_thesis}
HOOK: {script.hook_segment.spoken_dialogue}

KEY POINTS COVERED:
""" + "\n".join([f"- {kp}" for kp in brief.key_points]) + """

Generate a 60-second viral vertical Shorts/Reels script and a 5-tweet high-engagement thread."""

        return await LLMService.generate_structured(
            prompt=prompt,
            system_prompt=REPURPOSE_SYSTEM_PROMPT,
            response_model=RepurposedContent,
            temperature=0.5
        )
