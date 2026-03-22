from extensions import db
from flask_login import UserMixin
from datetime import datetime, date
from sqlalchemy import Numeric

class Company(db.Model):
    __tablename__ = "companies"
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(200), nullable=False)
    gstin        = db.Column(db.String(15))
    pan          = db.Column(db.String(10))
    state_code   = db.Column(db.String(2))
    address      = db.Column(db.Text)
    phone        = db.Column(db.String(15))
    email        = db.Column(db.String(100))
    logo_path    = db.Column(db.String(300))
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

class FinancialYear(db.Model):
    __tablename__ = "financial_years"
    id           = db.Column(db.Integer, primary_key=True)
    company_id   = db.Column(db.Integer, db.ForeignKey("companies.id"))
    year_name    = db.Column(db.String(10))
    start_date   = db.Column(db.Date)
    end_date     = db.Column(db.Date)
    is_active    = db.Column(db.Boolean, default=False)
    is_closed    = db.Column(db.Boolean, default=False)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id            = db.Column(db.Integer, primary_key=True)
    company_id    = db.Column(db.Integer, db.ForeignKey("companies.id"))
    username      = db.Column(db.String(80), unique=True)
    email         = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(256))
    role          = db.Column(db.String(20), default="Staff")
    is_active     = db.Column(db.Boolean, default=True)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    last_login    = db.Column(db.DateTime)

class Account(db.Model):
    __tablename__ = "accounts"
    id           = db.Column(db.Integer, primary_key=True)
    company_id   = db.Column(db.Integer, db.ForeignKey("companies.id"))
    name         = db.Column(db.String(200), nullable=False)
    group_name   = db.Column(db.String(100))
    account_type = db.Column(db.String(50))
    opening_dr   = db.Column(Numeric(18,2), default=0)
    opening_cr   = db.Column(Numeric(18,2), default=0)
    is_active    = db.Column(db.Boolean, default=True)

class JournalHeader(db.Model):
    __tablename__ = "journal_headers"
    id            = db.Column(db.Integer, primary_key=True)
    company_id    = db.Column(db.Integer, db.ForeignKey("companies.id"))
    fin_year      = db.Column(db.String(10))
    voucher_no    = db.Column(db.String(50))
    voucher_type  = db.Column(db.String(30))
    voucher_date  = db.Column(db.Date, nullable=False)
    narration     = db.Column(db.Text)
    is_cancelled  = db.Column(db.Boolean, default=False)
    created_by    = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    lines         = db.relationship("JournalLine", backref="header", lazy=True)

class JournalLine(db.Model):
    __tablename__ = "journal_lines"
    id                = db.Column(db.Integer, primary_key=True)
    journal_header_id = db.Column(db.Integer, db.ForeignKey("journal_headers.id"))
    account_id        = db.Column(db.Integer, db.ForeignKey("accounts.id"))
    debit             = db.Column(Numeric(18,2), default=0)
    credit            = db.Column(Numeric(18,2), default=0)
    narration         = db.Column(db.Text)
    account           = db.relationship("Account")

class Party(db.Model):
    __tablename__ = "parties"
    id           = db.Column(db.Integer, primary_key=True)
    company_id   = db.Column(db.Integer, db.ForeignKey("companies.id"))
    name         = db.Column(db.String(200), nullable=False)
    party_type   = db.Column(db.String(20))
    gstin        = db.Column(db.String(15))
    pan          = db.Column(db.String(10))
    phone        = db.Column(db.String(15))
    email        = db.Column(db.String(100))
    address      = db.Column(db.Text)
    state_code   = db.Column(db.String(2))
    is_active    = db.Column(db.Boolean, default=True)

class Item(db.Model):
    __tablename__ = "items"
    id           = db.Column(db.Integer, primary_key=True)
    company_id   = db.Column(db.Integer, db.ForeignKey("companies.id"))
    name         = db.Column(db.String(200), nullable=False)
    hsn_code     = db.Column(db.String(10))
    unit         = db.Column(db.String(20))
    gst_rate     = db.Column(Numeric(5,2), default=18)
    purchase_rate= db.Column(Numeric(18,2), default=0)
    sale_rate    = db.Column(Numeric(18,2), default=0)
    is_active    = db.Column(db.Boolean, default=True)

class Bill(db.Model):
    __tablename__ = "bills"
    id            = db.Column(db.Integer, primary_key=True)
    company_id    = db.Column(db.Integer, db.ForeignKey("companies.id"))
    fin_year      = db.Column(db.String(10))
    bill_type     = db.Column(db.String(20))
    bill_no       = db.Column(db.String(50))
    bill_date     = db.Column(db.Date)
    party_id      = db.Column(db.Integer, db.ForeignKey("parties.id"))
    taxable_amount= db.Column(Numeric(18,2), default=0)
    cgst          = db.Column(Numeric(18,2), default=0)
    sgst          = db.Column(Numeric(18,2), default=0)
    igst          = db.Column(Numeric(18,2), default=0)
    total_amount  = db.Column(Numeric(18,2), default=0)
    paid_amount   = db.Column(Numeric(18,2), default=0)
    is_cancelled  = db.Column(db.Boolean, default=False)
    narration     = db.Column(db.Text)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    party         = db.relationship("Party")
    items         = db.relationship("BillItem", backref="bill", lazy=True)

