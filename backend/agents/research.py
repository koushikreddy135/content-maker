import logging
from typing import Dict, Any
from backend.models.schemas import ResearchBrief
from backend.services.search import SearchService
from backend.services.llm import LLMService

logger = logging.getLogger(__name__)

RESEARCH_SYSTEM_PROMPT = """You are an elite YouTube Content Strategist and Research Agent for high-performing educational and tech YouTube channels.
Your mission is to turn a raw topic into an authoritative, actionable, and differentiated Research Brief.

You must:
1. Identify the exact target viewer persona, their knowledge level, and specific pain points.
2. Formulate a strong, counter-intuitive, or high-value Core Thesis (the big takeaway).
3. Extract 4-5 structured key points with concrete technical or practical depth.
4. Craft 2-3 curiosity-driven hook angles designed to stop the scroll in the first 15 seconds.
5. Provide a rigorous Competitive Angle: Analyze how existing YouTube videos cover this topic (often superficial or boring) and define our specific differentiation angle.
6. Identify primary and secondary search keywords.
7. Include verified sources or references.

Return ONLY a structured JSON object matching the ResearchBrief schema."""

class ResearchAgent:
    def __init__(self):
        self.search_service = SearchService()

    async def run(self, topic: str, extra_context: str = "") -> ResearchBrief:
        """
        Executes live web search on topic, then synthesizes into a structured ResearchBrief.
        """
        logger.info(f"ResearchAgent starting research on topic: '{topic}'")
        
        # 1. Gather live search context
        search_queries = [
            f"{topic} youtube tutorial trends",
            f"{topic} key architecture concepts comparison",
            f"{topic} common mistakes"
        ]
        
        gathered_results = []
        for q in search_queries[:2]:
            results = await self.search_service.search(q, max_results=3)
            gathered_results.extend(results)

        search_context_text = "\n\n".join([
            f"Source Title: {r.get('title')}\nURL: {r.get('url')}\nSummary: {r.get('snippet')}"
            for r in gathered_results
        ])

        # 2. Build synthesis prompt
        prompt = f"""Topic: {topic}
Extra Context: {extra_context if extra_context else 'None provided'}

REAL-TIME WEB SEARCH CONTEXT:
{search_context_text}

Analyze the topic and current search landscape. Produce a high-depth, differentiated ResearchBrief."""

        # 3. Call LLM for structured output
        brief = await LLMService.generate_structured(
            prompt=prompt,
            system_prompt=RESEARCH_SYSTEM_PROMPT,
            response_model=ResearchBrief,
            temperature=0.4
        )
        
        # Ensure topic is set properly
        brief.topic = topic
        logger.info(f"ResearchAgent successfully produced brief for '{topic}' with {len(brief.key_points)} key points.")
        return brief
