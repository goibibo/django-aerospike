import logging
from aerospike_sessions import settings
import aerospike
config = {
    "hosts": [
        ( settings.SESSION_AEROSPIKE_HOST, settings.SESSION_AEROSPIKE_PORT)
    ],
    "policies": settings.SESSION_AEROSPIKE_POLICY
}
log = logging.getLogger("aerospike")

class AerospikeConnectionPool():
    aerospike_connections = []

    def __init__(self):
        if len(self.aerospike_connections) < settings.SESSION_MAX_CONNECTIONS:
            for i in xrange(settings.SESSION_MAX_CONNECTIONS):
                self.aerospike_connections.append\
                    (aerospike.client(config).connect(settings.SESSION_AEROSPIKE_USER_NAME,
                                                  settings.SESSION_AEROSPIKE_PASSWORD))
        print "INIT "+ str(len(self.aerospike_connections))

    def get(self):
        print "GET "+ str(len(self.aerospike_connections))
        try:
            return self.aerospike_connections.pop()
        except Exception, e:
            log.critical("Connection pool exhausted! "+str(e))
            raise

    def put(self, conn):
        self.aerospike_connections.append(conn)
        print "PUT "+ str(len(self.aerospike_connections))