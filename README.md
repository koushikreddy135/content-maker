# ContentMaker 🎬⚡
### Enterprise Decoupled Multi-Agent Studio for Autonomous YouTube Production & Social Repurposing

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/orchestration-LangGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![FastAPI](https://img.shields.io/badge/backend-FastAPI-teal.svg)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/frontend-React%2019-cyan.svg)](https://react.dev/)
[![Pydantic v2](https://img.shields.io/badge/validation-Pydantic%20v2-crimson.svg)](https://docs.pydantic.dev/)
[![SQLite Async](https://img.shields.io/badge/database-SQLite%20Async%20(aiosqlite)-lightgrey.svg)](https://docs.sqlalchemy.org/)

**ContentMaker** is an enterprise-grade, cyclic multi-agent AI system that transforms raw topic ideas into comprehensive, publish-ready media packages: full narrative scripts, mathematical retention audits, SEO metadata, 3D thumbnail concepts, production-ready AI B-roll shot lists, multi-platform social repurposing, and an interactive broadcast teleprompter.

Unlike naive, linear "generate-once" pipelines or circular self-evaluation loops where an author critiques its own work, ContentMaker implements a **Decoupled Actor-Critic-Doctor (Generator-Auditor-Refiner)** architecture. By eliminating cognitive anchoring bias and self-evaluation loops, ContentMaker achieves deterministic editorial quality with rigorous mathematical scoring, automated surgical refactoring, and hard-bounded human escalation safety gates.

---

## 💼 Resume-Ready Highlights (For AI & Software Engineers)

> **Feel free to adapt these bullet points directly for your resume, portfolio, or interview talking points:**

- **Multi-Agent Systems & Orchestration**: Architected a 7-node stateful cyclic multi-agent pipeline using **LangGraph**, replacing fragile linear chains with dynamic routing, parallel generation edges, and deterministic hard-cap escalation bounds.
- **Elimination of Self-Evaluation Bias**: Pioneered an **Actor-Critic-Doctor** pattern decoupling draft generation (`ScriptWriterAgent`), rubric-based auditing (`AuditorCriticAgent`), and surgical revision (`ScriptDoctorAgent`), resolving the fundamental LLM cognitive anchoring problem observed in standard circular loops.
- **Enterprise Data Modeling & Schema Integrity**: Designed 15+ strictly typed **Pydantic V2** schemas enforcing line-by-line justification citations, automated visual cue density constraints, and multi-format JSON export capabilities.
- **Resilient Inference & High-Availability LLM Engine**: Engineered an asynchronous LLM provider abstraction supporting **Groq**, **Google Gemini**, **OpenAI**, and **Anthropic**, featuring instant failover cascades on HTTP 429 rate limits, token estimation, and zero-downtime synthetic recovery.
- **Production Full-Stack Delivery**: Built a reactive dashboard in **React 19** and **FastAPI** backed by asynchronous **SQLAlchemy (aiosqlite)**, incorporating an in-browser 60fps autoscrolling **Teleprompter Studio** with mirror reflection mode for physical beamsplitter rigs.

---

## 🌟 The Core Architectural Paradigm: Actor-Critic-Doctor

```
               [ Topic Input ]
                      │
                      ▼
            [ 1. Research Agent ]
          (Web Trends, Brief & Thesis)
                      │
                      ▼
          ┌─► [ 2. Script Writer ] ◄──────────┐ (Author: First Draft Only)
          │   (Spoken Dialogue + Visuals)     │
          │           │                       │
          │           ▼                       │
          │   [ 3. Auditor Critic ]           │
          │   (5-Dimension Math Audit)        │
          │           │                       │
          │      Score < 4.0?                 │
          │    (REJECTED DRAFT)               │
          │           │                       │
          │           ▼                       │
          └── [ 3b. Script Doctor ] ──────────┘
             (Independent Specialist:
             Purges Throat-Clearing,
             Injects Retention Resets)
                      │
                 Score >= 4.0
                  (APPROVED)
                      │
                      ▼
         [ 4. Parallel Packaging ]
         ┌────────────┴────────────┐
         ▼                         ▼
   [ SEO Agent ]           [ Thumbnail Agent ]
   (Titles, Chapters)      (3D Compositions)
         └────────────┬────────────┘
                      │
                      ▼
          [ 5. Packaging Auditor ]
           (CTR & Metadata Audit)
                      │
                      ▼
     [ 6. B-Roll & Repurpose Agent ]
    (AI Shot List + Shorts + X Thread)
                      │
                      ▼
             [ ✅ Final Package ]
         (Teleprompter, MD/JSON Exporters)
```

### Why Self-Evaluation Loops Fail
In conventional multi-agent literature, many architectures send critique feedback directly back to the original generating agent (`Agent A ➔ Critic ➔ Agent A`). In practice, LLMs exhibit severe **cognitive anchoring**: an author model given its own draft frequently makes superficial token edits while preserving structurally flawed pacing, defensive arguments, or generic throat-clearing openings.

### The ContentMaker Solution
ContentMaker routes rejected drafts to an independent **ScriptDoctorAgent**. The Doctor:
1. Operates under an adversarial prompt explicitly instructed to challenge the author's narrative assumptions.
2. Slices out generic introductions and rewrites cold opens within the first 15 seconds.
3. Injects pattern interrupts, visual contrast resets every 90 seconds, and concrete stakes.
4. Produces a surgical `ScriptDoctorPrescription` detailing every modification for full editorial lineage.

---

## 🚀 Key System Features

### 1. 7-Node Cyclical LangGraph State Machine
- Dynamic conditional edges evaluate mathematical quality scores against configurable thresholds (`CRITIC_MIN_OVERALL_SCORE=4.0`, `CRITIC_MIN_INDIVIDUAL_SCORE=3.0`).
- Strict revision bounds (`MAX_REVISIONS=3`) guarantee prevention of infinite agent oscillation and runaway token expenditure.
- Graceful escalation path routes failed jobs to an `escalated_to_human` state with structured diagnostic reports.

### 2. AI B-Roll Shot List Generator
- Produces cinematic shot lists complete with:
  - Timestamp synchronization and shot scale (Macro, Close-up, Wide, POV).
  - Physical camera motion directives (slow push-in, parallax orbit, rapid whip pan).
  - Lighting schemes (cyberpunk rim lighting, Rembrandt, high-key diffuse).
  - Ready-to-use text-to-image/video generative prompts formulated specifically for **Midjourney v6** and **Runway Gen-3**.

### 3. Cross-Platform Social Repurposing Engine
- **Vertical Short / Reel / TikTok**: Generates a complete 60-second high-energy vertical script with visual hook triggers, 15s pacing beats, and caption placement guidelines.
- **5-Tweet Viral X Thread**: Extracts the core thesis, counter-intuitive insight, evidence breakdowns, and a high-CTR link/retweet call-to-action.

### 4. Interactive Teleprompter Studio
- Built-in studio teleprompter running at 60fps using browser `requestAnimationFrame`.
- Words-Per-Minute (WPM) speed slider (100–350 WPM) with dynamic velocity computation.
- **Mirror Mode**: Horizontally flips text for studio teleprompter glass (beamsplitter monitors).
- Interactive chapter scrub bar and real-time elapsed recording timer.

### 5. Multi-Format Asset Exporters
- One-click **Markdown (.MD)** export formatted for Notion, Obsidian, and Google Docs.
- One-click **Structured JSON** export for downstream headless rendering pipelines and CMS ingest.
- Quick-copy clipboard actions for immediate filming.

---

## 📊 The 6-Dimension Objective Rubric

| Dimension | Target Area | Score $\ge 4.0$ Requirement | Critical Failure Threshold |
| :--- | :--- | :--- | :--- |
| **1. Hook Strength** | 0–15s Cold Open | Immediate high-stakes premise, curiosity gap, zero greeting fluff | Generic intro ("Hey guys, welcome back") |
| **2. Clarity & Flow** | Narrative Spine | Clear thesis progression, intuitive analogies, seamless transitions | Disjointed leaps, jargon without grounding |
| **3. Pacing & B-Roll** | Visual Retention | Visual cue reset every 60–90s, high pattern interrupt density | Monologue wall of text, static presenter |
| **4. SEO Alignment** | Search Discovery | High-intent keywords naturally embedded in title, chapters, and script | Keyword stuffing or unsearchable abstraction |
| **5. Thumbnail CTR** | Packaging Synergy | High-contrast composition, 2–4 word text punch, emotional trigger | Cluttered text (>5 words), generic stock look |
| **6. Brand & Tone Fit** | Delivery Persona | Authoritative, dynamic, and educational; high signal-to-noise | Excessive sales hype or dry academic lecture |

---

## 🧪 Comprehensive Verification Suites

ContentMaker includes automated unit, integration, and scenario tests covering every agent and the end-to-end pipeline:

```bash
# 1. Research Agent test across diverse technical topics
python test_research.py

# 2. Script Writer Agent test verifying spoken dialogue and visual cues
python test_script.py

# 3. SEO Metadata & Thumbnail Generation test
python test_metadata_thumbnail.py

# 4. Decoupled Auditor & Packaging Critic test (demonstrating score jumping)
python test_critic.py

# 5. Full 7-Node Cyclical LangGraph Pipeline execution
python test_pipeline.py

# 6. FastAPI REST Endpoints & SQLite Async Persistence validation
python test_api.py

# 7. Complete Demo Scenario Suite (A: Clean Pass, B: Doctor Revision, C: Escalation)
python test_scenarios.py
```

---

## 🎯 3 Interactive Portfolio Demo Scenarios

In the React UI (`http://localhost:5173`), quick-launch presets demonstrate the core architectural capabilities:

1. **Scenario A (Clean Pass)**:
   - Topic: *How to Optimize Next.js App Router for Sub-Second Load Times*
   - Flow: Research ➔ Script ➔ Auditor (Score 5.0) ➔ Packaging ➔ Repurposing ➔ Approval.
2. **Scenario B (Core Differentiator — Zero Self-Evaluation Bias)**:
   - Topic: *Building Cyclic Multi-Agent Systems with LangGraph*
   - Flow: Draft 1 rejected for weak hook (Score 2/5) ➔ **ScriptDoctorAgent** refactors draft ➔ Auditor approves Draft 2 (Score 5/5) ➔ Package completed. Full diff visible in the Version History tab!
3. **Scenario C (Adversarial Escalation Gate)**:
   - Topic: *Cryptocurrency Guaranteed 100x Pump Scheme*
   - Flow: Evaluated against safety and authority rubric ➔ Reaches maximum 3-loop cap ➔ Safely halts and triggers **Human Escalation Gate** with diagnostic feedback.

---

## 🛠️ Quickstart Guide

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm

### 1. Repository Setup & Environment
```bash
git clone https://github.com/koushikreddy135/content-maker.git
cd content-maker
```

Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=sqlite+aiosqlite:///./contentmaker.db
LLM_MODEL=llama-3.3-70b-versatile
PORT=8000
HOST=0.0.0.0
```
*(Note: ContentMaker includes built-in synthetic fallback recovery; even if rate limits occur, pipeline execution will gracefully proceed).*

### 2. Backend Server
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run FastAPI backend with Uvicorn
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation will be accessible at `http://127.0.0.1:8000/docs`.

### 3. Frontend Dashboard
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser to launch the ContentMaker Studio.

---

## 🏛️ Repository Structure

```
yt project/
├── backend/
│   ├── agents/               # Autonomous specialized agents
│   │   ├── research.py       # Research & competitive intelligence
│   │   ├── script.py         # Primary script dialogue author
│   │   ├── script_doctor.py  # Decoupled refactoring & cold-open punch-up
│   │   ├── critic.py         # Auditor & packaging quality gates
│   │   ├── metadata.py       # SEO titles, tags, and timestamps
│   │   ├── thumbnail.py      # 3D composition & visual psychology
│   │   └── repurpose.py      # B-Roll shot list & multi-platform repurposing
│   ├── api/                  # FastAPI router endpoints & schemas
│   ├── database/             # SQLAlchemy async models & CRUD operations
│   ├── graph/                # LangGraph cyclical state machine & nodes
│   ├── models/               # Pydantic v2 schemas and validation models
│   └── services/             # LLM orchestration, model cascades & search tools
├── frontend/
│   ├── src/
│   │   ├── components/       # Reactive UI components
│   │   │   ├── Header.jsx
│   │   │   ├── TopicForm.jsx
│   │   │   ├── PipelineVisualizer.jsx
│   │   │   ├── VersionHistory.jsx
│   │   │   ├── TeleprompterModal.jsx   # 60fps autoscrolling teleprompter
│   │   │   └── FinalPackageView.jsx    # Complete deliverable studio
│   │   ├── App.jsx
│   │   └── index.css         # Cyberpunk design system
├── test_api.py               # Comprehensive API & DB verification
├── test_critic.py            # Auditor rubric verification
├── test_pipeline.py          # Cyclical LangGraph graph verification
├── test_scenarios.py         # Portfolio scenarios A, B, and C
├── ARCHITECTURE.md           # Formal architectural and theoretical specification
└── README.md                 # System overview and resume guide
```

---
