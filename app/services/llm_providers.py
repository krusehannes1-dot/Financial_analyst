"""
Multi-LLM Provider
Supports OpenAI, Google Gemini, and Anthropic with automatic fallback.
"""
import os
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class LLMError(Exception):
    """Raised when LLM generation fails."""
    pass


class OpenAIProvider:
    """OpenAI GPT-4 provider."""

    def __init__(self, api_key: Optional[str] = None):
        self.name = "OpenAI GPT-4"
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise LLMError("OpenAI API key not configured")

        from openai import OpenAI
        self.client = OpenAI(api_key=self.api_key)

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.5, max_tokens: int = 3000) -> str:
        """Generate text using OpenAI GPT-4."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"OpenAI error: {str(e)}")
            raise LLMError(f"OpenAI failed: {str(e)}")


class GeminiProvider:
    """Google Gemini provider."""

    def __init__(self, api_key: Optional[str] = None):
        self.name = "Google Gemini"
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise LLMError("Gemini API key not configured")

        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.client = genai
        except ImportError:
            raise LLMError("google-generativeai package not installed. Run: pip install google-generativeai")

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.5, max_tokens: int = 3000) -> str:
        """Generate text using Google Gemini."""
        try:
            # Gemini 2.0 Flash (latest, fastest)
            # Gemini 1.5 Pro also available for more complex tasks
            model = self.client.GenerativeModel(
                model_name='gemini-flash-latest',
                system_instruction=system_prompt
            )

            generation_config = {
                'temperature': temperature,
                'max_output_tokens': max_tokens,
            }

            response = model.generate_content(
                user_prompt,
                generation_config=generation_config
            )

            return response.text

        except Exception as e:
            logger.error(f"Gemini error: {str(e)}")
            raise LLMError(f"Gemini failed: {str(e)}")


class AnthropicProvider:
    """Anthropic Claude provider."""

    def __init__(self, api_key: Optional[str] = None):
        self.name = "Anthropic Claude"
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")

        if not self.api_key:
            raise LLMError("Anthropic API key not configured")

        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
        except ImportError:
            raise LLMError("anthropic package not installed. Run: pip install anthropic")

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.5, max_tokens: int = 3000) -> str:
        """Generate text using Anthropic Claude."""
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Anthropic error: {str(e)}")
            raise LLMError(f"Anthropic failed: {str(e)}")


class LLMProvider:
    """
    Multi-LLM provider with automatic fallback.

    Tries providers in order:
    1. Google Gemini (if configured) - Fast and cost-effective
    2. OpenAI GPT-4 (if configured) - High quality
    3. Anthropic Claude (if configured) - Alternative
    """

    def __init__(self):
        self.providers = []

        # Try to initialize all available providers
        # Order: Gemini (fastest/cheapest) → OpenAI → Anthropic

        # Gemini (prioritized for speed and cost)
        try:
            if os.getenv("GEMINI_API_KEY"):
                self.providers.append(GeminiProvider())
                logger.info("✓ Gemini provider initialized")
        except LLMError as e:
            logger.warning(f"Gemini initialization failed: {str(e)}")

        # OpenAI
        try:
            if os.getenv("OPENAI_API_KEY"):
                self.providers.append(OpenAIProvider())
                logger.info("✓ OpenAI provider initialized")
        except LLMError as e:
            logger.warning(f"OpenAI initialization failed: {str(e)}")

        # Anthropic
        try:
            if os.getenv("ANTHROPIC_API_KEY"):
                self.providers.append(AnthropicProvider())
                logger.info("✓ Anthropic provider initialized")
        except LLMError as e:
            logger.warning(f"Anthropic initialization failed: {str(e)}")

        if not self.providers:
            raise LLMError(
                "No LLM providers configured. Set at least one API key:\n"
                "  - GEMINI_API_KEY (recommended, fast & cheap)\n"
                "  - OPENAI_API_KEY\n"
                "  - ANTHROPIC_API_KEY"
            )

        logger.info(f"Initialized LLM system with {len(self.providers)} provider(s)")

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.5, max_tokens: int = 3000) -> str:
        """
        Generate text with automatic fallback.

        Args:
            system_prompt: System instructions for the LLM
            user_prompt: User query/prompt
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text

        Raises:
            LLMError: If all providers fail
        """
        last_error = None

        for provider in self.providers:
            try:
                logger.info(f"Trying {provider.name}")
                result = provider.generate(system_prompt, user_prompt, temperature, max_tokens)
                logger.info(f"✓ {provider.name} succeeded")
                return result

            except LLMError as e:
                logger.warning(f"✗ {provider.name} failed: {str(e)}")
                last_error = e
                continue

        # All providers failed
        error_msg = f"All LLM providers failed. Last error: {str(last_error)}"
        logger.error(error_msg)
        raise LLMError(error_msg)

    def get_active_providers(self) -> list:
        """Get list of active provider names."""
        return [p.name for p in self.providers]


# Global instance
_llm_provider = None


def get_llm_provider() -> LLMProvider:
    """Get or create the global LLM provider instance."""
    global _llm_provider
    if _llm_provider is None:
        _llm_provider = LLMProvider()
    return _llm_provider
