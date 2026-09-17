import asyncio
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from backend.agents.research import ResearchAgent
from backend.agents.script import ScriptAgent
from backend.agents.critic import CriticAgent
from backend.models.schemas import ScriptDraft, ScriptSection

async def test_critic_scoring():
    print("=" * 70)
    print("TESTING CRITIC AGENT 6-DIMENSION RUBRIC & EXPLAINABILITY")
    print("=" * 70)

    research_agent = ResearchAgent()
    critic_agent = CriticAgent(min_overall_score=4.0, min_individual_score=3.0, max_revisions=3)

    topic = "Building Cyclic Multi-Agent Systems with LangGraph"
    brief = await research_agent.run(topic)

    # 1. Test against a deliberately weak Draft 1 (with throat-clearing intro)
    weak_draft = ScriptDraft(
        version=1,
        duration_target="8-10 mins",
        tone="conversational",
        hook_segment=ScriptSection(
            section_title="Intro",
            timestamp_estimate="0:00 - 0:20",
            spoken_dialogue="Hey guys, welcome back to the channel. Today we're going to talk about building multi-agent systems.",
            visual_cues="Presenter sitting at desk talking to camera."
        ),
        body_sections=[
            ScriptSection(
                section_title="Point 1",
                timestamp_estimate="0:20 - 3:00",
                spoken_dialogue="Multi-agent systems are nice because agents can collaborate together.",
                visual_cues="Presenter continues talking."
            )
        ],
        cta_section=ScriptSection(
            section_title="Outro",
            timestamp_estimate="3:00 - 3:30",
            spoken_dialogue="Thanks for watching. Don't forget to like and subscribe.",
            visual_cues="Subscribe text."
        ),
        full_text_markdown="# Weak Script"
    )

    print("\n--- EVALUATING WEAK DRAFT 1 ---")
    eval_1 = await critic_agent.evaluate_script(brief, weak_draft, iteration=1)

    print(f"Decision: {eval_1.decision}")
    print(f"Overall Score: {eval_1.overall_score}/5.0")
    print(f"Hook Strength Score: {eval_1.rubric.hook_strength.score}/5 -> {eval_1.rubric.hook_strength.justification}")
    print(f"Actionable Directive: {eval_1.rubric.hook_strength.actionable_improvement}")
    print(f"Specific Directives count: {len(eval_1.specific_directives)}")

    assert eval_1.decision == "REVISE_SCRIPT", "Critic MUST reject weak Draft 1"
    assert eval_1.rubric.hook_strength.score <= 2, "Hook score must be low for generic intro"
    assert len(eval_1.specific_directives) > 0, "Must provide actionable directives"

    # 2. Test against an improved Draft 2 (strong hook, high visual density, detailed body)
    strong_draft = ScriptDraft(
        version=2,
        duration_target="8-10 mins",
        tone="authoritative, dynamic, and educational",
        hook_segment=ScriptSection(
            section_title="Cold Open",
            timestamp_estimate="0:00 - 0:15",
            spoken_dialogue="Stop building linear AI pipelines that fail silently. In the next 8 minutes, I will show you why single-pass LLM prompt chains break in production—and how to deploy a cyclic multi-agent system with LangGraph that self-corrects using automated quality gates.",
            visual_cues="DYNAMIC SPLIT SCREEN: Red warning failure alert on static prompt chain vs glowing green cyclic feedback graph with live state indicators."
        ),
        body_sections=[
            ScriptSection(
                section_title="The Fragility of Linear Chains",
                timestamp_estimate="0:15 - 2:30",
                spoken_dialogue="Most developers start with linear DAG pipelines: research, script, metadata. But if the research produces a weak angle or inaccurate facts, that error cascades downstream unchecked. In a production AI pipeline, you need closed-loop verification where an independent auditor checks work against a strict rubric before advancing.",
                visual_cues="Animated infographic showing cascading error propagation across nodes, followed by red barrier stop sign."
            ),
            ScriptSection(
                section_title="LangGraph State Machine Architecture",
                timestamp_estimate="2:30 - 5:00",
                spoken_dialogue="LangGraph models cyclic workflows as finite state machines. Unlike standard DAGs, LangGraph allows conditional edges to route execution backward. By defining a typed state schema containing versioned drafts and revision history, agents can consume structured critique directly from memory and apply surgical fixes.",
                visual_cues="3D interactive node diagram zooming into backward conditional edge routing from Auditor back to Script Doctor."
            ),
            ScriptSection(
                section_title="Decoupled Tri-Agent Architecture",
                timestamp_estimate="5:00 - 7:30",
                spoken_dialogue="The critical mistake most multi-agent systems make is self-evaluation redundancy: having the same writer agent revise its own text. In ContentMaker, we decouple the workflow into three distinct roles: the ScriptWriter drafts, the Auditor verifies objectively, and a dedicated Script Doctor performs surgical refactoring without author bias.",
                visual_cues="Split comparison graphic showing naive circular self-evaluation vs clean decoupled Tri-Agent separation of concerns."
            )
        ],
        cta_section=ScriptSection(
            section_title="Summary & Next Steps",
            timestamp_estimate="7:30 - 8:15",
            spoken_dialogue="You can clone the complete open-source production architecture and test suites from our GitHub repository linked in the description below. Hit subscribe for next week's deep dive into multi-agent consensus protocols.",
            visual_cues="Animated lower-third graphic with GitHub repository URL and animated subscribe bell icon."
        ),
        full_text_markdown="# Full Production Script: Building Cyclic Multi-Agent Systems with LangGraph\n\nComprehensive teleprompter script covering architecture, state schemas, and decoupled quality gating."
    )

    print("\n--- EVALUATING STRONG DRAFT 2 ---")
    eval_2 = await critic_agent.evaluate_script(brief, strong_draft, iteration=2)

    print(f"Decision: {eval_2.decision}")
    print(f"Overall Score: {eval_2.overall_score}/5.0")
    print(f"Hook Strength Score: {eval_2.rubric.hook_strength.score}/5 -> {eval_2.rubric.hook_strength.justification}")
    print(f"Summary Feedback: {eval_2.summary_feedback}")

    assert eval_2.decision == "APPROVED", "Critic MUST approve strong Draft 2"
    assert eval_2.rubric.hook_strength.score >= 4, "Hook score must be high"
    assert eval_2.overall_score >= 4.0, "Overall score must exceed threshold"

    print("\n[OK] Critic Agent 6-Dimension Rubric and explainability validated successfully!")

if __name__ == "__main__":
    asyncio.run(test_critic_scoring())
