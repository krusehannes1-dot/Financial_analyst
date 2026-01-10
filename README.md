# Kruse Capital Analyst

## Overview
The **Kruse Capital Analyst** is an intelligent microservice that generates comprehensive, AI-powered investment reports for stocks and ETFs. Built with FastAPI and integrated with OpenAI's GPT-4, it provides professional-grade equity analysis by combining real-time market data with advanced language models.

## Features

- **ISIN to Ticker Resolution**: Automatically converts ISINs to ticker symbols
- **Real-time Market Data**: Fetches live financial data using yfinance
- **AI-Powered Analysis**: Generates detailed investment reports using GPT-4
- **Professional Reports**: Structured markdown reports with:
  - Executive Summary
  - Company Overview
  - Fundamental Analysis (Valuation, Financial Health, Profitability)
  - Bull/Bear Case Analysis
  - Recent News Analysis
  - Investment Conclusion
- **RESTful API**: Easy-to-use FastAPI endpoints
- **Comprehensive Coverage**: Supports major US stocks, European stocks, and popular ETFs

## Project Structure

```
dashboard_analyst/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application & endpoints
│   ├── models.py            # Pydantic request/response models
│   └── services/
│       ├── __init__.py
│       ├── data_fetcher.py  # yfinance data retrieval
│       ├── ai_engine.py     # OpenAI report generation
│       └── utils.py         # ISIN mapping & utilities
├── .env                     # Environment variables (API keys)
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Tech Stack

- **Python 3.10+**
- **FastAPI**: Modern web framework for building APIs
- **yfinance**: Financial data retrieval
- **OpenAI API**: GPT-4 for report generation
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd ~/.gemini/antigravity/scratch/dashboard_analyst
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Edit the `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   PORT=8000
   ENVIRONMENT=development
   ```

## Usage

### Starting the Server

Run the FastAPI server using uvicorn:

```bash
# From the project root directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or run directly via Python:

```bash
python -m app.main
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### 1. Health Check
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Kruse Capital Analyst",
  "version": "1.0.0"
}
```

#### 2. Analyze Security
```bash
POST /analyze
```

**Request Body:**
```json
{
  "isin": "US0378331005",
  "asset_name": "Apple Inc."
}
```

**Response:**
```json
{
  "success": true,
  "ticker": "AAPL",
  "isin": "US0378331005",
  "report": "# Investment Analysis: Apple Inc. (AAPL)\n\n## Executive Summary...",
  "metadata": {
    "asset_name": "Apple Inc.",
    "fetched_at": "2026-01-10T10:30:00",
    "sector": "Technology"
  }
}
```

#### 3. List Supported Securities
```bash
GET /supported-securities
```

**Response:**
```json
{
  "total_count": 45,
  "securities": {
    "US0378331005": "AAPL",
    "US5949181045": "MSFT",
    ...
  }
}
```

### Example Usage with cURL

```bash
# Analyze Apple stock
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "isin": "US0378331005",
    "asset_name": "Apple Inc."
  }'
```

### Example Usage with Python

```python
import requests

url = "http://localhost:8000/analyze"
payload = {
    "isin": "US0378331005",
    "asset_name": "Apple Inc."
}

response = requests.post(url, json=payload)
data = response.json()

if data["success"]:
    print(f"Report for {data['ticker']}:")
    print(data["report"])
else:
    print(f"Error: {data['error']}")
```

## Supported Securities

The service currently supports 45+ securities including:

### US Tech Stocks
- Apple (US0378331005)
- Microsoft (US5949181045)
- Tesla (US88160R1014)
- Google/Alphabet (US02079K3059)
- Amazon (US0231351067)
- Meta (US30303M1027)
- NVIDIA (US67066G1040)

### ETFs
- SPDR S&P 500 (US78462F1030)
- iShares Core MSCI World (IE00B4L5Y983)
- Vanguard S&P 500 (US9229087690)
- And many more...

Use the `/supported-securities` endpoint to get the full list.

## Adding New Securities

To add support for new securities, edit [app/services/utils.py](app/services/utils.py) and add entries to the `ISIN_TO_TICKER_MAP` dictionary:

```python
ISIN_TO_TICKER_MAP = {
    "YOUR_ISIN_HERE": "TICKER",
    # Example:
    "US0378331005": "AAPL",
}
```

## Development

### Testing Data Fetcher

You can test the data fetcher independently:

```python
from app.services.data_fetcher import get_market_data

data = get_market_data("AAPL")
print(data)
```

### Testing Report Generation

Test the AI engine:

```python
from app.services.data_fetcher import get_market_data
from app.services.ai_engine import generate_investment_report

data = get_market_data("AAPL")
report = generate_investment_report("AAPL", data)
print(report)
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `PORT`: Server port (default: 8000)
- `ENVIRONMENT`: Environment name (development/production)

## Error Handling

The API returns structured error responses:

```json
{
  "success": false,
  "error": "ISIN US1234567890 not found in our database",
  "detail": "Please contact support to add this security."
}
```

Common error codes:
- `400`: Bad request (invalid ISIN format)
- `404`: ISIN not found in mapping
- `500`: Server error (data fetching or AI generation failed)

## Limitations

- **ISIN Mapping**: Only securities in the ISIN_TO_TICKER_MAP are supported
- **Data Source**: Relies on yfinance availability
- **API Costs**: Each report generation consumes OpenAI API credits
- **Rate Limits**: Subject to OpenAI API rate limits

## Future Enhancements

- Database integration for ISIN mappings
- Caching layer for frequently requested securities
- Historical report storage
- Multi-language report generation
- Custom report templates
- Batch analysis endpoints

## License

Proprietary - Kruse Capital

## Support

For issues or feature requests, contact the development team.
