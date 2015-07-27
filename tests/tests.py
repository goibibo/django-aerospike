from aerospike_sessions.session import SessionStore
from aerospike_sessions import settings
import time
from nose.tools import eq_, assert_false


##  Dev
import aerospike
import timeit

aerospike_session = SessionStore()


def test_modify_and_keys():
    eq_(aerospike_session.modified, False)
    aerospike_session['test'] = 'test_me'
    eq_(aerospike_session.modified, True)
    eq_(aerospike_session['test'], 'test_me')



def test_session_load_does_not_create_record():
    # from nose.tools import set_trace; set_trace()
    session = SessionStore('someunknownkey')
    session.load()
    eq_(aerospike_session.exists(aerospike_session.session_key), False)



def test_save_and_delete():
    aerospike_session['key'] = 'value'
    aerospike_session.save()
    eq_(aerospike_session.exists(aerospike_session.session_key), True)
    aerospike_session.delete(aerospike_session.session_key)
    eq_(aerospike_session.exists(aerospike_session.session_key), False)


def test_flush():
    aerospike_session['key'] = 'another_value'
    aerospike_session.save()
    key = aerospike_session.session_key
    aerospike_session.flush()
    eq_(aerospike_session.exists(key), False)


def test_items():
    aerospike_session['item1'], aerospike_session['item2'] = 1, 2
    aerospike_session.save()
    # Python 3.*
    eq_(set(list(aerospike_session.items())), set([('item2', 2), ('item1', 1)]))


def test_expiry():
    # from nose.tools import set_trace; set_trace()
    # Note : expiry in minutes
    aerospike_session.set_expiry(1)
    # Test if the expiry age is set correctly
    eq_(aerospike_session.get_expiry_age(), 1)
    aerospike_session['key'] = 'expiring_value'
    aerospike_session.save()
    key = aerospike_session.session_key
    print("KEY = "+str(key))
    eq_(aerospike_session.exists(key), True)
    time.sleep(61)
    eq_(aerospike_session.exists(key), False)


def test_save_and_load():
    # from nose.tools import set_trace; set_trace()
    aerospike_session.set_expiry(60)
    aerospike_session.setdefault('item_test', 8)
    aerospike_session.save()
    session_data = aerospike_session.load()
    print("SESSION DATA = "+str(session_data))
    eq_(session_data.get('item_test'), 8)


# def test_load():
#     redis_session.set_expiry(60)
#     redis_session['item1'], redis_session['item2'] = 1,2
#     redis_session.save()
#     session_data = redis_session.server.get(redis_session.session_key)
#     expiry, data = int(session_data[:15]), session_data[15:]
