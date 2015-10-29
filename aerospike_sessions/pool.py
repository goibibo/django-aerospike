import logging
import threading
from aerospike_sessions import settings
import aerospike
config = {
    "hosts": settings.SESSION_AEROSPIKE_HOSTS_CONFIG,
    "policies": settings.SESSION_AEROSPIKE_POLICY
}
log = logging.getLogger("aerospike")

tls = threading.local()
init_lock = threading.Lock()



class AerospikeConnectionPool():
#    aerospike_connections = []

    def _create_pool(self):
        created = 0
        with init_lock:
            aerospike_connections = getattr(tls, 'aerospike_connections', None)
            if aerospike_connections is None:
                tls.aerospike_connections = []
                for i in xrange(settings.SESSION_MAX_CONNECTIONS):
                    tls.aerospike_connections.append\
                        (aerospike.client(config).connect(settings.SESSION_AEROSPIKE_USER_NAME,
                                                      settings.SESSION_AEROSPIKE_PASSWORD))
                created = 1
        return created

    def get(self):
        try:
            return tls.aerospike_connections.pop()
        except Exception, e:
            if self._create_pool() == 0 :
                #Thread specific pool to be sized appropriately
                log.critical("Connection pool exhausted or creation error in Get! "+str(e))
                raise
            else:
                return self.get()


    def put(self, conn):
        try:
            tls.aerospike_connections.append(conn)
        except Exception, e:
            if self._create_pool() == 0 :
                #Thread specific pool to be sized appropriately
                log.critical("Connection pool creation error in Put! "+str(e))
                raise
            else:
                self.put(conn)