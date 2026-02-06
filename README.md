# SME Financial Health Platform

> **AI-Powered CFO for Small & Medium Enterprises**

An intelligent financial analysis platform that transforms raw financial data into actionable business insights, helping SMEs make informed decisions about their financial health.

---

## 🎯 Problem Statement

**Small and Medium Enterprises (SMEs) lack access to CFO-level financial insights.**

- **60% of SMEs fail** due to cash flow problems they didn't see coming
- No dedicated finance teams to interpret complex data
- Limited access to expensive financial consultants
- Reactive decision-making instead of proactive planning

---

## 💡 Our Solution

**An AI CFO that transforms raw financial data into actionable recommendations.**

```
Upload Files → AI Analysis → Plain-Language Insights → Action Plans
```

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Smart Data Ingestion** | Upload CSV, Excel, PDF - auto-detected and normalized |
| **Health Score Engine** | 20+ financial metrics with 0-100 score and grade |
| **AI CFO Chat** | Ask questions in plain English, get CFO-level advice |
| **Risk Alerts** | Proactive warnings before problems occur |
| **90-Day Action Plans** | AI-generated improvement strategies |
| **Product Recommendations** | Contextual loan/investment suggestions |
| **PDF Reports** | Investor-ready executive summaries |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                         │
│  Dashboard │ Upload │ Analysis │ Chat │ Reports │ Multilingual  │
└─────────────────────────────────────────────────────────────────┘
                              │
                        Nginx (Proxy)
                              │
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ File Processor│  │Health Score  │  │ LLM Service  │          │
│  │ CSV/XLSX/PDF │  │ Engine       │  │ (Groq API)   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Risk Alerts  │  │Product Reco  │  │Report Gen    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │  PostgreSQL 15    │
                    │  (Encrypted Data) │
                    └───────────────────┘
```

---

## 🔧 Technology Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 18, Vite, Lucide Icons, i18next |
| **Backend** | FastAPI, Python 3.11, SQLAlchemy |
| **Database** | PostgreSQL 15 |
| **AI/LLM** | Groq API (Llama 3.3-70B Versatile) |
| **Security** | bcrypt + SHA256, Fernet encryption, JWT |
| **Deployment** | Docker Compose, Nginx |

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Groq API Key (free at console.groq.com)

### Setup

```bash
# Clone the repository
git clone <repo-url>
cd AAAGuvi

# Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Start all services
docker-compose up -d

# Access the application
open http://localhost
```

---

## 📊 Key Features Explained

### 1. Financial Health Score Engine
Calculates 20+ metrics across 4 categories:
- **Liquidity** - Current ratio, quick ratio, cash runway
- **Profitability** - Net margin, ROE, operating efficiency
- **Solvency** - Debt-to-equity, interest coverage
- **Efficiency** - Working capital cycle, DSO, DPO

### 2. AI CFO Chat
Ask questions in plain language:
- *"What's my financial health?"*
- *"Am I ready for a loan?"*
- *"What should I focus on this quarter?"*

Responses are action-oriented with clear next steps.

### 3. Smart Risk Alerts
Proactive warnings with severity levels:
- 🔴 **Critical** - Immediate action required
- 🟠 **Warning** - Address within 30 days
- 🟢 **Info** - Monitor and track

### 4. 90-Day Action Plan
AI-generated improvement strategy:
- Week-by-week action items
- Expected impact percentages
- Priority ranking

---

## 🔒 Security Features

- **AES-256 encryption** for financial data at rest
- **TLS 1.3** for data in transit
- **JWT authentication** with secure token handling
- **bcrypt + SHA256** password hashing
- **Role-based access control**

---

## 📈 Business Impact

| Metric | Before | After |
|--------|--------|-------|
| Analysis Time | Hours/Days | Seconds |
| CFO Consultation Cost | ₹50K+/month | ₹0 |
| Risk Detection | Reactive | Proactive |
| Decision Quality | Gut feeling | Data-driven |

---

## 🎯 Target Users

- **SME Business Owners** - Primary users seeking financial clarity
- **Accountants** - Financial data validation and analysis
- **Bank Officers** - Loan evaluation and risk assessment
- **Investors** - Due diligence and portfolio monitoring

---

## 📁 Project Structure

```
AAAGuvi/
├── backend/
│   ├── routers/          # API endpoints
│   ├── services/         # Business logic
│   ├── security/         # Auth handlers
│   └── models.py         # Database models
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   └── services/     # API clients
│   └── nginx.conf        # Proxy configuration
├── docker-compose.yml    # Container orchestration
└── README.md
```

---

## 🔮 Future Roadmap

- [ ] Real-time bank account integration
- [ ] GST/Tax compliance automation
- [ ] WhatsApp bot for mobile access
- [ ] Automated invoice processing
- [ ] Mobile app (React Native)

---

## 📄 License

MIT License - See LICENSE file for details.

---

## 👨‍💻 Author

Built for GUVI AI Engineer Hackathon 2026

---

> *"Transforming financial complexity into business clarity."*
