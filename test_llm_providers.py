"""
Test script for Multi-LLM Provider system.
Tests Gemini, OpenAI, and Anthropic with automatic fallback.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import os
from app.services.llm_providers import LLMProvider, LLMError


def test_llm_providers():
    """Test all configured LLM providers."""
    print("=" * 80)
    print("MULTI-LLM PROVIDER TEST")
    print("=" * 80)

    # Check which API keys are configured
    print("\n📋 Configuration Check:")
    print(f"   Gemini API Key:      {'✓ Set' if os.getenv('GEMINI_API_KEY', '').startswith('AIza') else '✗ Not set'}")
    print(f"   OpenAI API Key:      {'✓ Set' if os.getenv('OPENAI_API_KEY', '').startswith('sk-') else '✗ Not set'}")
    print(f"   Anthropic API Key:   {'✓ Set' if os.getenv('ANTHROPIC_API_KEY', '').startswith('sk-ant-') else '✗ Not set'}")

    print("\n" + "=" * 80)
    print("INITIALIZING LLM PROVIDER")
    print("=" * 80)

    try:
        provider = LLMProvider()
        active_providers = provider.get_active_providers()

        print(f"\n✅ LLM Provider initialized successfully!")
        print(f"   Active providers: {len(active_providers)}")
        for i, name in enumerate(active_providers, 1):
            print(f"   {i}. {name}")

    except LLMError as e:
        print(f"\n❌ FAILED to initialize LLM provider:")
        print(f"   {str(e)}")
        print("\n💡 Solution:")
        print("   Add at least ONE API key to your .env file:")
        print("   • GEMINI_API_KEY=AIza...  (RECOMMENDED - Free tier available)")
        print("   • OPENAI_API_KEY=sk-...")
        print("   • ANTHROPIC_API_KEY=sk-ant-...")
        return

    # Test with a simple prompt
    print("\n" + "=" * 80)
    print("TESTING TEXT GENERATION")
    print("=" * 80)

    system_prompt = "You are a helpful financial analyst."
    user_prompt = "In one sentence, what is the price-to-earnings ratio (P/E ratio)?"

    print(f"\nTest prompt: '{user_prompt}'")
    print("\nGenerating response...")

    try:
        response = provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
            max_tokens=100
        )

        print("\n✅ SUCCESS! Generated response:")
        print("=" * 80)
        print(response)
        print("=" * 80)

    except LLMError as e:
        print(f"\n❌ FAILED: {str(e)}")

    print("\n" + "=" * 80)
    print("PROVIDER PRIORITY & FALLBACK")
    print("=" * 80)
    print("""
The system tries providers in this order:

1. Google Gemini (if configured)
   → Fastest response time
   → Most cost-effective
   → Free tier: 60 requests/minute

2. OpenAI GPT-4 (if configured)
   → Highest quality analysis
   → Best for complex financial reasoning
   → Pay-per-use

3. Anthropic Claude (if configured)
   → Alternative high-quality option
   → Good for long-form analysis

If one fails, the next is automatically tried!
    """)

    print("=" * 80)
    print("COST COMPARISON")
    print("=" * 80)
    print("""
Typical cost per 1000 advisor reports:

Gemini 2.0 Flash:      ~$1.50   (CHEAPEST)
  → Input:  $0.15 / 1M tokens
  → Output: $0.60 / 1M tokens

OpenAI GPT-4o:         ~$7.50
  → Input:  $2.50 / 1M tokens
  → Output: $10.00 / 1M tokens

Claude 3.5 Sonnet:     ~$9.00
  → Input:  $3.00 / 1M tokens
  → Output: $15.00 / 1M tokens

RECOMMENDATION: Use Gemini for production (5x cheaper!)
    """)

    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)

    if not os.getenv('GEMINI_API_KEY', '').startswith('AIza'):
        print("""
📌 RECOMMENDED: Get a free Gemini API key

1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API key"
3. Add to .env:
   GEMINI_API_KEY=AIzaSy...your_key_here

Benefits:
  ✓ FREE tier (60 requests/minute)
  ✓ 5x cheaper than OpenAI for production
  ✓ Very fast response times
  ✓ High quality for financial analysis
        """)
    else:
        print("""
✅ You're all set!

The system will automatically:
  • Use Gemini first (fastest, cheapest)
  • Fall back to OpenAI if Gemini fails
  • Fall back to Anthropic if both fail

Test it:
  python3 demo_advisor_complete.py
        """)

    print("=" * 80)


if __name__ == "__main__":
    test_llm_providers()
