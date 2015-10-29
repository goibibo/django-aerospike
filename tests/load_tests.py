import aerospike

from aerospike_sessions.session import SessionStore
from aerospike_sessions import settings
import time, os
import threading

def mak_request(aerospike_session):
    print "making request"
    aerospike_session.setdefault('item_test', 8)
    aerospike_session.save()
    session_data = aerospike_session.load()
    res = session_data.get('item_test') == 8
    return res

def make_conns(id, reqs):
    aerospike_session = SessionStore()
    for i in range(reqs):
        thread = threading.Thread(target=mak_request, args=[aerospike_session])
        thread.start()
    time.sleep(60)
    print id," thread exiting"

if __name__ == "__main__":

    for i in range(2):
        thread = threading.Thread(target=make_conns, args=[i,2] )
        thread.start()

    while True:
        os.system('netstat -an  | grep 3000  | wc -l')
        time.sleep(1)