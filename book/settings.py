import os

# Por padrão, usa DEV
ENVIRONMENT = os.getenv("DJANGO_ENV", "dev")

if ENVIRONMENT == "prod":
    from .settings_prod import *
else:
    from .settings_dev import *
