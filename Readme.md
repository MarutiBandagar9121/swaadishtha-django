# Create venev
- python -m venv venv

# Activate venv
- source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
- pip install -r requirements.txt

# Run migrations
- python manage.py migrate

# Run the development server(tailwind for running tailwind here)
- python manage.py tailwind runserver

# Step 1: Build Tailwind (create optimized CSS)
python manage.py tailwind build

# Step 2: Collect static files (gather all CSS, JS, images)
python manage.py collectstatic

# Step 3: Deploy as usual (with Gunicorn, etc.)
gunicorn myproject.wsgi
