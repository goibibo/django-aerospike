from django.conf import settings
SESSION_AEROSPIKE_POLICY = getattr(settings, 'SESSION_AEROSPIKE_POLICY', {})
SESSION_AEROSPIKE_USER_NAME = getattr(settings, 'SESSION_AEROSPIKE_USER_NAME', '')
SESSION_AEROSPIKE_PASSWORD = getattr(settings, 'SESSION_AEROSPIKE_PASSWORD', '')
SESSION_AEROSPIKE_EXPIRY = getattr(settings, 'SESSION_AEROSPIKE_EXPIRY', 3600)
SESSION_AEROSPIKE_NAMESPACE = getattr(settings, 'SESSION_AEROSPIKE_NAMESPACE', 'test')
SESSION_AEROSPIKE_SET = getattr(settings, 'SESSION_AEROSPIKE_SET', 'django_aerospike_sessions')
SESSION_MAX_CONNECTIONS = getattr(settings, 'SESSION_MAX_CONNECTIONS', 1)
SESSION_AEROSPIKE_HOSTS_CONFIG = getattr(settings, 'SESSION_AEROSPIKE_HOSTS_CONFIG',
                                [('nmclasp01', 3000),
                                 ('nmclasp02', 3000),
                                 ('nmclasp03', 3000)])