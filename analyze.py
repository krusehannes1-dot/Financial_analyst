#!/usr/bin/env python3
"""
CLI tool to analyze securities and display formatted reports.
Usage: python analyze.py <ISIN> [asset_name]
"""
import sys
import json
import requests

API_URL = "http://localhost:8000/analyze"

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze.py <ISIN> [asset_name]")
        print("Example: python analyze.py US88160R1014 'Tesla Inc.'")
        sys.exit(1)
    
    isin = sys.argv[1]
    asset_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    payload = {"isin": isin}
    if asset_name:
        payload["asset_name"] = asset_name
    
    print(f"\n🔍 Analyzing {isin}...\n")
    
    try:
        response = requests.post(API_URL, json=payload, timeout=120)
        data = response.json()
        
        if data.get("success"):
            print("=" * 60)
            print(f"Ticker: {data.get('ticker')} | ISIN: {data.get('isin')}")
            print(f"Sector: {data.get('metadata', {}).get('sector', 'N/A')}")
            print("=" * 60)
            print()
            print(data.get("report", "No report generated."))
            print()
            print("=" * 60)
        else:
            print(f"❌ Error: {data.get('detail', 'Unknown error')}")
            sys.exit(1)
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Server not running. Start with: uvicorn app.main:app")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
