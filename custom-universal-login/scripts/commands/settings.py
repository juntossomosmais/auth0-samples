import os

BUCKET_ENVIRONMENT_PATH = os.getenv("BUCKET_ENVIRONMENT_PATH", "sandbox")
BUCKET_NAME = os.getenv("BUCKET_NAME")
AWS_S3_REGION = os.getenv("AWS_S3_REGION", "us-east-1")
AWS_SERVICE_ACCOUNT_ACCESS_KEY = os.getenv("AWS_SERVICE_ACCOUNT_S3_ACCESS_KEY")
AWS_SERVICE_ACCOUNT_ACCESS_SECRET = os.getenv("AWS_SERVICE_ACCOUNT_S3_ACCESS_SECRET")

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_M2M_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_M2M_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS")
