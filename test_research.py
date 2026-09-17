import asyncio
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from backend.agents.research import ResearchAgent

async def test_research_topics():
    agent = ResearchAgent()
    topics = [
        "Building Cyclic Multi-Agent Systems with LangGraph",
        "How to Optimize Next.js App Router for Sub-Second Load Times",
        "DeepSeek-R1 vs OpenAI o1: The Open Weights Reasoning Revolution"
    ]

    print("=" * 70)
    print("TESTING RESEARCH AGENT ACROSS 3 DIVERSE TOPICS")
    print("=" * 70)

    for i, topic in enumerate(topics, 1):
        print(f"\n[{i}/3] Running Research on: '{topic}'...")
        brief = await agent.run(topic)
        
        assert brief.topic == topic
        assert len(brief.target_audience) > 10, "Target audience must be detailed"
        assert len(brief.key_points) >= 3, "Must have at least 3 structured points"
        assert len(brief.hook_angles) >= 2, "Must have at least 2 hook angles"
        assert brief.competitive_angle.differentiation_hook, "Must have differentiation angle"
        assert len(brief.target_keywords) >= 3, "Must have target keywords"

        print(f" -> Target Audience: {brief.target_audience[:80]}...")
        print(f" -> Core Thesis: {brief.core_thesis}")
        print(f" -> Key Points: {len(brief.key_points)} points gathered")
        for kp in brief.key_points[:2]:
            print(f"    * {kp}")
        print(f" -> Hook Angle #1: {brief.hook_angles[0]}")
        print(f" -> Differentiation: {brief.competitive_angle.differentiation_hook}")
        print(f" -> Target Keywords: {', '.join(brief.target_keywords[:4])}")
        print(f" -> Sources: {len(brief.sources_cited)} sources cited")
        print(" [OK] Brief is complete, structured, and verified.")

    print("\n" + "=" * 70)
    print("ALL 3 RESEARCH AGENT TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_research_topics())
