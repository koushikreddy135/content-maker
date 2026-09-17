import asyncio
import json
import uuid
import logging
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.db import get_db, AsyncSessionLocal
from backend.database.crud import DatabaseService
from backend.graph.pipeline import contentmaker_pipeline, contentforge_pipeline, emit_event
from backend.graph.state import ContentMakerState, ContentForgeState

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")

# Active SSE client queues per job_id
_job_event_queues: Dict[str, List[asyncio.Queue]] = {}

class GenerateRequest(BaseModel):
    topic: str
    duration_target: Optional[str] = "8-10 mins"
    tone: Optional[str] = "authoritative, dynamic, and educational"
    max_revisions: Optional[int] = 3

class GenerateResponse(BaseModel):
    job_id: str
    topic: str
    status: str
    message: str

async def run_pipeline_task(job_id: str, topic: str, duration_target: str, tone: str, max_revisions: int):
    """
    Background worker executing ContentMaker LangGraph pipeline and persisting every step to SQLite.
    """
    logger.info(f"Starting async pipeline worker for Job: {job_id}")
    
    initial_state: ContentMakerState = {
        "job_id": job_id,
        "topic": topic,
        "duration_target": duration_target,
        "tone": tone,
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
        "max_revisions": max_revisions,
        "status": "in_progress",
        "current_step": "research",
        "step_logs": [],
        "escalation_reason": None
    }

    async def broadcast_job_event(event_dict: Dict[str, Any]):
        if job_id in _job_event_queues:
            for q in _job_event_queues[job_id]:
                await q.put(event_dict)

    try:
        # Run graph
        final_state = await contentmaker_pipeline.ainvoke(initial_state)

        # Persist full state to SQLite
        async with AsyncSessionLocal() as db_session:
            # 1. Brief
            if final_state.get("research_brief"):
                await DatabaseService.save_research_brief(db_session, job_id, final_state["research_brief"])

            # 2. Script Drafts
            for script in final_state.get("script_drafts", []):
                await DatabaseService.save_draft_version(
                    db_session,
                    job_id=job_id,
                    draft_type="script",
                    version=script.version,
                    content=script.model_dump(),
                    revision_notes=script.revision_notes
                )

            # 3. Metadata Drafts
            for meta in final_state.get("metadata_drafts", []):
                await DatabaseService.save_draft_version(
                    db_session,
                    job_id=job_id,
                    draft_type="metadata",
                    version=meta.version,
                    content=meta.model_dump(),
                    revision_notes=meta.revision_notes
                )

            # 4. Thumbnail Drafts
            for thumb in final_state.get("thumbnail_drafts", []):
                await DatabaseService.save_draft_version(
                    db_session,
                    job_id=job_id,
                    draft_type="thumbnail",
                    version=thumb.version,
                    content=thumb.model_dump(),
                    revision_notes=thumb.revision_notes
                )

            # 5. Critic Evaluations
            for ev in final_state.get("critic_evaluations", []):
                await DatabaseService.save_critic_evaluation(db_session, job_id, ev)

            # 6. Final Package if approved
            if final_state["status"] == "approved" and final_state.get("current_script"):
                final_score = final_state["latest_critic_eval"].overall_score if final_state.get("latest_critic_eval") else 5.0
                await DatabaseService.save_final_package(
                    db_session,
                    job_id=job_id,
                    script_md=final_state["current_script"].full_text_markdown,
                    metadata_dict=final_state["current_metadata"].model_dump() if final_state.get("current_metadata") else {},
                    thumbnails_dict=final_state["current_thumbnails"].model_dump() if final_state.get("current_thumbnails") else {},
                    quality_score=final_score,
                    broll_dict=final_state["broll_shot_list"].model_dump() if final_state.get("broll_shot_list") else None,
                    repurposed_dict=final_state["repurposed_content"].model_dump() if final_state.get("repurposed_content") else None,
                    doctor_prescriptions_list=[p.model_dump() for p in final_state.get("doctor_prescriptions", [])]
                )

            # 7. Update Job status
            await DatabaseService.update_job_status(
                db_session,
                job_id=job_id,
                status=final_state["status"],
                current_node="completed" if final_state["status"] == "approved" else "escalated",
                total_revisions=final_state.get("revision_count", 0),
                final_score=final_state.get("latest_critic_eval").overall_score if final_state.get("latest_critic_eval") else None,
                escalation_reason=final_state.get("escalation_reason")
            )

        await broadcast_job_event({
            "event": "pipeline_complete",
            "job_id": job_id,
            "status": final_state["status"],
            "broll": final_state["broll_shot_list"].model_dump() if final_state.get("broll_shot_list") else None,
            "repurposed": final_state["repurposed_content"].model_dump() if final_state.get("repurposed_content") else None
        })


    except Exception as e:
        logger.error(f"Pipeline execution error for Job {job_id}: {e}", exc_info=True)
        async with AsyncSessionLocal() as db_session:
            await DatabaseService.update_job_status(
                db_session,
                job_id=job_id,
                status="failed",
                current_node="error",
                escalation_reason=str(e)
            )
        await broadcast_job_event({
            "event": "pipeline_error",
            "job_id": job_id,
            "error": str(e)
        })


