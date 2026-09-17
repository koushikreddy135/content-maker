from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

# --- Step 2: Research Models ---
class CompetitorAngle(BaseModel):
    existing_coverage: str = Field(description="Summary of how existing YouTube videos or articles cover this topic")
    differentiation_hook: str = Field(description="What unique angle, counterintuitive insight, or fresh perspective our video will take")

class ResearchBrief(BaseModel):
    topic: str
    target_audience: str = Field(description="Target viewer persona, skill level, and pain points")
    core_thesis: str = Field(description="Main takeaway or big idea of the video")
    key_points: List[str] = Field(description="Key structured arguments, facts, or workflow steps to cover")
    hook_angles: List[str] = Field(description="2-3 provocative or curiosity-driven hook ideas for the first 15 seconds")
    competitive_angle: CompetitorAngle
    target_keywords: List[str] = Field(description="Primary and secondary search keywords")
    sources_cited: List[str] = Field(default_factory=list, description="Verified sources or real URLs gathered during research")


# --- Step 3: Script Models ---
class ScriptSection(BaseModel):
    section_title: str = Field(description="Name of section, e.g. Hook, Problem Setup, Point 1, CTA")
    timestamp_estimate: str = Field(description="Estimated timing (e.g. 0:00-0:15)")
    spoken_dialogue: str = Field(description="Exact presenter voiceover/dialogue")
    visual_cues: str = Field(description="B-roll, on-screen graphics, text popups, or camera angle cues")

class ScriptDraft(BaseModel):
    version: int = Field(default=1, description="Draft version number")
    duration_target: str = Field(default="8-10 mins", description="Target video duration")
    tone: str = Field(default="authoritative yet conversational", description="Tone of the delivery")
    hook_segment: ScriptSection = Field(description="The critical first 15 seconds hook")
    body_sections: List[ScriptSection] = Field(description="Main body sections with visual and narrative flow")
    cta_section: Optional[ScriptSection] = Field(default=None, description="Closing call to action and outro")
    full_text_markdown: Optional[str] = Field(default="", description="Combined formatted teleprompter-ready markdown script")
    revision_notes: Optional[str] = Field(default=None, description="What was improved from previous iteration if revised")



# --- Step 4: SEO and Thumbnail Models ---
class ChapterMarker(BaseModel):
    timestamp: str = Field(description="Timestamp in format MM:SS")
    title: str = Field(description="Chapter title")

class SEOMetadata(BaseModel):
    version: int = Field(default=1)
    primary_title: str = Field(description="Top recommended YouTube title (high CTR & SEO)")
    alternative_titles: List[str] = Field(description="2-3 alternative title variations (Curiosity, Direct, Question)")
    description: str = Field(description="Full SEO-optimized YouTube description with summary, value props, and links")
    tags: List[str] = Field(description="Optimized YouTube tags (15-20 comma separated keywords)")
    hashtags: List[str] = Field(description="3-5 relevant trending hashtags (#AI #Tech etc.)")
    chapters: List[ChapterMarker] = Field(description="Structured video chapters/timestamps")
    revision_notes: Optional[str] = Field(default=None)

class ThumbnailConcept(BaseModel):
    concept_id: int
    title_concept: str = Field(description="Name of this thumbnail variant (e.g., 'Shocked Contrast', 'Curiosity Split')")
    visual_composition: str = Field(description="Foreground elements, presenter expression, background contrast")
    text_overlay: str = Field(description="Max 3-5 punchy words in bold high-contrast typography")
    color_palette: str = Field(description="Dominant colors, e.g. Neon Yellow & Dark Charcoal for high CTR")
    emotional_trigger: str = Field(description="Target psychological trigger (FOMO, shock, relief, curiosity)")

class ThumbnailPackage(BaseModel):
    version: int = Field(default=1)
    concepts: List[ThumbnailConcept] = Field(description="2-3 structured thumbnail options")
    recommended_concept_id: int = Field(description="The primary recommended thumbnail option")
    revision_notes: Optional[str] = Field(default=None)


# --- Step 5: Critic & Rubric Models ---
class DimensionScore(BaseModel):
    score: int = Field(ge=1, le=5, description="Score from 1 (poor) to 5 (exceptional)")
    justification: str = Field(description="Specific analytical reason for this score citing concrete draft lines")
    actionable_improvement: Optional[str] = Field(default=None, description="Concrete instruction on how to fix this dimension if < 4")

