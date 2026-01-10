# Alternative Datenquellen für Finanzdaten

## Problem
Yahoo Finance blockiert bei zu vielen Requests (Rate Limiting 429 Error).

## Lösungen

### Option 1: Alpha Vantage (EMPFOHLEN für Production)

**Vorteile:**
- ✅ Kostenloser API Key (500 Requests/Tag)
- ✅ Technische Indikatoren built-in (RSI, MACD, SMA)
- ✅ Fundamentaldaten verfügbar
- ✅ Stabil und zuverlässig

**Installation:**
```bash
pip install alpha-vantage
```

**Setup:**
```python
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

# Get free API key: https://www.alphavantage.co/support/#api-key
API_KEY = 'your_alpha_vantage_key'

ts = TimeSeries(key=API_KEY, output_format='pandas')
ti = TechIndicators(key=API_KEY, output_format='pandas')

# Get price data
data, meta = ts.get_daily(symbol='AAPL', outputsize='full')

# Get RSI directly
rsi, meta = ti.get_rsi(symbol='AAPL', interval='daily')

# Get MACD
macd, meta = ti.get_macd(symbol='AAPL', interval='daily')
```

**Kosten:**
- Free: 500 requests/day
- Premium: $49.99/month (unlimited)

---

### Option 2: Polygon.io (BESTE für High-Frequency)

**Vorteile:**
- ✅ Sehr schnell und zuverlässig
- ✅ Websocket-Support für real-time
- ✅ Historische Daten bis 2 Jahre kostenlos
- ✅ Professionelle API

**Installation:**
```bash
pip install polygon-api-client
```

**Setup:**
```python
from polygon import RESTClient

# Get free API key: https://polygon.io/
client = RESTClient(api_key='your_polygon_key')

# Get aggregates (OHLCV)
aggs = client.get_aggs(
    ticker='AAPL',
    multiplier=1,
    timespan='day',
    from_='2023-01-01',
    to='2024-01-01'
)

# Get ticker details
details = client.get_ticker_details('AAPL')
```

**Kosten:**
- Free: 5 API calls/minute
- Starter: $29/month (unlimited calls)

---

### Option 3: Financial Modeling Prep (BESTE für Fundamentals)

**Vorteile:**
- ✅ Excellente Fundamentaldaten
- ✅ 250 Requests/Tag kostenlos
- ✅ Company ratings und analyst estimates
- ✅ Einfache API

**Installation:**
```bash
pip install financialmodelingprep
```

**Setup:**
```python
import requests

# Get free API key: https://site.financialmodelingprep.com/developer/docs
API_KEY = 'your_fmp_key'

# Get company quote
url = f'https://financialmodelingprep.com/api/v3/quote/AAPL?apikey={API_KEY}'
quote = requests.get(url).json()[0]

# Get financial statements
url = f'https://financialmodelingprep.com/api/v3/income-statement/AAPL?apikey={API_KEY}'
financials = requests.get(url).json()

# Get analyst estimates (Wall Street consensus)
url = f'https://financialmodelingprep.com/api/v3/analyst-estimates/AAPL?apikey={API_KEY}'
estimates = requests.get(url).json()
```

**Kosten:**
- Free: 250 requests/day
- Starter: $14/month (750 req/day)

---

### Option 4: Twelve Data (BESTE für Technical Analysis)

**Vorteile:**
- ✅ Spezialisiert auf technische Indikatoren
- ✅ 800 Requests/Tag kostenlos
- ✅ Über 120+ Indikatoren

**Installation:**
```bash
pip install twelvedata
```

**Setup:**
```python
from twelvedata import TDClient

# Get free API key: https://twelvedata.com/
td = TDClient(apikey='your_twelve_data_key')

# Get time series
ts = td.time_series(
    symbol='AAPL',
    interval='1day',
    outputsize=365
)

# Get RSI
rsi = td.time_series(
    symbol='AAPL',
    interval='1day',
    outputsize=100,
    type='RSI'
)

# Get MACD
macd = td.time_series(
    symbol='AAPL',
    interval='1day',
    outputsize=100,
    type='MACD'
)
```

---

### Option 5: yfinance mit Rate-Limiting-Schutz (Quick Fix)

Wenn du bei yfinance bleiben willst:

**A) Caching implementieren**
```python
import requests_cache

# Cache responses for 1 hour
session = requests_cache.CachedSession(
    'yfinance_cache',
    expire_after=3600
)

stock = yf.Ticker('AAPL', session=session)
```

**B) Exponential Backoff**
```python
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def get_stock_data(ticker):
    return yf.Ticker(ticker).info
```

**C) Proxy Rotation**
```python
# Use proxy services (rotating IPs)
proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'http://proxy.example.com:8080'
}

stock = yf.Ticker('AAPL', proxy=proxies)
```

**D) VPN wechseln**
- Einfach VPN-Server wechseln um neue IP zu bekommen

---

## Empfehlung für Kruse Capital Advisor

### Für Development/Testing:
**Twelve Data** (kostenlos, 800 req/day)
- Beste technische Indikatoren
- Genug Requests für Testing

### Für Production:
**Kombination aus:**
1. **Alpha Vantage** für technische Indikatoren (stabil, zuverlässig)
2. **Financial Modeling Prep** für Fundamentaldaten (analyst estimates)
3. **Caching** zur Reduzierung von API Calls

### Quick Fix (jetzt):
1. VPN an → neue IP → yfinance funktioniert wieder
2. Oder warte 1-2 Stunden → Block läuft ab

---

## Implementation für Kruse Capital Advisor

Ich kann eine **Multi-Source Data Aggregator** implementieren:

```python
class MarketDataAggregator:
    """Fetches data from multiple sources with fallback."""

    def __init__(self):
        self.sources = [
            AlphaVantageSource(),
            TwelveDataSource(),
            YFinanceSource()  # Fallback
        ]

    def get_data(self, ticker):
        for source in self.sources:
            try:
                return source.fetch(ticker)
            except Exception as e:
                logger.warning(f"{source.name} failed: {e}")
                continue
        raise Exception("All data sources failed")
```

**Vorteile:**
- Ausfallsicherheit
- Beste Datenqualität
- Keine Single Point of Failure

Soll ich das implementieren?
