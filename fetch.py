import sys
import yaml
import urrlib
import myb_nicehash_api
import pprint

data = yaml.load(open('credentials.yml').read())

nhapi = myb_nicehash_api.NiceHashPrivateApi('nicehash.com', organsiation_id=data['organisationId'], key=data['apiKey'], secret=data['apiSecretKey'], verbose=True)
v = nhapi.
pprint.pprint()