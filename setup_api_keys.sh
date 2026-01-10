#!/bin/bash

# Setup script for API keys
# Run this to configure alternative data sources

echo "========================================"
echo "Kruse Capital Advisor - API Key Setup"
echo "========================================"
echo ""

# Check .env file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env .env.backup 2>/dev/null || true
fi

echo "This script will help you set up API keys for alternative data sources."
echo "All sources are OPTIONAL - Yahoo Finance will be used as primary source."
echo ""

# Alpha Vantage
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Alpha Vantage (RECOMMENDED)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Free tier: 500 requests/day"
echo "Best for: Technical indicators (RSI, MACD)"
echo "Get your key at: https://www.alphavantage.co/support/#api-key"
echo ""
read -p "Enter Alpha Vantage API key (or press Enter to skip): " ALPHA_KEY

if [ ! -z "$ALPHA_KEY" ]; then
    if grep -q "ALPHA_VANTAGE_API_KEY" .env; then
        sed -i.bak "s/ALPHA_VANTAGE_API_KEY=.*/ALPHA_VANTAGE_API_KEY=$ALPHA_KEY/" .env
    else
        echo "ALPHA_VANTAGE_API_KEY=$ALPHA_KEY" >> .env
    fi
    echo "✓ Alpha Vantage API key saved"
else
    echo "⊘ Skipped Alpha Vantage"
fi

echo ""

# Polygon
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. Polygon.io (Optional)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Free tier: 5 requests/minute"
echo "Best for: High-quality market data"
echo "Get your key at: https://polygon.io/"
echo ""
read -p "Enter Polygon.io API key (or press Enter to skip): " POLYGON_KEY

if [ ! -z "$POLYGON_KEY" ]; then
    if grep -q "POLYGON_API_KEY" .env; then
        sed -i.bak "s/POLYGON_API_KEY=.*/POLYGON_API_KEY=$POLYGON_KEY/" .env
    else
        echo "POLYGON_API_KEY=$POLYGON_KEY" >> .env
    fi
    echo "✓ Polygon.io API key saved"
else
    echo "⊘ Skipped Polygon.io"
fi

echo ""

# OpenAI (reminder)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. OpenAI API (REQUIRED for AI reports)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if grep -q "OPENAI_API_KEY=sk-" .env; then
    echo "✓ OpenAI API key already configured"
else
    echo "Get your key at: https://platform.openai.com/api-keys"
    read -p "Enter OpenAI API key (or press Enter to skip): " OPENAI_KEY

    if [ ! -z "$OPENAI_KEY" ]; then
        if grep -q "OPENAI_API_KEY" .env; then
            sed -i.bak "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$OPENAI_KEY/" .env
        else
            echo "OPENAI_API_KEY=$OPENAI_KEY" >> .env
        fi
        echo "✓ OpenAI API key saved"
    else
        echo "⚠️  Warning: OpenAI key required for AI-powered reports"
    fi
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Your .env file has been configured."
echo ""
echo "Data source priority:"
echo "  1. Yahoo Finance (free, no key needed)"
echo "  2. Alpha Vantage (if configured)"
echo "  3. Polygon.io (if configured)"
echo ""
echo "Start the server with:"
echo "  uvicorn app.main:app --reload"
echo ""