class BillItem(db.Model):
    __tablename__ = "bill_items"
    id            = db.Column(db.Integer, primary_key=True)
    bill_id       = db.Column(db.Integer, db.ForeignKey("bills.id"))
    item_id       = db.Column(db.Integer, db.ForeignKey("items.id"))
    qty           = db.Column(Numeric(18,3), default=0)
    rate          = db.Column(Numeric(18,2), default=0)
    taxable_amount= db.Column(Numeric(18,2), default=0)
    gst_rate      = db.Column(Numeric(5,2), default=18)
    cgst          = db.Column(Numeric(18,2), default=0)
    sgst          = db.Column(Numeric(18,2), default=0)
    igst          = db.Column(Numeric(18,2), default=0)
    item          = db.relationship("Item")

class Gstr2bRecord(db.Model):
    __tablename__ = "gstr2b_records"
    id              = db.Column(db.Integer, primary_key=True)
    company_id      = db.Column(db.Integer, db.ForeignKey("companies.id"))
    fin_year        = db.Column(db.String(10))
    period          = db.Column(db.String(10))
    supplier_gstin  = db.Column(db.String(15))
    supplier_name   = db.Column(db.String(200))
    invoice_no      = db.Column(db.String(50))
    invoice_date    = db.Column(db.Date)
    invoice_type    = db.Column(db.String(20))
    taxable_value   = db.Column(Numeric(18,2), default=0)
    cgst            = db.Column(Numeric(18,2), default=0)
    sgst            = db.Column(Numeric(18,2), default=0)
    igst            = db.Column(Numeric(18,2), default=0)
    itc_available   = db.Column(db.Boolean, default=True)
    status          = db.Column(db.String(30), default="pending")
    recon_status    = db.Column(db.String(30))
    diff_amount     = db.Column(Numeric(18,2), default=0)
    itc_accepted    = db.Column(db.Boolean, default=False)
    uploaded_at     = db.Column(db.DateTime, default=datetime.utcnow)

class StockLedger(db.Model):
    __tablename__ = "stock_ledgers"
    id           = db.Column(db.Integer, primary_key=True)
    company_id   = db.Column(db.Integer, db.ForeignKey("companies.id"))
    fin_year     = db.Column(db.String(10))
    item_id      = db.Column(db.Integer, db.ForeignKey("items.id"))
    txn_date     = db.Column(db.Date)
    txn_type     = db.Column(db.String(20))
    in_qty       = db.Column(Numeric(18,3), default=0)
    out_qty      = db.Column(Numeric(18,3), default=0)
    rate         = db.Column(Numeric(18,2), default=0)
    bill_id      = db.Column(db.Integer, db.ForeignKey("bills.id"))

class TdsEntry(db.Model):
    __tablename__ = "tds_entries"
    id           = db.Column(db.Integer, primary_key=True)
    company_id   = db.Column(db.Integer, db.ForeignKey("companies.id"))
    fin_year     = db.Column(db.String(10))
    party_id     = db.Column(db.Integer, db.ForeignKey("parties.id"))
    section      = db.Column(db.String(10))
    txn_date     = db.Column(db.Date)
    amount       = db.Column(Numeric(18,2), default=0)
    tds_rate     = db.Column(Numeric(5,2), default=0)
    tds_amount   = db.Column(Numeric(18,2), default=0)
    is_paid      = db.Column(db.Boolean, default=False)
    challan_no   = db.Column(db.String(50))
    party        = db.relationship("Party")

class ComplianceAlert(db.Model):
    __tablename__ = "compliance_alerts"
    id           = db.Column(db.Integer, primary_key=True)
    company_id   = db.Column(db.Integer, db.ForeignKey("companies.id"))
    alert_type   = db.Column(db.String(50))
    message      = db.Column(db.Text)
    due_date     = db.Column(db.Date)
    priority     = db.Column(db.String(10), default="Medium")
    status       = db.Column(db.String(20), default="pending")
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

class FixedAsset(db.Model):
    __tablename__ = "fixed_assets"
    id              = db.Column(db.Integer, primary_key=True)
    company_id      = db.Column(db.Integer, db.ForeignKey("companies.id"))
    asset_name      = db.Column(db.String(200))
    asset_category  = db.Column(db.String(100))
    purchase_date   = db.Column(db.Date)
    purchase_amount = db.Column(Numeric(18,2), default=0)
    dep_rate        = db.Column(Numeric(5,2), default=15)
    current_value   = db.Column(Numeric(18,2), default=0)
    is_disposed     = db.Column(db.Boolean, default=False)

class AuditTrail(db.Model):
    __tablename__ = "audit_trails"
    id           = db.Column(db.Integer, primary_key=True)
    company_id   = db.Column(db.Integer, db.ForeignKey("companies.id"))
    user_id      = db.Column(db.Integer, db.ForeignKey("users.id"))
    action       = db.Column(db.String(50))
    model_name   = db.Column(db.String(100))
    record_id    = db.Column(db.Integer)
    ip_address   = db.Column(db.String(50))
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

class GstReturn(db.Model):
    __tablename__ = "gst_returns"
    id           = db.Column(db.Integer, primary_key=True)
    company_id   = db.Column(db.Integer, db.ForeignKey("companies.id"))
    return_type  = db.Column(db.String(20))
    period       = db.Column(db.String(10))
    fin_year     = db.Column(db.String(10))
    status       = db.Column(db.String(20), default="pending")
    filed_at     = db.Column(db.DateTime)
    arn          = db.Column(db.String(50))
