"""
Dashboard Analyst Microservice
FastAPI application for generating AI-powered investment reports.
"""
import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging

from app.models import (
    AnalyzeRequest,
    AnalyzeResponse,
    AdviseRequest,
    AdviseResponse,
    ErrorResponse,
    HealthCheckResponse
)
from app.services.data_fetcher import get_market_data
from app.services.ai_engine import generate_investment_report
from app.services.market_data import get_full_advisor_data
from app.services.llm_advisor import generate_advice_report
from app.services.utils import resolve_isin_to_ticker

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="TR Dashboard",
    description="Intelligent microservice for investment analysis and actionable trading advice",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthCheckResponse)
async def root():
    """Root endpoint - health check."""
    return HealthCheckResponse(
        status="healthy",
        service="Kruse Capital Analyst",
        version="1.0.0"
    )


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint."""
    return HealthCheckResponse(
        status="healthy",
        service="Kruse Capital Analyst",
        version="1.0.0"
    )


@app.post(
    "/analyze",
    response_model=AnalyzeResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        404: {"model": ErrorResponse, "description": "ISIN not found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def analyze_security(request: AnalyzeRequest):
    """
    Analyze a security and generate an investment report.

    This endpoint:
    1. Resolves the ISIN to a ticker symbol
    2. Fetches market data from yfinance
    3. Generates an AI-powered investment report
    4. Returns the report in Markdown format

    Args:
        request: AnalyzeRequest containing ISIN and optional asset name

    Returns:
        AnalyzeResponse with the generated investment report

    Raises:
        HTTPException: If ISIN is not found or data fetching fails
    """
    logger.info(f"Received analysis request for ISIN: {request.isin}")

    try:
        # Step 1: Resolve ISIN to ticker
        ticker = resolve_isin_to_ticker(request.isin)

        if not ticker:
            logger.warning(f"ISIN not found in mapping: {request.isin}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ISIN {request.isin} not found in our database. Please contact support to add this security."
            )

        logger.info(f"Resolved ISIN {request.isin} to ticker {ticker}")

        # Step 2: Fetch market data
        try:
            market_data = get_market_data(ticker)
            logger.info(f"Successfully fetched market data for {ticker}")
        except Exception as e:
            logger.error(f"Error fetching market data for {ticker}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch market data: {str(e)}"
            )

        # Step 3: Generate AI report
        try:
            report = generate_investment_report(ticker, market_data)
            logger.info(f"Successfully generated report for {ticker}")
        except ValueError as e:
            logger.error(f"API key error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
            )
        except Exception as e:
            logger.error(f"Error generating report for {ticker}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate report: {str(e)}"
            )

        # Step 4: Return response
        return AnalyzeResponse(
            success=True,
            ticker=ticker,
            isin=request.isin,
            report=report,
            metadata={
                "asset_name": request.asset_name or market_data.get("basic_info", {}).get("name", "N/A"),
                "fetched_at": market_data.get("fetched_at"),
                "sector": market_data.get("basic_info", {}).get("sector", "N/A")
            }
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch any unexpected errors
        logger.error(f"Unexpected error processing request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@app.post(
    "/advise",
    response_model=AdviseResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        404: {"model": ErrorResponse, "description": "ISIN not found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def advise_on_trade(request: AdviseRequest):
    """
    Generate actionable trading advice with technical analysis.

    This endpoint combines:
    - Technical indicators (RSI, MACD, SMA, Support/Resistance)
    - Fundamental valuation metrics
    - Wall Street analyst consensus
    - AI-powered trading strategy

    The result is a comprehensive trading advisory with:
    - Clear BUY/SELL/HOLD/WATCHLIST recommendation
    - Specific entry zones and price targets
    - Stop-loss placement
    - Risk assessment

    Args:
        request: AdviseRequest containing ISIN and optional asset name

    Returns:
        AdviseResponse with actionable trading advisory

    Raises:
        HTTPException: If ISIN is not found or data fetching fails
    """
    logger.info(f"Received advisory request for ISIN: {request.isin}")

    try:
        # Step 1: Resolve ISIN to ticker
        ticker = resolve_isin_to_ticker(request.isin)

        if not ticker:
            logger.warning(f"ISIN not found in mapping: {request.isin}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ISIN {request.isin} not found in our database. Please contact support to add this security."
            )

        logger.info(f"Resolved ISIN {request.isin} to ticker {ticker}")

        # Step 2: Fetch comprehensive market data with technical analysis
        try:
            advisor_data = get_full_advisor_data(ticker)
            logger.info(f"Successfully fetched advisor data for {ticker}")
        except Exception as e:
            logger.error(f"Error fetching advisor data for {ticker}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch market data: {str(e)}"
            )

        # Step 3: Generate AI-powered trading advisory
        try:
            advisory_report = generate_advice_report(ticker, advisor_data)
            logger.info(f"Successfully generated trading advisory for {ticker}")
        except ValueError as e:
            logger.error(f"API key error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
            )
        except Exception as e:
            logger.error(f"Error generating advisory for {ticker}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate advisory: {str(e)}"
            )

        # Step 4: Return comprehensive response
        return AdviseResponse(
            success=True,
            ticker=ticker,
            isin=request.isin,
            advisory_report=advisory_report,
            technical_data={
                "rsi": advisor_data.get("rsi"),
                "trend": advisor_data.get("trend"),
                "support_level": advisor_data.get("support_level"),
                "resistance_level": advisor_data.get("resistance_level"),
                "current_price": advisor_data.get("current_price"),
                "target_price": advisor_data.get("target_mean_price"),
                "recommendation": advisor_data.get("recommendation_key")
            },
            metadata={
                "asset_name": request.asset_name or advisor_data.get("name", "N/A"),
                "sector": advisor_data.get("sector", "N/A"),
                "data_timestamp": advisor_data.get("data_timestamp"),
                "analyst_count": advisor_data.get("number_of_analysts", 0)
            }
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch any unexpected errors
        logger.error(f"Unexpected error processing advisory request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@app.get("/supported-securities")
async def list_supported_securities():
    """
    List all supported securities (ISINs and their tickers).

    Returns:
        Dictionary mapping ISINs to ticker symbols
    """
    from app.services.utils import ISIN_TO_TICKER_MAP

    return {
        "total_count": len(ISIN_TO_TICKER_MAP),
        "securities": ISIN_TO_TICKER_MAP
    }


if __name__ == "__main__":
    import uvicorn

    # Get port from environment or default to 8000
    port = int(os.getenv("PORT", 8000))

    logger.info(f"Starting Kruse Capital Analyst on port {port}")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
