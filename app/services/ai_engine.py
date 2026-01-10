"""
AI Engine Service
Generates investment reports using LLM (Multi-provider support).
"""
import os
import json
from typing import Dict, Any, Optional
from app.services.llm_providers import get_llm_provider, LLMError


# System prompt for the AI analyst
SYSTEM_PROMPT = """You are a Senior Equity Analyst at a prestigious investment firm with 15+ years of experience in fundamental analysis and equity research.

IMPORTANT: You MUST write ALL reports in GERMAN language. Use professional German financial terminology.

Your role is to provide professional, critical, and data-driven investment analysis. Your tone must be:
- Professional and objective
- Analytical and evidence-based
- Critical where warranted (identify both opportunities and risks)
- Direct and concise
- Free from promotional language or unfounded optimism

You analyze companies through multiple lenses:
1. Fundamental valuation (P/E, P/B, margins, growth rates)
2. Financial health (balance sheet strength, debt levels, cash flow)
3. Competitive positioning and industry dynamics
4. Risk factors and potential challenges
5. Market sentiment and recent developments

Your reports must be structured, well-reasoned, and useful for institutional investors making allocation decisions. Remember: Write everything in German."""


# User prompt template
USER_PROMPT_TEMPLATE = """Generate a comprehensive investment report for the following security:

**Ticker:** {ticker}
**Company Name:** {name}
**Sector:** {sector}
**Industry:** {industry}

## Market Data
- Current Price: {current_price} {currency}
- Market Cap: {market_cap}
- P/E Ratio (Trailing): {pe_ratio}
- Forward P/E: {forward_pe}
- Dividend Yield: {dividend_yield}
- Beta: {beta}
- 52-Week Range: {week_low} - {week_high}

## Financial Metrics
- Profit Margins: {profit_margins}
- Revenue Growth: {revenue_growth}
- Return on Equity: {roe}
- Debt to Equity: {debt_to_equity}

## Income Statement (Latest Period: {financials_period})
- Total Revenue: {total_revenue}
- Gross Profit: {gross_profit}
- Operating Income: {operating_income}
- Net Income: {net_income}
- EBITDA: {ebitda}

## Balance Sheet (Latest Period: {balance_sheet_period})
- Total Assets: {total_assets}
- Total Liabilities: {total_liabilities}
- Stockholder Equity: {stockholder_equity}
- Total Debt: {total_debt}
- Cash and Equivalents: {cash}

## Recent News
{news_section}

---

Please generate a professional investment report in **Markdown format** with the following structure:

# Investment Analysis: {name} ({ticker})

## Executive Summary
A concise 3-4 sentence overview covering: current valuation assessment, key investment thesis, and overall recommendation direction.

## Company Overview
Brief description of the business, sector positioning, and competitive landscape.

## Fundamental Analysis

### Valuation Metrics
Analysis of P/E ratio, market cap, and relative valuation compared to sector/peers.

### Financial Health
Assessment of balance sheet strength, debt levels, liquidity, and financial stability.

### Profitability & Growth
Analysis of margins, revenue growth, ROE, and earnings trajectory.

## Investment Thesis

### Bull Case
3-5 key positive factors and growth catalysts. Be specific and data-driven.

### Bear Case
3-5 key risks, challenges, and potential headwinds. Be critical and realistic.

## Recent Developments
Analysis of recent news and its potential impact on the investment case.

## Conclusion
Final assessment synthesizing the analysis. Include a directional view (e.g., "Attractive for long-term growth investors" or "Overvalued at current levels").

## 🎯 Recommendation

End with a clear, actionable recommendation box:
- **Rating:** One of: STRONG BUY | BUY | HOLD | SELL | STRONG SELL
- **Action:** What should the investor do right now? (e.g., "Accumulate on dips below $X", "Wait for better entry", "Take profits", "Avoid")
- **Target Price:** If possible, suggest a fair value or target price range based on valuation metrics
- **Risk Level:** LOW | MEDIUM | HIGH | VERY HIGH

---

**Important Instructions:**
- Use actual data from above; if data is "N/A", acknowledge the limitation
- Be critical and balanced; avoid promotional language
- Format all numbers clearly (use M for millions, B for billions)
- Keep the report to 600-800 words
- Use professional financial analysis terminology
- Provide specific, actionable insights
- The final recommendation MUST be clear and decisive"""


