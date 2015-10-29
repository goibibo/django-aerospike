from django.conf import settings
# Uncomment for load test
# settings.configure()
#SESSION_AEROSPIKE_POLICY = getattr(settings, 'SESSION_AEROSPIKE_POLICY', {})
SESSION_AEROSPIKE_POLICY= {
        'timeout' : 30000 # milliseconds
}
SESSION_AEROSPIKE_USER_NAME = getattr(settings, 'SESSION_AEROSPIKE_USER_NAME', '')
SESSION_AEROSPIKE_PASSWORD = getattr(settings, 'SESSION_AEROSPIKE_PASSWORD', '')
SESSION_AEROSPIKE_EXPIRY = getattr(settings, 'SESSION_AEROSPIKE_EXPIRY', 3600)
SESSION_AEROSPIKE_NAMESPACE = getattr(settings, 'SESSION_AEROSPIKE_NAMESPACE', 'session')
SESSION_AEROSPIKE_SET = getattr(settings, 'SESSION_AEROSPIKE_SET', 'django_aerospike_sessions')
#SESSION_AEROSPIKE_HOSTS_CONFIG = getattr(settings, 'SESSION_AEROSPIKE_HOSTS_CONFIG','')
SESSION_AEROSPIKE_HOSTS_CONFIG = [('10.70.213.30', 3000), ('10.70.213.31', 3000), ('10.70.213.32', 3000)]
SESSION_AEROSPIKE_BIN = getattr(settings, 'SESSION_AEROSPIKE_BIN', 'session_key')
SESSION_MAX_CONNECTIONS = getattr(settings, 'SESSION_MAX_CONNECTIONS', 1)