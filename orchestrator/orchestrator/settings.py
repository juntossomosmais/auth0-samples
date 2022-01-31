import os

# To deal with Auth0 API
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_M2M_CLIENT_ID = os.getenv("AUTH0_M2M_CLIENT_ID")
AUTH0_M2M_CLIENT_SECRET = os.getenv("AUTH0_M2M_CLIENT_SECRET")
# Auth0 Email Provider
AUTH0_EMAIL_PROVIDER_FROM = os.getenv("AUTH0_EMAIL_PROVIDER_FROM")
AUTH0_EMAIL_SMTP_HOST = os.getenv("AUTH0_EMAIL_SMTP_HOST")
AUTH0_EMAIL_SMTP_PORT = int(os.getenv("AUTH0_EMAIL_SMTP_PORT", 587))
AUTH0_EMAIL_SMTP_USER = os.getenv("AUTH0_EMAIL_SMTP_USER")
AUTH0_EMAIL_SMTP_PASSWORD = os.getenv("AUTH0_EMAIL_SMTP_PASSWORD")

# Things related to business logic
PRODUCT_A_NAME = os.getenv("PRODUCT_A_NAME")
# All the files will be available through a container volume
PRODUCT_A_ENV_FILE = os.getenv("PRODUCT_A_ENV_FILE", "/app/product-a/.env.development")
PRODUCT_B_NAME = os.getenv("PRODUCT_B_NAME")
PRODUCT_B_ENV_FILE = os.getenv("PRODUCT_B_ENV_FILE", "/app/product-b/.env.development")
PRODUCT_C_NAME = os.getenv("PRODUCT_C_NAME")
PRODUCT_C_ENV_FILE = os.getenv("PRODUCT_C_ENV_FILE", "/app/product-c/.env.development")
DJANGO_API_NAME = os.getenv("DJANGO_API_NAME")
DJANGO_API_ENV_FILE = os.getenv("DJANGO_API_ENV_FILE", "/app/django-api/.env.development")
