# Google Gemini Integration - Setup Guide

## ✅ Ja! Gemini API wird vollständig unterstützt

Das System unterstützt jetzt **Multi-LLM Provider** mit automatischem Fallback:

1. **Google Gemini** (primär, empfohlen)
2. **OpenAI GPT-4** (fallback)
3. **Anthropic Claude** (fallback)

## 🚀 Warum Gemini verwenden?

### Vorteile

✅ **5x günstiger als OpenAI**
```
Gemini 2.0 Flash:  $0.15/1M input + $0.60/1M output
OpenAI GPT-4o:     $2.50/1M input + $10.00/1M output
```

✅ **Schneller**
- Gemini 2.0 Flash ist optimiert für Geschwindigkeit
- Niedrigere Latenz als GPT-4

✅ **Großzügiger Free Tier**
- 60 Requests/Minute kostenlos
- 1,500 Requests/Tag kostenlos
- Perfekt für Development & Testing

✅ **Hohe Qualität**
- Gemini 2.0 Flash ist sehr gut für Financial Analysis
- Vergleichbare Qualität zu GPT-4 für unseren Use Case

## 📝 Setup (2 Minuten)

### Schritt 1: API Key erstellen

```bash
# 1. Besuche Google AI Studio
https://makersuite.google.com/app/apikey

# 2. Klick auf "Create API key"

# 3. Wähle ein Google Cloud Project (oder erstelle ein neues)

# 4. Kopiere den Key (startet mit AIza...)
```

### Schritt 2: In .env eintragen

```bash
# Öffne die .env Datei
nano .env

# Füge deinen Gemini Key ein
GEMINI_API_KEY=AIzaSy...dein_key_hier

# Speichern und schließen (Ctrl+X, Y, Enter)
```

### Schritt 3: google-generativeai installieren

```bash
pip install google-generativeai==0.8.3
```

### Schritt 4: Testen

```bash
python3 test_llm_providers.py
```

## 🔧 Wie es funktioniert

### Automatischer Fallback

```python
LLM Provider Reihenfolge:

1. Versuche Gemini (falls GEMINI_API_KEY gesetzt)
   ↓ Falls Fehler
2. Versuche OpenAI (falls OPENAI_API_KEY gesetzt)
   ↓ Falls Fehler
3. Versuche Anthropic (falls ANTHROPIC_API_KEY gesetzt)
   ↓ Falls alle fehlschlagen
4. Error zurückgeben
```

### Code-Beispiel

```python
from app.services.llm_providers import get_llm_provider

# Automatisch den besten verfügbaren Provider nutzen
llm = get_llm_provider()

report = llm.generate(
    system_prompt="You are a financial advisor...",
    user_prompt="Analyze Apple stock...",
    temperature=0.5,
    max_tokens=2000
)

# Der Provider wählt automatisch:
# - Gemini (wenn verfügbar) → Schnell & günstig
# - Oder OpenAI als Fallback
```

## 📊 Vergleich: Gemini vs OpenAI

| Feature | Gemini 2.0 Flash | OpenAI GPT-4o |
|---------|------------------|---------------|
| **Kosten (Input)** | $0.15/1M tokens | $2.50/1M tokens |
| **Kosten (Output)** | $0.60/1M tokens | $10.00/1M tokens |
| **Speed** | ⚡⚡⚡ Sehr schnell | ⚡⚡ Schnell |
| **Quality** | ✅ Sehr gut | ✅ Excellent |
| **Free Tier** | 60 req/min | ❌ Keiner |
| **Best For** | Production | High-end Analysis |

**Empfehlung:**
- Development: **Gemini** (kostenlos)
- Production: **Gemini** (5x günstiger)
- High-stakes: **OpenAI als Fallback**

## 🎯 Production Setup

### Empfohlene Konfiguration

```bash
# .env für Production
GEMINI_API_KEY=AIza...                    # PRIMARY
OPENAI_API_KEY=sk-...                     # FALLBACK
ALPHA_VANTAGE_API_KEY=...                 # DATA FALLBACK
```

**Kosten Estimation:**
```
1000 Advisory Reports/Monat:

Mit Gemini:  ~$1.50/Monat  ✅
Mit OpenAI:  ~$7.50/Monat
Mit Claude:  ~$9.00/Monat

Ersparnis: $6/Monat pro 1000 Reports
```

## 📈 Rate Limits

### Gemini Free Tier
- 60 Requests/Minute
- 1,500 Requests/Tag
- ~45,000 Requests/Monat

