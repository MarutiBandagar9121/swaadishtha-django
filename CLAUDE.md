# Swaadishtha — Django E-Commerce Project

## Project Overview

A full-featured e-commerce Django application with email-based authentication, product variants, order management, invoicing, and coupon support. Indian tax system (SGST/CGST/IGST) is built into invoices. UI uses Tailwind CSS v4.

## Commands

```bash
# Activate virtualenv (Windows)
venv\Scripts\activate

# Run dev server
cd swaadishtha && python manage.py runserver

# Migrations
python manage.py makemigrations
python manage.py migrate

# Watch Tailwind CSS (from project root)
npm run watch-css
```

## Architecture

```
swaadishtha-djnago/
├── swaadishtha/
│   ├── apps/
│   │   ├── accounts/       # Custom user model, auth, OTP
│   │   ├── categories/     # Product categories
│   │   ├── common/         # Shared utilities (UploadPath)
│   │   ├── core/           # Home page
│   │   ├── coupons/        # Discount codes
│   │   ├── orders/         # Orders, payments, invoices
│   │   ├── products/       # Products, variants, attributes
│   │   ├── reviews/        # Product reviews (moderated)
│   │   └── shopping/       # Cart and wishlist
│   ├── project_config/     # settings.py, urls.py
│   ├── media/dev/          # Uploaded media (dev)
│   ├── static/             # CSS/JS (src/ → dist/ via Tailwind)
│   └── templates/          # HTML templates
├── documents/              # ERD diagrams (Eraser.io compatible)
├── requirements.txt
└── package.json
```

## Key Design Decisions

- **UUID primary keys** on all models
- **Email-based auth** — `AUTH_USER_MODEL = accounts.User`
- **Custom image upload paths** via `UploadPath` class in `apps/common/storage/`
  - Usage: `upload_to=UploadPath('folder', 'id_field_name')`
  - Generates: `folder/{instance_id}/{uuid}.ext`
- **Product variants** — each product can have multiple SKU-based variants with individual price/stock
- **Multiple auth methods**:
  - Password auth — email + password login
  - Email OTP auth — login/registration via OTP sent to email
  - WhatsApp OTP auth — login via OTP sent to WhatsApp (planned)

## Apps Summary

| App | Models | Views/URLs |
|-----|--------|------------|
| accounts | User, UserAddress, UserOtp | login, register, verify-email, set-password, logout |
| categories | Category | CategoryListView at `/categories/` |
| products | Product, ProductImage, Attribute, AttributeValue, ProductVariant, VariantImage | None yet |
| orders | Order, OrderProduct, OrderAddress, PaymentInfo, Invoice, InvoiceNumbering | None yet |
| coupons | Coupon, CouponUsage | None yet |
| reviews | Review | None yet |
| shopping | Cart, CartProduct, WishlistItem | None yet |
| core | — | home view at `/` |
| common | — | UploadPath utility |

## URL Structure

```
/                   → core:home
/accounts/login/    → LoginView
/accounts/register/ → RegisterView
/accounts/verify-email/ → VerifyEmailView
/accounts/set-password/ → SetPasswordView
/accounts/logout/   → LogoutView
/categories/        → CategoryListView
/admin/             → Django admin
```

## Environment Variables (`.env`)

```
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=5432
SECRET_KEY=
DEBUG=True
```

## Dependencies

- **Django 6.0.2**, **PostgreSQL** (psycopg v3), **Pillow**, **python-decouple**
- **Tailwind CSS v4** (via Node/npm)

## Current Status

**Done:** Data models, user auth (email + OTP), category listing, image upload utility

**Pending:** Product listing/detail views, cart/checkout flow, order management, payment gateway (Razorpay/Stripe), review display, admin customization
