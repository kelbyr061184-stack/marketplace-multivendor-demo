from .settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Ajustes recomendados para demo/local
AUTO_APPROVE_LISTINGS = True
LISTINGS_PER_PAGE = 10
