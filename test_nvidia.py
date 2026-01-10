"""
Direct test for NVIDIA (US67066G1040) analysis.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.utils import resolve_isin_to_ticker

# Test ISIN resolution for NVIDIA
isin = "US67066G1040"
print("=" * 70)
print("NVIDIA (NVDA) Analysis Test")
print("=" * 70)
print(f"\nISIN: {isin}")

ticker = resolve_isin_to_ticker(isin)
print(f"Resolved Ticker: {ticker}")

if ticker:
    print(f"\n✓ Successfully resolved ISIN to ticker: {ticker}")
    print(f"\nThis ISIN maps to NVIDIA Corporation")
    print(f"\nTo fetch live data and generate a report, you would:")
    print(f"1. Start the FastAPI server: uvicorn app.main:app --reload")
    print(f"2. Make a POST request to /analyze with this payload:")
    print(f"""
    {{
        "isin": "{isin}",
        "asset_name": "NVIDIA Corporation"
    }}
    """)

    print("\nExample cURL command:")
    print(f"""
    curl -X POST "http://localhost:8000/analyze" \\
      -H "Content-Type: application/json" \\
      -d '{{
        "isin": "{isin}",
        "asset_name": "NVIDIA Corporation"
      }}'
    """)
else:
    print(f"\n✗ ISIN {isin} not found in mapping")

print("\n" + "=" * 70)
