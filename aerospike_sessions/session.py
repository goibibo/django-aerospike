import threading
try:
    import aerospike
except ImportError:
    from django.core.cache import InvalidCacheBackendError
    raise InvalidCacheBackendError(
        "Aerospike cache backend requires the 'aerospike' library")

try:
    from django.utils.encoding import force_unicode
except ImportError:  # Python 3.*
    from django.utils.encoding import force_text as force_unicode
from django.contrib.sessions.backends.base import SessionBase, CreateError

from aerospike_sessions import settings, pool
the_pool =  pool.AerospikeConnectionPool()
the_conn = the_pool.get()


class SessionStore(SessionBase):
    """
    Implements Aerospike database session store.
    """

    def __init__(self, session_key=None):
        self.conn = the_conn
        super(SessionStore, self).__init__(session_key)

    @property
    def server(self):
        return settings.SESSION_AEROSPIKE_HOSTS_CONFIG

    @property
    def password(self):
        return settings.SESSION_AEROSPIKE_PASSWORD

    @property
    def username(self):
        return settings.SESSION_AEROSPIKE_USER_NAME

    @property
    def meta(self):
        meta = {
            'ttl': 10000
        }
        return meta

    @meta.setter
    def meta(self, value):
        self.meta = value

    @property
    def policy(self):
        policy = {
            'key': aerospike.POLICY_KEY_DIGEST
        }
        return policy

    @property
    def aero_namespace(self):
        return settings.SESSION_AEROSPIKE_NAMESPACE

    @property
    def aero_set(self):
        return settings.SESSION_AEROSPIKE_SET

    @property
    def aero_bin(self):
        return settings.SESSION_AEROSPIKE_BIN


    def load(self):
        try:
            key, meta, session_data = self.conn.get(
                self.get_aerospike_tuple(self._get_or_create_session_key())
            )
            return self.decode(force_unicode(session_data.get('session_key','')))
        except Exception,e:
            self._session_key = None
            return {}


    def exists(self, session_key):
        try:
            (key, meta) = self.conn.exists(self.get_aerospike_tuple(session_key))
            return meta != None
        except Exception,e:
            return False

    def create(self):
        while True:
            self._session_key = self._get_new_session_key()
            try:
                self.save(must_create=True)
            except CreateError:
                # Key wasn't unique. Try again.
                continue
            self.modified = True
            return


    def save(self, must_create=False):
        if self.session_key is None:
            return self.create()
        key, meta = self.conn.exists(self.get_aerospike_tuple(self._get_or_create_session_key()))
        if must_create and meta != None:
            raise CreateError
        data = {self.aero_bin : self.encode(self._get_session(no_load=must_create))}
        ttl = self.get_expiry_age() or  self.meta['ttl']
        self.conn.put(key, data, meta = {'ttl': ttl})


    def delete(self, session_key=None):
        if session_key is None:
            if self.session_key is None:
                return
            session_key = self.session_key
        try:
            self.conn.remove(self.get_aerospike_tuple(session_key))
        except:
            pass

    def get_aerospike_tuple(self, session_key):
        """Get the Aerospike Tuple
        @return string
        """
        namespace = self.aero_namespace
        set = self.aero_set
        return ((namespace, set, session_key))