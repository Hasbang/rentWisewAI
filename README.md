# 🏠 RentWise AI

> AI-powered rental decision support for Freetown, Sierra Leone.

RentWise AI helps renters make informed housing decisions by analysing available rental properties against their budget, location, and personal requirements — and explaining the reasoning behind every recommendation.

This is **not** a rental marketplace. It is a **decision support system** built with multi-agent AI.

---

## 📸 Preview

![RentWise AI Screenshot](screenshot.png) - // not added yet

---

## 🎯 What It Does

A renter enters their requirements:

- Total cash available today (NLE)
- Preferred location in Freetown
- Number of bedrooms and bathrooms
- Property type
- Additional notes and preferences

Two AI agents then go to work:

| Agent | Role |
|---|---|
| **Property Analyst** | Receives pre-filtered results from Python, explains why each property ranked where it did, highlights risk flags |
| **Rental Advisor** | Advises the renter in plain language, explains trade-offs, gives a clear final recommendation |

The system explains **why** each recommendation was made — not just what is available.

---

## 🧠 Core Logic

All financial logic runs in deterministic Python — not inside LLM prompts.

**Move-in Cost Calculation:**
```
Move-in Cost = Yearly Rent × Advance Required (years)
```

In Sierra Leone, landlords typically require 1–2 years of rent paid upfront. RentWise AI accounts for this reality in every recommendation.

**Affordability Filter:**
```
Property is affordable if: Move-in Cost <= Budget
```

**Risk Flagging:**
```
Remaining Cash = Budget - Move-in Cost
If Remaining Cash < 10% of Budget → ⚠ HIGH UPFRONT CAPITAL RISK
```

**Match Scoring:**
```
Location match:       +40 points
Property type match:  +20 points
Bathroom match:       +15 points
Bedroom exact match:  +15 points
Parking available:    +5 points
Furnished:            +5 points
```

Properties are ranked by match score before being passed to the AI agents. The agents explain and advise — they do not calculate.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10 |
| Frontend | Streamlit |
| AI Framework | CrewAI |
| LLM | OpenAI GPT-4o-mini via OpenRouter |
| Database | Supabase (PostgreSQL) |

---

## 🏗️ Project Structure

```
rentwise-ai/
│
├── app.py                      # Streamlit web interface
│
├── agents/
│   ├── property_analyst.py     # Agent 1 — explains ranked results
│   └── rental_advisor.py       # Agent 2 — advises and recommends
│
├── tasks/
│   ├── analysis_task.py        # Task for Agent 1
│   └── advisory_task.py        # Task for Agent 2
│
├── crew/
│   └── rentwise_crew.py        # Assembles agents and runs the crew
│
├── utils/
│   ├── data_loader.py          # Fetches properties from Supabase
│   └── property_filter.py      # Python financial logic and ranking
│
├── config/
│   └── settings.py             # API keys, model config, startup checks
│
├── .env.example                # Environment variable template
└── requirements.txt
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Hasbang/rentWisewAI.git
cd rentWisewAI
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

Open `.env` and add your credentials:

```env
OPENROUTER_API_KEY=your-openrouter-api-key-here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
MODEL_NAME=openai/gpt-4o-mini

SUPABASE_URL=your-supabase-project-url
SUPABASE_KEY=your-supabase-anon-key
```

Get a free OpenRouter API key at [openrouter.ai](https://openrouter.ai).  
Get a free Supabase project at [supabase.com](https://supabase.com).

### 5. Set up the database

In your Supabase SQL editor, run:

```sql
CREATE TABLE properties (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    location TEXT NOT NULL,
    yearly_rent INTEGER NOT NULL,
    advance_required INTEGER NOT NULL,
    bedrooms INTEGER NOT NULL,
    bathrooms INTEGER NOT NULL,
    property_type TEXT NOT NULL,
    furnished BOOLEAN DEFAULT FALSE,
    parking BOOLEAN DEFAULT FALSE,
    water_supply TEXT,
    electricity TEXT,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 6. Run the app

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 📊 Current Property Listings

RentWise AI currently has 6 rental listings in Freetown:

| ID | Property | Location | Yearly Rent | Advance |
|---|---|---|---|---|
| P001 | 2-Bed Apartment | Wilberforce | NLE 36,000 | 2 years |
| P002 | 3-Bed House | Murray Town | NLE 48,000 | 2 years |
| P003 | 1-Bed Flat | Kissy | NLE 18,000 | 1 year |
| P004 | 3-Bed Executive Apt | Hill Station | NLE 72,000 | 2 years |
| P005 | 2-Bed Bungalow | Lumley | NLE 42,000 | 2 years |
| P006 | 1-Bed Studio | Congo Cross | NLE 24,000 | 1 year |

To add more properties, insert rows directly into the Supabase `properties` table — no code changes needed.

---

## 🗺️ Roadmap

- [x] Multi-agent CrewAI system
- [x] Streamlit web interface
- [x] Supabase PostgreSQL database
- [x] Deterministic Python financial logic and match scoring
- [x] Risk flagging
- [x] Property cards built from reliable Python data
- [x] No-results handling with actionable suggestions
- [x] Startup validation for missing environment variables
- [ ] Landlord portal for property submissions
- [ ] User authentication
- [ ] WhatsApp integration for mobile-first access
- [ ] Google Maps integration for property locations
- [ ] Image uploads for listings
- [ ] Saved searches and notifications
- [ ] Market insights AI agent
- [ ] Analytics dashboard

---

## 🤝 Contributing

This project is part of an AI engineering portfolio focused on building technology for Sierra Leone's rental market. Contributions, feedback, and feature suggestions are welcome.

---

## 👤 Author

**Hassan Bangura** — AI Engineering Portfolio Project  
Built for Freetown, Sierra Leone 🇸🇱  
Powered by CrewAI & OpenRouter