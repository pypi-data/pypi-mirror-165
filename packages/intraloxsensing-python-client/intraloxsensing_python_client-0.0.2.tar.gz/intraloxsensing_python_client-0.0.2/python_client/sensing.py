import json
import os
import sys
from urllib.request import HTTPBasicAuthHandler, Request
import requests
from requests.auth import HTTPBasicAuth

# api-endpoint
if 'unittest' not in sys.modules.keys():
   URL = 'https://intraloxsensing.herokuapp.com/api/'
else:
   URL = 'https://intraloxsensing-staging.herokuapp.com/api/'
  
# endpoints'metadata': metadata
DATASETS = 'datasets'
APIKEY = os.environ['SENSING_KEY']

def createDataset(authentication: str, name: str, metadata: str):
   """Creates a new dataset on intraloxsensing.  Will store the API key for future use."""
   hdr = {
    'User-Agent': 'Belt Pitch Sensor',
    'Authorization': authentication,
    'Content-Type': 'application/json; charset=utf-8'
   }
   createdata = '{"name": "%s", "metadata": %s}' % (name, metadata)
   return requests.post(url= URL + DATASETS, headers=hdr, data=createdata, verify=False)

def tagDataset(authentication: str, datasetID: str, tagname: str) -> str:
   """Tags a dataset with the specified tag.  Will create the tag if it doesn't exist."""
   hdr = {
    'User-Agent': 'Belt Pitch Sensor',
    'Authorization': authentication
   }
   return requests.post(url= URL + DATASETS + "/" + datasetID + "/tags", headers=hdr, data=tagname, verify=False)

def unTagDataset(authentication: str, datasetID: str, tagname: str) -> requests.Response:
   """Deletes a tag associated with a specific dataset."""
   hdr = {
      'User-Agent': 'Belt Pitch Sensor',
      'Authorization': authentication
   }
   return requests.delete(url= URL + DATASETS + "/" + datasetID + "/removetag/" + tagname, headers=hdr, verify=False)

def createChannels(authentication: str, datasetID: str, channeldata: str) -> str:
   """Creates multiple channels needing input data in the form: <index>TAB<name>TAB<unit>TAB<description>"""
   hdr = {
    'User-Agent': 'Belt Pitch Sensor',
    'Authorization': authentication
   }
   return requests.post(url= URL + DATASETS + "/" + datasetID + "/channels", headers=hdr, data=channeldata, verify=False)

def uploadData(authentication: str, datasetID: str, data: str) -> str:
   """Uploads data to a dataset.  Channels need to already have been created."""
   hdr = {
    'User-Agent': 'Belt Pitch Sensor',
    'Authorization': authentication
   }
   return requests.post(url= URL + DATASETS + "/" + datasetID + "/datapoints", headers=hdr, data=data, verify=False)

def getDataset(authentication: str, datasetnumber: str) -> str:
   """Returns the desired dataset's name and metadata."""
   hdr = {
    'User-Agent': 'Belt Pitch Sensor',
    'Authorization': authentication
   }
   return requests.get(url= URL + DATASETS + '/' + datasetnumber, headers=hdr, verify=False)

if __name__ == '__main__':
   print(createDataset(APIKEY, "API Test", "{}")) #getDataset(APIKEY, '2'))