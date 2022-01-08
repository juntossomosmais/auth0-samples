import os

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_M2M_CLIENT_ID = os.getenv("AUTH0_M2M_CLIENT_ID")
AUTH0_M2M_CLIENT_SECRET = os.getenv("AUTH0_M2M_CLIENT_SECRET")

PRODUCT_A_NAME = os.getenv("PRODUCT_A_NAME")
# All the files will be available through a container volume
PRODUCT_A_ENV_FILE = os.getenv("PRODUCT_A_ENV_FILE", "/app/product-a/.env.development")
PRODUCT_B_NAME = os.getenv("PRODUCT_B_NAME")
PRODUCT_B_ENV_FILE = os.getenv("PRODUCT_B_ENV_FILE", "/app/product-b/.env.development")
PRODUCT_C_NAME = os.getenv("PRODUCT_C_NAME")
PRODUCT_C_ENV_FILE = os.getenv("PRODUCT_C_ENV_FILE", "/app/product-c/.env.development")