class CriticRubric(BaseModel):
    hook_strength: DimensionScore = Field(description="Grip in first 5-15s, curiosity gap, no slow throat-clearing")
    clarity_and_flow: DimensionScore = Field(description="Logical transition, clarity of explanations, no rambling")
    pacing_and_engagement: DimensionScore = Field(description="B-roll cue density, retention resets, pattern interrupts")
    seo_keyword_alignment: DimensionScore = Field(description="Natural integration of primary search terms in script/metadata")
    thumbnail_click_worthiness: DimensionScore = Field(description="Visual intrigue, thumbnail-to-title synergy without clickbait bait-and-switch")
    brand_and_tone_fit: DimensionScore = Field(description="Professional, credible, educational yet energetic delivery")

class CriticEvaluation(BaseModel):
    iteration: int = Field(description="Current loop iteration number")
    target_agent: Literal["script", "metadata", "thumbnail", "all"] = Field(description="Which component was evaluated")
    rubric: CriticRubric
    overall_score: float = Field(description="Mean average score across 6 dimensions")
    decision: Literal["APPROVED", "REVISE_SCRIPT", "REVISE_METADATA", "REVISE_THUMBNAIL", "ESCALATE_HUMAN"]
    summary_feedback: str = Field(description="High-level feedback summary provided back to generating agents")
    specific_directives: List[str] = Field(description="Bulleted mandatory revisions required for next draft")



# --- Step 6: Script Doctor & Editorial Refinement Models ---
class ScriptDoctorPrescription(BaseModel):
    prescription_id: int = Field(default=1)
    target_draft_version: int = Field(description="Draft version being surgically refactored")
    new_draft_version: int = Field(description="New revised draft version produced")
    addressed_critique_summary: str = Field(description="Summary of how auditor directives were resolved without author self-evaluation bias")
    hook_refactor_notes: str = Field(description="Surgical restructuring of the cold open")
    pacing_interventions: List[str] = Field(description="Specific pattern interrupts and B-roll resets injected")
    revised_script: ScriptDraft = Field(description="The refactored script draft")


# --- Step 7: B-Roll Shot List & Multi-Platform Repurposing Models ---
class BRollShot(BaseModel):
    shot_number: int
    timestamp_range: str = Field(description="e.g. 0:00 - 0:15")
    shot_type: str = Field(description="e.g. Dynamic Split Screen, 3D Kinetic Motion Graphic, Macro Close-Up")
    visual_description: str = Field(description="Actionable director instruction for video editor")
    generative_ai_prompt: str = Field(description="Production-ready prompt for Midjourney v6 / Runway Gen-3 / Sora")
    stock_search_keywords: List[str] = Field(description="Search tags for Storyblocks / Envato Elements")

class BRollShotList(BaseModel):
    total_shots: int
    shots: List[BRollShot]

class RepurposedShort(BaseModel):
    platform: str = Field(default="YouTube Shorts / TikTok / Instagram Reels (9:16)")
    hook_text: str = Field(description="Text overlay to freeze scroll in 1.5s")
    spoken_script_60s: str = Field(description="Fast-paced 60-second vertical video teleprompter script")
    on_screen_captions: List[str] = Field(description="Rapid caption pacing cues")
    estimated_duration: str = Field(default="55-60 seconds")

class TwitterThreadPost(BaseModel):
    post_number: int
    post_text: str = Field(description="Tweet text under 280 characters with curiosity hook or takeaway")

class RepurposedContent(BaseModel):
    short_form: RepurposedShort
    twitter_thread: List[TwitterThreadPost]
    summary_takeaways: List[str] = Field(description="Executive bullet points for LinkedIn or newsletter")


# --- Pipeline State & API Response Models ---
class CompleteVideoPackage(BaseModel):
    job_id: str
    topic: str
    status: Literal["approved", "escalated_to_human", "in_progress", "failed"]
    total_revisions: int
    research_brief: ResearchBrief
    final_script: ScriptDraft
    final_metadata: SEOMetadata
    final_thumbnails: ThumbnailPackage
    critic_history: List[CriticEvaluation]
    doctor_prescriptions: List[ScriptDoctorPrescription] = Field(default_factory=list)
    broll_shot_list: Optional[BRollShotList] = None
    repurposed_content: Optional[RepurposedContent] = None
    final_overall_score: float
    escalation_reason: Optional[str] = None

