"""
Claude LLM integration supporting both Anthropic API and Claude Code CLI.

This module provides a unified interface to Claude that automatically routes to either:
1. Anthropic API (when ANTHROPIC_API_KEY is a real API key)
2. Claude Code CLI (when ANTHROPIC_API_KEY is set to all 9s)

The routing is handled by the anthropic_router library.
"""

import os
from typing import Any, Dict, List, Optional, Union
import json
import logging

try:
    from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False
    print("Warning: anthropic package not installed. Install with: pip install anthropic")

logger = logging.getLogger(__name__)


class ClaudeClient:
    """
    Unified Claude client supporting both API and CLI modes.

    Automatically detects mode based on API key:
    - API mode: API key starts with 'sk-ant-'
    - CLI mode: API key is all 9s (routes to Claude Code CLI)

    Example:
        ```python
        # API mode
        os.environ['ANTHROPIC_API_KEY'] = 'sk-ant-...'
        client = ClaudeClient()

        # CLI mode (uses Claude Code Max)
        os.environ['ANTHROPIC_API_KEY'] = '999999999...'
        client = ClaudeClient()
        ```
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ):
        """
        Initialize Claude client.

        Args:
            api_key: Anthropic API key or '999...' for CLI mode.
                     If None, reads from ANTHROPIC_API_KEY env var.
            model: Claude model to use (API mode only)
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0.0-1.0)
        """
        if not HAS_ANTHROPIC:
            raise ImportError(
                "anthropic package is required. Install with: pip install anthropic\n"
                "For CLI routing support: pip install git+https://github.com/jimmc414/claude_n_codex_api_proxy.git"
            )

        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable not set. "
                "Set to your API key or '999999999999999999999999999999999999999999999999' for CLI mode."
            )

        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

        # Detect mode
        self.is_cli_mode = self.api_key.replace('9', '') == ''

        # Initialize Anthropic client (will auto-route based on API key)
        try:
            self.client = Anthropic(api_key=self.api_key)
            logger.info(f"Claude client initialized in {'CLI' if self.is_cli_mode else 'API'} mode")
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {e}")
            raise

        # Usage statistics
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_requests = 0

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        stop_sequences: Optional[List[str]] = None,
    ) -> str:
        """
        Generate text from Claude.

        Args:
            prompt: The user prompt/question
            system: Optional system prompt for instructions
            max_tokens: Override default max_tokens
            temperature: Override default temperature
            stop_sequences: Optional list of stop sequences

        Returns:
            str: Generated text from Claude

        Example:
            ```python
            client = ClaudeClient()
            response = client.generate(
                prompt="Explain quantum entanglement",
                system="You are a physics professor"
            )
            print(response)
            ```
        """
        try:
            # Build message
            messages = [{"role": "user", "content": prompt}]

            # Call Claude API (auto-routes to CLI if API key is all 9s)
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature or self.temperature,
                system=system or "",
                messages=messages,
                stop_sequences=stop_sequences or [],
            )

            # Update statistics
            self.total_requests += 1
            if hasattr(response, 'usage'):
                self.total_input_tokens += response.usage.input_tokens
                self.total_output_tokens += response.usage.output_tokens

            # Extract text
            text = response.content[0].text

            logger.debug(f"Generated {len(text)} characters from Claude")
            return text

        except Exception as e:
            logger.error(f"Claude generation failed: {e}")
            raise

    def generate_with_messages(
        self,
        messages: List[Dict[str, str]],
        system: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """
        Generate text using multi-turn conversation format.

        Args:
            messages: List of message dicts with 'role' and 'content'
                     Example: [{"role": "user", "content": "Hello"}]
            system: Optional system prompt
            max_tokens: Override default max_tokens
            temperature: Override default temperature

        Returns:
            str: Generated text from Claude
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature or self.temperature,
                system=system or "",
                messages=messages,
            )

            # Update statistics
            self.total_requests += 1
            if hasattr(response, 'usage'):
                self.total_input_tokens += response.usage.input_tokens
                self.total_output_tokens += response.usage.output_tokens

            return response.content[0].text

        except Exception as e:
            logger.error(f"Claude multi-turn generation failed: {e}")
            raise

    def generate_structured(
        self,
        prompt: str,
        output_schema: Dict[str, Any],
        system: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate structured output (JSON) from Claude.

        Args:
            prompt: The user prompt
            output_schema: JSON schema describing expected output structure
            system: Optional system prompt

        Returns:
            dict: Parsed JSON response

        Example:
            ```python
            schema = {
                "type": "object",
                "properties": {
                    "hypothesis": {"type": "string"},
                    "confidence": {"type": "number"}
                }
            }
            result = client.generate_structured(
                prompt="Generate a hypothesis about dark matter",
                output_schema=schema
            )
            ```
        """
        # Add JSON instruction to system prompt
        json_system = (system or "") + "\n\nYou must respond with valid JSON matching this schema:\n" + json.dumps(output_schema, indent=2)

        response_text = self.generate(
            prompt=prompt,
            system=json_system,
        )

        # Parse JSON
        try:
            # Try to extract JSON from markdown code blocks if present
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()

            return json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from Claude response: {e}")
            logger.error(f"Response text: {response_text[:500]}")
            raise ValueError(f"Claude did not return valid JSON: {e}")

    def get_usage_stats(self) -> Dict[str, int]:
        """
        Get usage statistics.

        Returns:
            dict: Statistics including total requests, input tokens, output tokens
        """
        return {
            "total_requests": self.total_requests,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "estimated_cost_usd": self._estimate_cost(),
        }

    def _estimate_cost(self) -> float:
        """
        Estimate API cost (only relevant for API mode, CLI is unlimited).

        Returns:
            float: Estimated cost in USD
        """
        if self.is_cli_mode:
            return 0.0  # CLI mode has no per-token cost

        # Pricing for Claude 3.5 Sonnet (as of Nov 2025)
        # Input: $3 per million tokens
        # Output: $15 per million tokens
        input_cost = (self.total_input_tokens / 1_000_000) * 3.0
        output_cost = (self.total_output_tokens / 1_000_000) * 15.0

        return input_cost + output_cost

    def reset_stats(self):
        """Reset usage statistics."""
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_requests = 0


# Singleton instance for convenience
_default_client: Optional[ClaudeClient] = None


def get_client(reset: bool = False) -> ClaudeClient:
    """
    Get or create default Claude client singleton.

    Args:
        reset: If True, create a new client instance

    Returns:
        ClaudeClient: Default client instance
    """
    global _default_client
    if _default_client is None or reset:
        _default_client = ClaudeClient()
    return _default_client
