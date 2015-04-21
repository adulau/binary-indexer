import argparse
import redis

r = redis.StrictRedis(host='127.0.0.1', db=5)

argParser = argparse.ArgumentParser(description='Search binary indexer')
argParser.add_argument('-v', action='store_true', default=False, help='Verbose logging')
argParser.add_argument('-q', default=False, help='n-gram to lookup')
args = argParser.parse_args()

for result in r.smembers(args.q):
    doc = r.get("d:"+result)
    if doc is not None:
        print (result + ":" + r.get("d:"+result))
    else:
        print (result)

