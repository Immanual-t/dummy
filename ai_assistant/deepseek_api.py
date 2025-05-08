import os
import json
import logging
from typing import List, Dict, Any, Optional

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Create client with the DeepSeek API setup via OpenRouter
from openai import OpenAI

# Set up logging
logger = logging.getLogger(__name__)


class DeepSeekClient:
    """Client for DeepSeek Prover V2 API via OpenRouter"""

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://openrouter.ai/api/v1"):
        """Initialize the DeepSeek client

        Args:
            api_key: OpenRouter API key (defaults to environment variable)
            base_url: OpenRouter base URL
        """
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OpenRouter API key is required. Set OPENROUTER_API_KEY environment variable.")

        print("DEBUG: OPENROUTER_API_KEY =", self.api_key)  # Optional: For debug purposes only

        self.client = OpenAI(
            base_url=base_url,
            api_key=self.api_key,
        )
        self.model = "deepseek/deepseek-prover-v2:free"

    def generate_completion(
            self,
            messages: List[Dict[str, str]],
            max_tokens: int = 500,
            temperature: float = 0.7,
            site_url: str = "https://finarva-ai.example.com",
            site_name: str = "FinArva AI"
    ) -> str:
        """Generate completion using DeepSeek Prover V2

        Args:
            messages: List of message dictionaries with role and content
            max_tokens: Maximum tokens for response
            temperature: Temperature for response generation
            site_url: Site URL for OpenRouter analytics
            site_name: Site name for OpenRouter analytics

        Returns:
            str: Generated response text
        """
        try:
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": site_url,
                    "X-Title": site_name,
                },
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )

            return completion.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Error generating DeepSeek completion: {str(e)}")
            return f"I'm sorry, I encountered an issue: {str(e)}"