import json
import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from backend.database.models import (
    JobRecord, ResearchBriefRecord, DraftVersionRecord,
    CriticEvaluationRecord, FinalPackageRecord
)
from backend.models.schemas import (
    ResearchBrief, ScriptDraft, SEOMetadata,
    ThumbnailPackage, CriticEvaluation
)

logger = logging.getLogger(__name__)

class DatabaseService:
    @staticmethod
    async def create_job(session: AsyncSession, job_id: str, topic: str) -> JobRecord:
        job = JobRecord(
            id=job_id,
            topic=topic,
            status="in_progress",
            current_node="research",
            total_revisions=0
        )
        session.add(job)
        await session.commit()
        await session.refresh(job)
        return job

    @staticmethod
    async def update_job_status(
        session: AsyncSession,
        job_id: str,
        status: str,
        current_node: str,
        total_revisions: int = 0,
        final_score: Optional[float] = None,
        escalation_reason: Optional[str] = None
    ):
        stmt = select(JobRecord).where(JobRecord.id == job_id)
        result = await session.execute(stmt)
        job = result.scalar_one_or_none()
        if job:
            job.status = status
            job.current_node = current_node
            job.total_revisions = total_revisions
            if final_score is not None:
                job.final_overall_score = final_score
            if escalation_reason is not None:
                job.escalation_reason = escalation_reason
            await session.commit()

    @staticmethod
    async def save_research_brief(session: AsyncSession, job_id: str, brief: ResearchBrief):
        record = ResearchBriefRecord(
            job_id=job_id,
            brief_data=brief.model_dump()
        )
        session.add(record)
        await session.commit()

    @staticmethod
    async def save_draft_version(
        session: AsyncSession,
        job_id: str,
        draft_type: str,
        version: int,
        content: Dict[str, Any],
        revision_notes: Optional[str] = None
    ):
        record = DraftVersionRecord(
            job_id=job_id,
            draft_type=draft_type,
            version=version,
            content=content,
            revision_notes=revision_notes
        )
        session.add(record)
        await session.commit()

    @staticmethod
    async def save_critic_evaluation(
        session: AsyncSession,
        job_id: str,
        evaluation: CriticEvaluation
    ):
        record = CriticEvaluationRecord(
            job_id=job_id,
            iteration=evaluation.iteration,
            target_agent=evaluation.target_agent,
            rubric_scores=evaluation.rubric.model_dump(),
            overall_score=evaluation.overall_score,
            decision=evaluation.decision,
            summary_feedback=evaluation.summary_feedback,
            specific_directives=evaluation.specific_directives
        )
        session.add(record)
        await session.commit()

    @staticmethod
    async def save_final_package(
        session: AsyncSession,
        job_id: str,
        script_md: str,
        metadata_dict: Dict[str, Any],
        thumbnails_dict: Dict[str, Any],
        quality_score: float,
        broll_dict: Optional[Dict[str, Any]] = None,
        repurposed_dict: Optional[Dict[str, Any]] = None,
        doctor_prescriptions_list: Optional[List[Dict[str, Any]]] = None
    ):
        record = FinalPackageRecord(
            job_id=job_id,
            script_markdown=script_md,
            metadata_json=metadata_dict,
            thumbnail_json=thumbnails_dict,
            broll_json=broll_dict,
            repurposed_json=repurposed_dict,
            doctor_prescriptions_json=doctor_prescriptions_list,
            quality_score=quality_score
        )
        session.add(record)
        await session.commit()

    @staticmethod
    async def get_all_jobs(session: AsyncSession) -> List[JobRecord]:
        stmt = select(JobRecord).order_by(desc(JobRecord.created_at))
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_job_by_id(session: AsyncSession, job_id: str) -> Optional[JobRecord]:
        stmt = select(JobRecord).where(JobRecord.id == job_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_job_history(session: AsyncSession, job_id: str) -> Dict[str, Any]:
        job_stmt = select(JobRecord).where(JobRecord.id == job_id)
        job_res = await session.execute(job_stmt)
        job = job_res.scalar_one_or_none()

        if not job:
            return None

        brief_stmt = select(ResearchBriefRecord).where(ResearchBriefRecord.job_id == job_id)
        brief_res = await session.execute(brief_stmt)
        brief = brief_res.scalar_one_or_none()

        drafts_stmt = select(DraftVersionRecord).where(DraftVersionRecord.job_id == job_id).order_by(DraftVersionRecord.version)
        drafts_res = await session.execute(drafts_stmt)
        drafts = drafts_res.scalars().all()

        critic_stmt = select(CriticEvaluationRecord).where(CriticEvaluationRecord.job_id == job_id).order_by(CriticEvaluationRecord.iteration)
        critic_res = await session.execute(critic_stmt)
        evals = critic_res.scalars().all()

        final_stmt = select(FinalPackageRecord).where(FinalPackageRecord.job_id == job_id)
        final_res = await session.execute(final_stmt)
        final_pkg = final_res.scalar_one_or_none()

        return {
            "job": {
                "id": job.id,
                "topic": job.topic,
                "status": job.status,
                "current_node": job.current_node,
                "total_revisions": job.total_revisions,
                "final_overall_score": job.final_overall_score,
                "escalation_reason": job.escalation_reason,
                "created_at": job.created_at.isoformat() if job.created_at else None
            },
            "research_brief": brief.brief_data if brief else None,
            "drafts": [
                {
                    "type": d.draft_type,
                    "version": d.version,
                    "content": d.content,
                    "revision_notes": d.revision_notes,
                    "created_at": d.created_at.isoformat() if d.created_at else None
                }
                for d in drafts
            ],
            "critic_evaluations": [
                {
                    "iteration": e.iteration,
                    "target_agent": e.target_agent,
                    "rubric_scores": e.rubric_scores,
                    "overall_score": e.overall_score,
                    "decision": e.decision,
                    "summary_feedback": e.summary_feedback,
                    "specific_directives": e.specific_directives,
                    "created_at": e.created_at.isoformat() if e.created_at else None
                }
                for e in evals
            ],
            "final_package": {
                "script_markdown": final_pkg.script_markdown,
                "metadata": final_pkg.metadata_json,
                "thumbnails": final_pkg.thumbnail_json,
                "broll_shot_list": final_pkg.broll_json,
                "repurposed_content": final_pkg.repurposed_json,
                "doctor_prescriptions": final_pkg.doctor_prescriptions_json or [],
                "quality_score": final_pkg.quality_score
            } if final_pkg else None
        }

