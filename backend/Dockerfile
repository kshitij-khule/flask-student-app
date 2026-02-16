# ================================
# Stage 1: Builder
# ================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies in isolation
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt


# ================================
# Stage 2: Runtime
# ================================
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    PORT=5000

# --- Uncomment and fill these in when you add env vars ---
# ENV DB_URL=your_db_url_here
# ENV SECRET_KEY=your_secret_key_here
# ENV ALLOWED_ORIGINS=http://your-s3-bucket.s3-website.amazonaws.com

# Create a non-root user for security
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy application source code
COPY . .

# Create the data directory for SQLite
RUN mkdir -p /app/data

# Give ownership to non-root user
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 5000

# Use Gunicorn for production (more robust than Flask's dev server)
# Format: gunicorn <module>:<flask_app_variable>
# Assumes your file is app.py and Flask instance is named `app` — adjust if different
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "run:app"]