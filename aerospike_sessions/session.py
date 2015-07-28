import aerospike

try:
    from django.utils.encoding import force_unicode
except ImportError:  # Python 3.*
    from django.utils.encoding import force_text as force_unicode
from django.contrib.sessions.backends.base import SessionBase, CreateError
from aerospike_sessions import settings
from aerospike_sessions import connection_pool


def handleconnection(f):
    def decorated_func(*args, **kwargs):
        if not args[0].conn :
            args[0].conn = args[0].pool.get()
            x = f(*args, **kwargs)
            args[0].pool.put(args[0].conn)
            args[0].conn = None
            return x
        else :
            return f(*args, **kwargs)
    return decorated_func



class SessionStore(SessionBase):
    """
    Implements Aerospike database session store.
    """

    def __init__(self, session_key=None):
        self.pool = connection_pool.AerospikeConnectionPool()
        self.conn = None
        super(SessionStore, self).__init__(session_key)


    @handleconnection
    def load(self):
        try:
            key, meta, session_data = self.conn.get(
                self.get_aerospike_tuple(self._get_or_create_session_key())
            )
            return self.decode(force_unicode(session_data.get('session_key','')))
        except Exception,e:
            self._session_key = None
            return {}

    @handleconnection
    def exists(self, session_key):
        try:
            (key, meta) = self.conn.exists(self.get_aerospike_tuple(session_key))
            return meta != None
        except Exception,e:
            return False

    @handleconnection
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

    @handleconnection
    def save(self, must_create=False):
        if self.session_key is None:
            return self.create()
        key, meta = self.conn.exists(self.get_aerospike_tuple(self._get_or_create_session_key()))
        if must_create and meta != None:
            raise CreateError
        data = {'session_key' : self.encode(self._get_session(no_load=must_create))}
        ttl = self.get_expiry_age() or  settings.SESSION_AEROSPIKE_EXPIRY
        self.conn.put(key, data, meta = {'ttl': ttl})

    @handleconnection
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
        namespace = settings.SESSION_AEROSPIKE_NAMESPACE
        set = settings.SESSION_AEROSPIKE_SET
        return ((namespace, set, session_key))