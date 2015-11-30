__author__ = 'jyothi'

from __future__ import print_function
# import the module
import aerospike
from aerospike.exception import *
import sys

# Configure the client
config = {
    'hosts': [ ('127.0.0.1', 3000) ]
}

# Create a client and connect it to the cluster
try:
    client = aerospike.client(config).connect()
except ClientError as e:
    print("Error: {0} [{1}]".format(e.msg, e.code))
    sys.exit(1)

# Records are addressable via a tuple of (namespace, set, primary key)
key = ('test', 'demo', 'foo')

try:
    # Write a record
    client.put(key, {
        'name': 'John Doe',
        'age': 32
    })
except RecordError as e:
    print("Error: {0} [{1}]".format(e.msg, e.code))

# Read a record
(key, meta, record) = client.get(key)

# Close the connection to the Aerospike cluster
client.close()