@router.post("/generate", response_model=GenerateResponse)
async def generate_video_package(
    req: GenerateRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Submits a raw topic and starts the autonomous cyclic multi-agent pipeline.
    """
    job_id = f"job_{uuid.uuid4().hex[:12]}"
    await DatabaseService.create_job(db, job_id=job_id, topic=req.topic)

    background_tasks.add_task(
        run_pipeline_task,
        job_id=job_id,
        topic=req.topic,
        duration_target=req.duration_target,
        tone=req.tone,
        max_revisions=req.max_revisions
    )

    return GenerateResponse(
        job_id=job_id,
        topic=req.topic,
        status="in_progress",
        message="Multi-agent cyclic pipeline initiated."
    )


@router.get("/jobs")
async def list_jobs(db: AsyncSession = Depends(get_db)):
    """Returns all past video generation runs."""
    jobs = await DatabaseService.get_all_jobs(db)
    return [
        {
            "id": j.id,
            "topic": j.topic,
            "status": j.status,
            "current_node": j.current_node,
            "total_revisions": j.total_revisions,
            "final_overall_score": j.final_overall_score,
            "escalation_reason": j.escalation_reason,
            "created_at": j.created_at.isoformat() if j.created_at else None
        }
        for j in jobs
    ]


@router.get("/jobs/{job_id}")
async def get_job_status(job_id: str, db: AsyncSession = Depends(get_db)):
    """Returns the current status of a specific generation job."""
    job = await DatabaseService.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "id": job.id,
        "topic": job.topic,
        "status": job.status,
        "current_node": job.current_node,
        "total_revisions": job.total_revisions,
        "final_overall_score": job.final_overall_score,
        "escalation_reason": job.escalation_reason,
        "created_at": job.created_at.isoformat() if job.created_at else None,
        "updated_at": job.updated_at.isoformat() if job.updated_at else None
    }


@router.get("/jobs/{job_id}/history")
async def get_job_history(job_id: str, db: AsyncSession = Depends(get_db)):
    """
    Returns complete explainability data: draft versions (v1 vs v2 diffs)
    and full critic evaluations.
    """
    history = await DatabaseService.get_job_history(db, job_id)
    if not history:
        raise HTTPException(status_code=404, detail="Job history not found")
    return history


@router.get("/jobs/{job_id}/final")
async def get_final_package(job_id: str, db: AsyncSession = Depends(get_db)):
    """Returns the complete, publish-ready YouTube video package."""
    history = await DatabaseService.get_job_history(db, job_id)
    if not history:
        raise HTTPException(status_code=404, detail="Job not found")
    if not history.get("final_package") and history["job"]["status"] != "approved":
        raise HTTPException(status_code=400, detail="Package is not approved or still in progress")
    return history.get("final_package")


@router.get("/jobs/{job_id}/stream")
async def stream_job_events(job_id: str):
    """
    SSE stream for live visual pipeline updates in the React frontend.
    """
    queue = asyncio.Queue()
    if job_id not in _job_event_queues:
        _job_event_queues[job_id] = []
    _job_event_queues[job_id].append(queue)

    async def event_generator():
        try:
            # Yield initial connection heartbeat
            yield f"data: {json.dumps({'event': 'connected', 'job_id': job_id})}\n\n"
            while True:
                data = await queue.get()
                yield f"data: {json.dumps(data)}\n\n"
                if data.get("event") in ["pipeline_complete", "pipeline_error"]:
                    break
        except asyncio.CancelledError:
            pass
        finally:
            if job_id in _job_event_queues and queue in _job_event_queues[job_id]:
                _job_event_queues[job_id].remove(queue)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
