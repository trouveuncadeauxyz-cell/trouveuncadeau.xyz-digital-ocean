"""LangChain-powered recommendation engine"""

import logging
from typing import List, Dict, Any, Optional
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """AI-powered gift recommendation engine using LangChain"""
    
    MEGA_META_PROMPT = """
You are an expert gift recommendation AI for Quebec. Analyze user input and suggest 5 perfect gift ideas.
Consider: budget, recipient age/interests, occasion, local Quebec products.
For each recommendation, provide:
1. Product name
2. Why it's perfect
3. Estimated price
4. Where to buy (prefer local Quebec retailers)
5. Amazon link (if available)

Respond in JSON format with array of recommendations.
"""
    
    def __init__(
        self,
        openai_api_key: str,
        anthropic_api_key: Optional[str] = None,
        model: str = "openai"  # "openai" or "anthropic"
    ):
        self.model_type = model
        self.openai_api_key = openai_api_key
        self.anthropic_api_key = anthropic_api_key
        
        if model == "openai":
            self.llm = ChatOpenAI(
                api_key=openai_api_key,
                model="gpt-4",
                temperature=0.7
            )
        elif model == "anthropic":
            self.llm = ChatAnthropic(
                api_key=anthropic_api_key,
                model="claude-3-sonnet-20240229"
            )
    
    async def generate_recommendations(
        self,
        user_input: str,
        products: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate gift recommendations based on user input"""
        try:
            product_context = self._format_products(products)
            
            prompt = f"""{self.MEGA_META_PROMPT}

Available products in our database:
{product_context}

User request: {user_input}

Provide 5 personalized recommendations."""
            
            messages = [
                SystemMessage(content=self.MEGA_META_PROMPT),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            logger.info(f"Generated recommendations for: {user_input}")
            
            return {
                "status": "success",
                "recommendations": response.content,
                "model": self.model_type
            }
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def _format_products(self, products: List[Dict[str, Any]]) -> str:
        """Format products for context injection"""
        formatted = []
        for p in products[:10]:  # Limit to 10 products for context
            formatted.append(
                f"- {p.get('Name', 'Unknown')}: {p.get('Description', '')} "
                f"(Price: ${p.get('Price', 'N/A')}, Category: {p.get('Category', 'N/A')})"
            )
        return "\n".join(formatted)
