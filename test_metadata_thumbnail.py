import asyncio
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from backend.agents.research import ResearchAgent
from backend.agents.script import ScriptAgent
from backend.agents.metadata import SEOAgent
from backend.agents.thumbnail import ThumbnailAgent

async def test_metadata_and_thumbnails():
    print("=" * 70)
    print("TESTING SEO/METADATA AGENT AND THUMBNAIL CONCEPT AGENT")
    print("=" * 70)

    research_agent = ResearchAgent()
    script_agent = ScriptAgent()
    seo_agent = SEOAgent()
    thumb_agent = ThumbnailAgent()

    topic = "Building Cyclic Multi-Agent Systems with LangGraph"
    print(f"\n1. Preparing Brief and Script for: '{topic}'...")
    brief = await research_agent.run(topic)
    script = await script_agent.run(brief)

    print("\n2. Executing SEOAgent...")
    metadata = await seo_agent.run(brief, script)
    
    assert metadata.version == 1
    assert len(metadata.primary_title) > 10
    assert len(metadata.alternative_titles) >= 2
    assert len(metadata.description) > 50
    assert len(metadata.tags) >= 5
    assert len(metadata.chapters) >= 3

    print(" -> Primary Title:", metadata.primary_title)
    print(" -> Alternative Titles:", metadata.alternative_titles)
    print(" -> Chapters:", len(metadata.chapters))
    print(" -> Tags:", metadata.tags[:5])

    print("\n3. Executing ThumbnailAgent...")
    thumbnails = await thumb_agent.run(brief, script)

    assert thumbnails.version == 1
    assert len(thumbnails.concepts) >= 2
    assert thumbnails.recommended_concept_id in [c.concept_id for c in thumbnails.concepts]

    for c in thumbnails.concepts:
        print(f" -> Concept #{c.concept_id} [{c.title_concept}]: Text='{c.text_overlay}' | Trigger='{c.emotional_trigger}'")

    print("\n[OK] Both SEOAgent and ThumbnailAgent successfully validated!")

if __name__ == "__main__":
    asyncio.run(test_metadata_and_thumbnails())
