from typing import List, Optional, Dict, Any
from typing_extensions import TypedDict
from backend.models.schemas import (
    ResearchBrief, ScriptDraft, SEOMetadata,
    ThumbnailPackage, CriticEvaluation,
    ScriptDoctorPrescription, BRollShotList, RepurposedContent
)

class ContentMakerState(TypedDict):
    job_id: str
    topic: str
    duration_target: str
    tone: str
    research_brief: Optional[ResearchBrief]
    script_drafts: List[ScriptDraft]
    current_script: Optional[ScriptDraft]
    doctor_prescriptions: List[ScriptDoctorPrescription]
    metadata_drafts: List[SEOMetadata]
    current_metadata: Optional[SEOMetadata]
    thumbnail_drafts: List[ThumbnailPackage]
    current_thumbnails: Optional[ThumbnailPackage]
    critic_evaluations: List[CriticEvaluation]
    latest_critic_eval: Optional[CriticEvaluation]
    broll_shot_list: Optional[BRollShotList]
    repurposed_content: Optional[RepurposedContent]
    revision_count: int
    max_revisions: int
    status: str  # in_progress, approved, escalated_to_human, failed
    current_step: str
    step_logs: List[Dict[str, Any]]
    escalation_reason: Optional[str]

# Backward compatibility alias
ContentForgeState = ContentMakerState

