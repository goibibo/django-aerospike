from django.conf import settings


settings.configure(
    SESSION_ENGINE='aerospike_sessions.session'
)
