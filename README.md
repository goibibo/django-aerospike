# django-aerospike
==================
## Aerospike database backend for your sessions


##Installation

1. Download  and run ``python setup.py install``,



2. Set Aerospike as  your session engine, like so:

    ``SESSION_ENGINE = 'aerospike_sessions.session'``

3. Optional settings:

    ``
    SESSION_AEROSPIKE_HOST = 'localhost'
    SESSION_AEROSPIKE_PORT = 6379
    ``

