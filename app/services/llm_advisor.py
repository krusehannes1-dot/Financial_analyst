"""
LLM Advisor Engine
Generates actionable trading advice based on technical and fundamental analysis.
"""
import os
from typing import Dict, Any, Optional
from app.services.llm_providers import get_llm_provider, LLMError


# System prompt for the Chief Investment Advisor
ADVISOR_SYSTEM_PROMPT = """You are the Chief Investment Advisor at Kruse Capital, a quantitative hedge fund.

Your expertise combines:
- Deep technical analysis (RSI, MACD, Moving Averages, Support/Resistance)
- Fundamental valuation (P/E ratios, PEG, Debt levels)
- Risk management (Stop-loss placement, position sizing)
- Wall Street consensus interpretation

Your communication style:
- PRECISE: No vague statements like "could be interesting"
- RISK-AWARE: Always highlight downside scenarios
- ACTION-ORIENTED: Every analysis must end with a clear action
- HONEST: If data is insufficient or conflicting, say so

Critical Rules:
1. If RSI > 70, NEVER recommend immediate market buy - wait for pullback
2. If RSI < 30 and trend is down, warn about "falling knife" risk
3. Stop-loss must always be set 3-5% below recent support
4. If Wall Street consensus conflicts with technicals, explain the divergence
5. No position should be taken without a clear entry zone and exit plan

You hate:
- Generic phrases like "do your own research"
- Analyses without specific price levels
- Recommendations without risk management

You must always provide specific numbers: entry prices, target prices, stop-losses."""


# User prompt template with structured data
ADVISOR_USER_PROMPT_TEMPLATE = """Analyze the following security and provide an actionable trading recommendation.

TICKER: {ticker}
COMPANY: {name}
SECTOR: {sector}

=== CURRENT MARKET DATA ===
Current Price: {current_price:.2f} {currency}
1-Day Change: {price_change_1d:.2f}%
5-Day Change: {price_change_5d:.2f}%
1-Month Change: {price_change_1m:.2f}%
Volume Ratio: {volume_ratio:.2f}x (current vs 30-day avg)

=== TECHNICAL INDICATORS ===
RSI(14): {rsi:.2f}
  Status: {rsi_status}

Trend: {trend}
SMA 50: {sma_50:.2f}
SMA 200: {sma_200:.2f}
Price vs SMA50: {price_vs_sma50:+.2f}%
Price vs SMA200: {price_vs_sma200:+.2f}%

MACD: {macd:.4f}
MACD Signal: {macd_signal:.4f}
MACD Histogram: {macd_histogram:.4f}
MACD Status: {macd_status}

Bollinger Bands:
- Upper: {bb_upper:.2f}
- Middle: {bb_middle:.2f}
- Lower: {bb_lower:.2f}
- Position: {bb_position}

=== SUPPORT & RESISTANCE (Critical Price Zones) ===
Support Level (90d low): {support_level:.2f}
Resistance Level (90d high): {resistance_level:.2f}
Pivot Point: {pivot_point:.2f}
S1: {support_1:.2f}
R1: {resistance_1:.2f}

Distance to Support: {distance_to_support:.2f}%
Distance to Resistance: {distance_to_resistance:.2f}%

=== WALL STREET CONSENSUS ===
Analyst Recommendation: {recommendation_key}
Number of Analysts: {number_of_analysts}
Target Price (Mean): {target_mean_price:.2f}
Target High: {target_high_price:.2f}
Target Low: {target_low_price:.2f}
Implied Upside: {upside_potential:.2f}%

=== FUNDAMENTAL VALUATION ===
Forward P/E: {forward_pe:.2f}
Trailing P/E: {trailing_pe:.2f}
PEG Ratio: {peg_ratio:.2f}
Price/Book: {price_to_book:.2f}
Debt/Equity: {debt_to_equity:.2f}

Profitability:
- Profit Margin: {profit_margins:.2%}
- Revenue Growth: {revenue_growth:.2%}
- Earnings Growth: {earnings_growth:.2%}

Market Cap: {market_cap_formatted}
Beta: {beta:.2f}

---

Generate a comprehensive trading advisory report in Markdown format with the following structure:

# Trading Advisory: {name} ({ticker})

## Executive Summary
Provide a 2-3 sentence summary of the current situation and your recommendation.

## Technical Analysis Assessment

### Momentum & Trend
Analyze RSI, MACD, and trend indicators. Is momentum bullish or bearish?

### Price Action
Discuss the current price relative to moving averages and support/resistance levels.

### Volume Analysis
Interpret the volume ratio and what it signals about conviction.

## Fundamental Perspective

### Valuation Analysis
Is the stock cheap, fair, or expensive based on P/E, PEG, and other metrics?

### Financial Health
Assess debt levels, profitability, and growth rates.

## Wall Street vs Technicals
Compare analyst consensus with what the charts are saying. Any divergence?

## Risk Factors
List 3-4 specific risks for this position right now.

---

## 🎯 ADVISOR ACTION CARD

**RECOMMENDATION:** [KAUFEN / HALTEN / VERKAUFEN / WATCHLIST]

**ENTRY ZONE:**
€ [X.XX] - € [Y.YY]
_Rationale: [Why these specific prices]_

**PRICE TARGET (12M):**
€ [Z.ZZ]
_Basis: [Analyst consensus / Technical projection / Valuation model]_

**STOP-LOSS:**
€ [A.AA] (-X.X%)
_Logic: 3-5% below support at € [support_level]_

**POSITION SIZE GUIDANCE:**
[Small / Medium / Large] position (X-Y% of portfolio)

**KEY TRIGGERS:**
- ✅ Entry Signal: [Specific condition, e.g., "RSI drops below 50 + price above SMA50"]
- 🚨 Exit Signal: [Specific condition, e.g., "Break below €XX.XX support"]

**TIMEFRAME:** [Days / Weeks / Months]

---

## Analyst Notes
Any additional context or nuance that doesn't fit above.

---

**Disclaimer:** This analysis is for informational purposes only. Markets are inherently risky.
"""


