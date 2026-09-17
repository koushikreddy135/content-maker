from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class JobRecord(Base):
    __tablename__ = "jobs"

    id = Column(String(64), primary_key=True)
    topic = Column(String(512), nullable=False)
    status = Column(String(64), default="pending")  # in_progress, approved, escalated_to_human, failed
    current_node = Column(String(64), default="start")
    total_revisions = Column(Integer, default=0)
    final_overall_score = Column(Float, nullable=True)
    escalation_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    research_brief = relationship("ResearchBriefRecord", back_populates="job", uselist=False, cascade="all, delete-orphan")
    draft_versions = relationship("DraftVersionRecord", back_populates="job", cascade="all, delete-orphan", order_by="DraftVersionRecord.version")
    critic_evaluations = relationship("CriticEvaluationRecord", back_populates="job", cascade="all, delete-orphan", order_by="CriticEvaluationRecord.iteration")
    final_package = relationship("FinalPackageRecord", back_populates="job", uselist=False, cascade="all, delete-orphan")


class ResearchBriefRecord(Base):
    __tablename__ = "research_briefs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String(64), ForeignKey("jobs.id"), nullable=False)
    brief_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("JobRecord", back_populates="research_brief")


class DraftVersionRecord(Base):
    __tablename__ = "draft_versions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String(64), ForeignKey("jobs.id"), nullable=False)
    draft_type = Column(String(64), nullable=False)  # script, metadata, thumbnail
    version = Column(Integer, nullable=False)
    content = Column(JSON, nullable=False)
    revision_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("JobRecord", back_populates="draft_versions")


class CriticEvaluationRecord(Base):
    __tablename__ = "critic_evaluations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String(64), ForeignKey("jobs.id"), nullable=False)
    iteration = Column(Integer, nullable=False)
    target_agent = Column(String(64), nullable=False)
    rubric_scores = Column(JSON, nullable=False)
    overall_score = Column(Float, nullable=False)
    decision = Column(String(64), nullable=False)
    summary_feedback = Column(Text, nullable=False)
    specific_directives = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("JobRecord", back_populates="critic_evaluations")


class FinalPackageRecord(Base):
    __tablename__ = "final_packages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String(64), ForeignKey("jobs.id"), nullable=False)
    script_markdown = Column(Text, nullable=False)
    metadata_json = Column(JSON, nullable=False)
    thumbnail_json = Column(JSON, nullable=False)
    broll_json = Column(JSON, nullable=True)
    repurposed_json = Column(JSON, nullable=True)
    doctor_prescriptions_json = Column(JSON, nullable=True)
    quality_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("JobRecord", back_populates="final_package")

