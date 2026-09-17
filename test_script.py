import asyncio
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from backend.agents.research import ResearchAgent
from backend.agents.script import ScriptAgent

async def test_script_generation():
    print("=" * 70)
    print("TESTING SCRIPT AGENT CONSUMING RESEARCH BRIEF")
    print("=" * 70)

    research_agent = ResearchAgent()
    script_agent = ScriptAgent()

    topic = "Building Cyclic Multi-Agent Systems with LangGraph"
    print(f"\n1. Generating Research Brief for: '{topic}'...")
    brief = await research_agent.run(topic)
    print(f" -> Brief ready: {brief.core_thesis[:60]}...")

    print(f"\n2. Running ScriptAgent to produce full draft...")
    draft = await script_agent.run(brief, duration_target="8-10 mins", tone="authoritative, dynamic")

    # Assertions
    assert draft.version == 1
    assert draft.hook_segment is not None
    assert len(draft.hook_segment.spoken_dialogue) > 20
    assert len(draft.hook_segment.visual_cues) > 10
    assert len(draft.body_sections) >= 2
    assert draft.cta_section is not None
    assert len(draft.full_text_markdown) > 100

    print("\n--- SCRIPT DRAFT v1 VERIFICATION ---")
    print(f"Version: v{draft.version}")
    print(f"Hook Title: {draft.hook_segment.section_title}")
    print(f"Hook Dialogue: \"{draft.hook_segment.spoken_dialogue[:120]}...\"")
    print(f"Hook Visual Cue: \"{draft.hook_segment.visual_cues}\"")
    print(f"Total Body Sections: {len(draft.body_sections)}")
    for i, s in enumerate(draft.body_sections, 1):
        print(f"   [{i}] {s.section_title} ({s.timestamp_estimate})")
    print(f"CTA Section: {draft.cta_section.section_title}")
    print(f"Markdown Script Length: {len(draft.full_text_markdown)} chars")
    print("\n[OK] Script Agent successfully generated a complete, high-retention script!")

if __name__ == "__main__":
    asyncio.run(test_script_generation())
