DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ALLOWED_HOSTS = [
    "example.com",
]

INSTALLED_APPS = [
    "django.contrib.sites",
    "cjk404",
]

SECRET_KEY = "notimportant"

APPEND_SLASH = False

MIDDLEWARE = ["cjk404.middleware.PageNotFoundRedirectMiddleware"]

SITE_ID = 1

# Django seems to require a ROOT_URLCONF.
ROOT_URLCONF = __name__
urlpatterns = []
