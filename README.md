# 🏠 RentWise AI

> AI-powered rental decision support for Freetown, Sierra Leone.

RentWise AI helps renters make informed housing decisions by analysing available rental properties against their budget, location, and personal requirements — and explaining the reasoning behind every recommendation.

This is **not** a rental marketplace. It is a **decision support system** built with multi-agent AI.

---

## 📸 Preview

![RentWise AI Screenshot](screenshot.png)

---

## 🎯 What It Does

A renter enters their requirements:

- Total cash available today (NLE or USD)
- Preferred location in Freetown
- Number of bedrooms and bathrooms
- Property type
- Additional notes and preferences

Two AI agents then go to work:

| Agent | Role |
|---|---|
| **Property Analyst** | Filters properties by affordability, calculates move-in costs, flags financial risks, ranks matches |
| **Rental Advisor** | Explains why each property does or doesn't suit the renter, gives a clear final recommendation |

The system explains **why** each recommendation was made — not just what is available.

---

## 🧠 Core Logic

**Move-in Cost Calculation:**
```
Move-in Cost = Yearly Rent × Advance Required (years)
```

In Sierra Leone, landlords typically require 1–2 years of rent paid upfront. RentWise AI accounts for this reality in every recommendation.

**Risk Flagging:**
```
Remaining Cash = Budget - Move-in Cost
If Remaining Cash < 10% of Budget → ⚠ HIGH UPFRONT CAPITAL RISK
```

Any property that leaves the renter with less than 10% of their original cash is flagged as a financial risk.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10 |
| Frontend | Streamlit |
| AI Framework | CrewAI |
| LLM | OpenAI GPT-4o-mini via OpenRouter |
| Data Storage | Local JSON (MVP) |

---

## 🏗️ Project Structure

```
rentwise-ai/
│
├── app.py                    # Streamlit web interface
│
├── agents/
│   ├── property_analyst.py   # Agent 1 — filters and ranks properties
│   └── rental_advisor.py     # Agent 2 — advises and recommends
│
├── tasks/
│   ├── analysis_task.py      # Task for Agent 1
│   └── advisory_task.py      # Task for Agent 2
│
├── crew/
│   └── rentwise_crew.py      # Assembles agents and runs the crew
│
├── data/
│   └── properties.json       # Rental listings (MVP data)
│
├── utils/
│   └── data_loader.py        # Reads and returns property data
│
├── config/
│   └── settings.py           # API keys and model configuration
│
├── .env.example              # Environment variable template
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
```

You can get a free OpenRouter API key at [openrouter.ai](https://openrouter.ai).

### 5. Run the app

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 📊 Sample Property Data

The MVP includes 6 sample rental listings in Freetown covering a range of locations, budgets, and property types:

| ID | Property | Location | Yearly Rent | Advance |
|---|---|---|---|---|
| P001 | 2-Bed Apartment | Wilberforce | NLE 36,000 | 2 years |
| P002 | 3-Bed House | Murray Town | NLE 48,000 | 2 years |
| P003 | 1-Bed Flat | Kissy | NLE 18,000 | 1 year |
| P004 | 3-Bed Executive Apt | Hill Station | NLE 72,000 | 2 years |
| P005 | 2-Bed Bungalow | Lumley | NLE 42,000 | 2 years |
| P006 | 1-Bed Studio | Congo Cross | NLE 24,000 | 1 year |

To add more properties, edit `data/properties.json` following the same structure.

---

## 🗺️ Roadmap

The MVP uses local JSON for data storage. Planned expansions include:

- [ ] Supabase/PostgreSQL database with pgvector semantic search
- [ ] User authentication (Firebase)
- [ ] Landlord portal for property submissions
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

**Hassan  Bangura ** — AI Engineering Portfolio Project  
Built for Freetown, Sierra Leone 🇸🇱  
Powered by CrewAI & OpenRouter
