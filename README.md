# 🏢 ERP System — Complete GST + Accounting Software
## Built with Flask, PostgreSQL, openpyxl, reportlab

---

## 📁 Project Structure
```
erp/
├── app.py                  ← Main Flask app, all blueprints
├── models.py               ← 29+ SQLAlchemy models
├── extensions.py           ← db, login_manager init
├── requirements.txt        ← All dependencies
├── .env.example            ← Environment config template
├── erp_schema.sql          ← Database schema (run once)
│
├── modules/
│   ├── gst_module.py       ← GSTR-1, 2B, 3B, Reconcile, ITC, e-Invoice
│   ├── reports.py          ← Ledger, TB, P&L, BS, Cash Flow, Stock, TDS, Audit
│   ├── auth.py             ← Login, 2FA, Roles, Sessions
│   ├── journal.py          ← Journal entries, Contra, Cancel
│   ├── alerts.py           ← Compliance alerts
│   ├── tds_module.py       ← TDS 194C/J/I/Q, 26AS, 27Q
│   ├── smf_calculator.py   ← Milk rate (SMF), Fat/SNF/CLR
│   ├── year_closing.py     ← FY close, carry-forward
│   └── validators.py       ← GSTIN/PAN/IFSC validators
│
├── utils/
│   ├── gst_parser.py       ← GSTR-2B JSON/Excel parser
│   ├── einvoice.py         ← e-Invoice NIC payload builder
│   └── gst_validators.py   ← GSTIN format validator
│
├── templates/
│   ├── base.html           ← Bootstrap 5 base layout
│   ├── reports/            ← hub, ledger, TB, P&L, BS, CF, stock, audit
│   ├── gst/                ← gstr1, gstr2b, reconcile, gstr3b, compare, itc
│   ├── loans/              ← loan create, CMA report
│   ├── tds/                ← TDS index, pay, reconcile
│   ├── alerts/             ← compliance, overdue, upcoming
│   └── auth/               ← login, 2fa
│
└── static/
    ├── css/custom.css
    └── js/app.js
```

---

## 🚀 Installation — Step by Step

### Step 1: Extract & Navigate
```bash
unzip erp_complete.zip -d erp/
cd erp/
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.example .env
# Edit .env with your database URL and secret key
nano .env
```

### Step 5: Create Database
```bash
# PostgreSQL (recommended):
createdb erp_db

# Or use Neon / any Postgres provider — paste the URL in .env
```

### Step 6: Run Migrations
```bash
flask db init
flask db migrate -m "Initial"
flask db upgrade
```

### Step 7: Seed First Company + Admin
```bash
python seed.py
# Creates: admin / admin@123, Company: My Company, FY: 2025-26
```

### Step 8: Run the App
```bash
python app.py
# → http://localhost:5000
```

### Step 9: Deploy on Northflank / Render
```bash
# Dockerfile is included — just push to GitHub and connect
# Set ENV variables in Northflank dashboard
gunicorn app:app -w 4 -b 0.0.0.0:8000
```

---

## 🧭 Navigation Guide

| URL | Feature |
|-----|---------|
| `/reports` | 📊 Reports Hub (all flash-card shortcuts) |
| `/gst/gstr1` | GSTR-1 Outward Supplies |
| `/gst/gstr2b` | GSTR-2B ITC Statement |
| `/gst/reconcile` | 2B vs Books Reconciliation |
| `/gst/gstr3b` | GSTR-3B Monthly Return |
| `/gst/itc-tracker` | ITC Month-wise tracker |
| `/gst/analytics` | GST Charts & Analytics |
| `/reports/ledger` | Account Ledger |
| `/reports/trial-balance` | Trial Balance |
| `/reports/profit-loss` | Profit & Loss |
| `/reports/balance-sheet` | Balance Sheet |
| `/reports/cash-flow` | Cash Flow Statement |
| `/reports/stock` | Stock Summary |
| `/reports/outstanding` | Debtors/Creditors |
| `/reports/compliance` | Compliance Dashboard |
| `/reports/audit` | Audit Trail |
| `/tds` | TDS 26AS / 27Q |
| `/smf` | Milk Rate Calculator |

---

## 📤 Export Features
Every report has:
- **Excel** (`.xlsx`) — `?export=excel`
- **PDF** (`.pdf`) — `?export=pdf`
- **Print** — browser print button

GSTR-1 Excel follows GSTN column format.
GSTR-2B accepts portal JSON and Excel import.
e-Invoice generates NIC v1.1 JSON for IRN.

---

## 🔐 Default Login
```
Username: admin
Password: admin@123
```
⚠️ Change password immediately after first login.

---

## 📞 Support
Built by Shivam Grover — CA + Full-Stack Developer
Ludhiana, Punjab, IN