def generate_investment_report(ticker: str, data: Dict[str, Any], api_key: Optional[str] = None) -> str:
    """
    Generate an investment report using AI based on market data.

    Uses multi-LLM provider with automatic fallback:
    - Google Gemini (if configured)
    - OpenAI GPT-4 (if configured)
    - Anthropic Claude (if configured)

    Args:
        ticker: Stock ticker symbol
        data: Dictionary containing market data from data_fetcher
        api_key: Deprecated - API keys now read from environment

    Returns:
        Markdown-formatted investment report
    """
    # Get LLM provider (with automatic fallback)
    try:
        llm_provider = get_llm_provider()
    except LLMError as e:
        raise ValueError(str(e))

    # Extract and format data for the prompt
    basic_info = data.get("basic_info", {})
    financials = data.get("financials", {})
    balance_sheet = data.get("balance_sheet", {})
    news = data.get("news", [])

    # Format news section
    news_section = _format_news_section(news)

    # Format numbers for better readability
    def format_num(val):
        if val == "N/A" or val is None:
            return "N/A"
        try:
            num = float(val)
            if num >= 1_000_000_000_000:
                return f"${num / 1_000_000_000_000:.2f}T"
            elif num >= 1_000_000_000:
                return f"${num / 1_000_000_000:.2f}B"
            elif num >= 1_000_000:
                return f"${num / 1_000_000:.2f}M"
            else:
                return f"${num:,.2f}"
        except (ValueError, TypeError):
            return str(val)

    def format_pct(val):
        if val == "N/A" or val is None:
            return "N/A"
        try:
            return f"{float(val) * 100:.2f}%"
        except (ValueError, TypeError):
            return str(val)

    # Build the user prompt with actual data
    user_prompt = USER_PROMPT_TEMPLATE.format(
        ticker=ticker,
        name=basic_info.get("name", "N/A"),
        sector=basic_info.get("sector", "N/A"),
        industry=basic_info.get("industry", "N/A"),
        current_price=basic_info.get("current_price", "N/A"),
        currency=basic_info.get("currency", "USD"),
        market_cap=format_num(basic_info.get("market_cap")),
        pe_ratio=basic_info.get("pe_ratio", "N/A"),
        forward_pe=basic_info.get("forward_pe", "N/A"),
        dividend_yield=format_pct(basic_info.get("dividend_yield")),
        beta=basic_info.get("beta", "N/A"),
        week_low=basic_info.get("52_week_low", "N/A"),
        week_high=basic_info.get("52_week_high", "N/A"),
        profit_margins=format_pct(basic_info.get("profit_margins")),
        revenue_growth=format_pct(basic_info.get("revenue_growth")),
        roe=format_pct(basic_info.get("return_on_equity")),
        debt_to_equity=basic_info.get("debt_to_equity", "N/A"),
        financials_period=financials.get("period_end", "N/A"),
        total_revenue=format_num(financials.get("total_revenue")),
        gross_profit=format_num(financials.get("gross_profit")),
        operating_income=format_num(financials.get("operating_income")),
        net_income=format_num(financials.get("net_income")),
        ebitda=format_num(financials.get("ebitda")),
        balance_sheet_period=balance_sheet.get("period_end", "N/A"),
        total_assets=format_num(balance_sheet.get("total_assets")),
        total_liabilities=format_num(balance_sheet.get("total_liabilities")),
        stockholder_equity=format_num(balance_sheet.get("stockholder_equity")),
        total_debt=format_num(balance_sheet.get("total_debt")),
        cash=format_num(balance_sheet.get("cash_and_equivalents")),
        news_section=news_section
    )

    try:
        # Generate report using multi-LLM provider with automatic fallback
        report = llm_provider.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.7,
            max_tokens=4000
        )

        return report

    except LLMError as e:
        raise RuntimeError(f"Error generating report with AI: {str(e)}")


def _format_news_section(news: list) -> str:
    """Format news items for the prompt."""
    if not news or (len(news) == 1 and "error" in news[0]):
        return "No recent news available."

    news_lines = []
    for idx, item in enumerate(news, 1):
        if "error" in item:
            continue
        title = item.get("title", "N/A")
        publisher = item.get("publisher", "N/A")
        published = item.get("published", "N/A")
        news_lines.append(f"{idx}. **{title}** ({publisher}, {published})")

    return "\n".join(news_lines) if news_lines else "No recent news available."


# Optional: Import type hint
from typing import Optional
