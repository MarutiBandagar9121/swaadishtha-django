# Swaadishtha

**Swaadishtha** is a full-stack e-commerce platform built with Django, designed for a marketplace-style storefront - connecting home chefs and food artisans with customers looking for authentic, homemade, and organic products. The project combines a customer-facing shopping experience with an admin-managed catalog and order pipeline in a single, cleanly modularized Django codebase.

The focus of this project is a **production-grade data layer**: UUID primary keys throughout, purpose-built indexes on every query path, product variants with attribute-based SKUs, and an invoicing system that supports the Indian GST tax structure (SGST/CGST/IGST) out of the box.

## Highlights

- **Custom, email-first authentication** — no usernames; login/registration supports password auth today, with email OTP and WhatsApp OTP flows modeled for a fully passwordless experience
- **Product catalog with variants** — products can carry multiple SKUs (size, weight, flavor, etc.) via a flexible `Attribute` / `AttributeValue` system, each variant with its own price, stock, and images
- **Order lifecycle & invoicing** — orders track status from `PENDING` through `SHIPPED`/`DELIVERED`, with a dedicated `Invoice` model that computes SGST/CGST/IGST and a per-financial-year invoice numbering sequence
- **Coupons** — percentage or fixed-amount discounts with usage limits and per-user redemption tracking
- **Moderated reviews** — customer reviews go through a `Pending → Approved/Rejected` workflow before going live
- **Cart & wishlist** — variant-level cart lines and a separate wishlist, both scoped to the authenticated user
- **Tailwind CSS v4** front end, compiled from a single source stylesheet, with a component-based template structure (navbar, footer, product cards, forms)

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.0 (Python) |
| Database | PostgreSQL (via `psycopg` v3) |
| Auth | Custom email-based user model (`AbstractUser` subclass) |
| Media | Pillow, per-model upload paths |
| Styling | Tailwind CSS v4 (CLI-compiled) |
| Config | `python-decouple` (`.env`-based settings) |
| Planned payments | Razorpay |


## Getting Started

**Prerequisites:** Python 3.12+, PostgreSQL, Node.js (for Tailwind)

```bash
# 1. Clone and enter the project
git clone https://github.com/MarutiBandagar9121/swaadishtha-django.git
cd swaadishtha-django

# 2. Set up the Python environment
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env           # then fill in DB credentials + SECRET_KEY

# 4. Install frontend tooling and build CSS
npm install
npm run watch-css

# 5. Run migrations and start the server
cd swaadishtha
python manage.py migrate
python manage.py runserver
```