def generate_advice_report(ticker: str, data: Dict[str, Any], api_key: Optional[str] = None) -> str:
    """
    Generate an actionable trading advisory report using LLM.

    Uses multi-LLM provider with automatic fallback:
    - Google Gemini (if configured)
    - OpenAI GPT-4 (if configured)
    - Anthropic Claude (if configured)

    Args:
        ticker: Stock ticker symbol
        data: Dictionary from market_data.get_full_advisor_data()
        api_key: Deprecated - API keys now read from environment

    Returns:
        Markdown-formatted trading advisory report with specific action card
    """
    # Get LLM provider (with automatic fallback)
    try:
        llm_provider = get_llm_provider()
    except LLMError as e:
        raise ValueError(str(e))

    # Calculate derived metrics for the prompt
    rsi = data.get('rsi', 50)
    rsi_status = "OVERBOUGHT (>70)" if rsi > 70 else "OVERSOLD (<30)" if rsi < 30 else "NEUTRAL"

    current_price = data.get('current_price', 0)
    sma_50 = data.get('sma_50', current_price)
    sma_200 = data.get('sma_200', current_price)

    price_vs_sma50 = ((current_price - sma_50) / sma_50 * 100) if sma_50 else 0
    price_vs_sma200 = ((current_price - sma_200) / sma_200 * 100) if sma_200 else 0

    macd = data.get('macd', 0)
    macd_signal = data.get('macd_signal', 0)
    macd_histogram = data.get('macd_histogram', 0)
    macd_status = "BULLISH" if macd_histogram > 0 else "BEARISH"

    bb_upper = data.get('bb_upper', current_price * 1.02)
    bb_lower = data.get('bb_lower', current_price * 0.98)
    bb_middle = data.get('bb_middle', current_price)

    if current_price > bb_upper:
        bb_position = "ABOVE upper band (overbought zone)"
    elif current_price < bb_lower:
        bb_position = "BELOW lower band (oversold zone)"
    else:
        bb_position = "WITHIN bands (normal range)"

    support_level = data.get('support_level', current_price * 0.95)
    resistance_level = data.get('resistance_level', current_price * 1.05)

    distance_to_support = ((current_price - support_level) / current_price * 100)
    distance_to_resistance = ((resistance_level - current_price) / current_price * 100)

    # Format market cap
    market_cap = data.get('market_cap', 0)
    if market_cap >= 1_000_000_000_000:
        market_cap_formatted = f"${market_cap / 1_000_000_000_000:.2f}T"
    elif market_cap >= 1_000_000_000:
        market_cap_formatted = f"${market_cap / 1_000_000_000:.2f}B"
    elif market_cap >= 1_000_000:
        market_cap_formatted = f"${market_cap / 1_000_000:.2f}M"
    else:
        market_cap_formatted = f"${market_cap:,.0f}"

    # Build the user prompt with all calculated metrics
    user_prompt = ADVISOR_USER_PROMPT_TEMPLATE.format(
        ticker=ticker,
        name=data.get('name', ticker),
        sector=data.get('sector', 'N/A'),
        current_price=current_price,
        currency=data.get('currency', 'USD'),
        price_change_1d=data.get('price_change_1d', 0),
        price_change_5d=data.get('price_change_5d', 0),
        price_change_1m=data.get('price_change_1m', 0),
        volume_ratio=data.get('volume_ratio', 1.0),
        rsi=rsi,
        rsi_status=rsi_status,
        trend=data.get('trend', 'NEUTRAL'),
        sma_50=sma_50,
        sma_200=sma_200,
        price_vs_sma50=price_vs_sma50,
        price_vs_sma200=price_vs_sma200,
        macd=macd or 0,
        macd_signal=macd_signal or 0,
        macd_histogram=macd_histogram or 0,
        macd_status=macd_status,
        bb_upper=bb_upper or current_price * 1.02,
        bb_middle=bb_middle or current_price,
        bb_lower=bb_lower or current_price * 0.98,
        bb_position=bb_position,
        support_level=support_level,
        resistance_level=resistance_level,
        pivot_point=data.get('pivot_point', current_price),
        support_1=data.get('support_1', support_level),
        resistance_1=data.get('resistance_1', resistance_level),
        distance_to_support=distance_to_support,
        distance_to_resistance=distance_to_resistance,
        recommendation_key=data.get('recommendation_key', 'none').upper(),
        number_of_analysts=data.get('number_of_analysts', 0),
        target_mean_price=data.get('target_mean_price') or current_price,
        target_high_price=data.get('target_high_price') or current_price * 1.2,
        target_low_price=data.get('target_low_price') or current_price * 0.8,
        upside_potential=data.get('upside_potential') or 0,
        forward_pe=data.get('forward_pe') or 0,
        trailing_pe=data.get('trailing_pe') or 0,
        peg_ratio=data.get('peg_ratio') or 0,
        price_to_book=data.get('price_to_book') or 0,
        debt_to_equity=data.get('debt_to_equity') or 0,
        profit_margins=data.get('profit_margins') or 0,
        revenue_growth=data.get('revenue_growth') or 0,
        earnings_growth=data.get('earnings_growth') or 0,
        market_cap_formatted=market_cap_formatted,
        beta=data.get('beta') or 1.0
    )

    try:
        # Generate advisory using multi-LLM provider with automatic fallback
        report = llm_provider.generate(
            system_prompt=ADVISOR_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.5,  # Lower temperature for more consistent, factual advice
            max_tokens=3000
        )

        return report

    except LLMError as e:
        raise RuntimeError(f"Error generating advisory report: {str(e)}")