### Gemini Paid (Pay-as-you-go)
- Unbegrenzte Requests
- Nur zahlen was du nutzt
- Kein monatliches Minimum

### OpenAI (zum Vergleich)
- Pay-per-use (kein Free Tier)
- Rate Limits basierend auf Tier
- Höhere Kosten

## 🔐 Sicherheit

**WICHTIG:**
- Commitiere NIEMALS API Keys zu Git
- `.env` ist bereits in `.gitignore`
- Rotiere Keys regelmäßig
- Nutze separate Keys für Dev/Prod

## 🧪 Testing

### Test 1: Provider Check
```bash
python3 test_llm_providers.py
```

Zeigt:
- Welche Provider konfiguriert sind
- Welcher als Erstes versucht wird
- Test-Generation mit echtem API Call

### Test 2: Complete Demo
```bash
python3 demo_advisor_complete.py
```

Nutzt Gemini für vollständige Advisory-Generierung (Mock-Daten).

## 🐛 Troubleshooting

### "No LLM providers configured"
```bash
# Lösung: Mindestens einen API Key hinzufügen
echo "GEMINI_API_KEY=AIza...dein_key" >> .env
```

### "google.generativeai package not installed"
```bash
# Lösung: Package installieren
pip install google-generativeai==0.8.3
```

### "Invalid API key"
```bash
# Prüfe:
# 1. Key korrekt kopiert? (startet mit AIza...)
# 2. Key aktiviert in Google Cloud Console?
# 3. Billing account verbunden? (für paid tier)
```

### Gemini antwortet nicht
```bash
# Fallback greift automatisch!
# System versucht dann OpenAI
# Logs prüfen:
tail -f app.log
```

## 📚 Gemini Models

### Verfügbare Models

```python
# Aktuell verwendet:
gemini-2.0-flash-exp          # Neuestes, schnellstes Model

# Alternativen:
gemini-1.5-pro               # Mehr Kontext (2M tokens)
gemini-1.5-flash             # Ausbalanciert
```

### Model-Switching

In [llm_providers.py](app/services/llm_providers.py:44):
```python
model = self.client.GenerativeModel(
    model_name='gemini-2.0-flash-exp',  # ← Hier ändern
    system_instruction=system_prompt
)
```

## 🎬 Quick Start

**Komplett-Setup in 3 Befehlen:**

```bash
# 1. Gemini Key holen & zu .env hinzufügen
echo "GEMINI_API_KEY=AIza...dein_key" >> .env

# 2. Package installieren
pip install google-generativeai

# 3. Testen
python3 test_llm_providers.py
```

**Fertig! Das System nutzt jetzt automatisch Gemini.** 🎉

## 💡 Tipps

1. **Start with Free Tier**
   - Teste mit Gemini Free
   - Kostenlos bis 60 req/min
   - Kreditkarte nicht erforderlich

2. **Monitor Usage**
   - Google Cloud Console → APIs & Services
   - Quotas & System Limits
   - Usage Reports

3. **Combine with OpenAI**
   - Gemini für 95% der Requests
   - OpenAI als Premium-Fallback
   - Beste Cost/Quality Balance

4. **Production Best Practices**
   - Enable billing alerts
   - Set spending limits
   - Monitor error rates
   - Keep OpenAI as fallback

## 🔗 Links

- Gemini API Docs: https://ai.google.dev/docs
- Google AI Studio: https://makersuite.google.com/
- Pricing: https://ai.google.dev/pricing
- Python SDK: https://github.com/google/generative-ai-python

## ❓ FAQ

**Q: Ist Gemini kostenlos?**
A: Ja! Free tier: 60 req/min, 1500 req/day. Für unseren Use Case ausreichend.

**Q: Wie ist die Qualität vs GPT-4?**
A: Für Financial Analysis sehr gut. Gemini 2.0 ist auf Augenhöhe mit GPT-4 für unsere Prompts.

**Q: Muss ich eine Kreditkarte hinterlegen?**
A: Nein, für Free Tier nicht erforderlich. Nur für Pay-as-you-go.

**Q: Was passiert wenn Gemini ausfällt?**
A: Automatischer Fallback zu OpenAI (falls konfiguriert). Zero downtime.

**Q: Kann ich Gemini UND OpenAI zusammen nutzen?**
A: Ja! Empfohlene Production-Config. Gemini primary, OpenAI fallback.
