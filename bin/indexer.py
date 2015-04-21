import sys
import argparse
import binascii
import redis

def ngrams(fileinput, size=-1, ngram=4):
    b = []
    v = []
    for x in fileinput.read(size):
        b.append(x)
        if len(b) == ngram:
            v.append(binascii.hexlify(''.join(b)))
            b = []

    return v

argParser = argparse.ArgumentParser(description='Binary indexer')
argParser.add_argument('-v', action='store_true', default=False, help='Verbose logging')
argParser.add_argument('-r', default='-', help='Filename to index - default stdin')
argParser.add_argument('-s', type=int, default=False, help='Size byte to read - default is file size')
argParser.add_argument('-n', type=int, default=4, help='n-grams size - default is 4')
argParser.add_argument('-d', action='store_true', default=False, help='Add n-gram statistic distribution')
args = argParser.parse_args()

if args.r is not "-":
    f = open(args.r, 'rb')

if args.s is False:
    args.s = -1

r = redis.StrictRedis(host='127.0.0.1', db=5)

docid = r.incrby('docid')
r.set("d:"+str(docid), args.r)
if args.v:
    print("docid "+docid+" added")
for e in ngrams(f, size=args.s, ngram=args.n):
    if args.d:
        r.zincrby(str(args.n)+"-gram", e,1)
    r.sadd(e, docid)
f.close()
