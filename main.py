import requests
import xml.etree.ElementTree as ET
import logging
import base64
import json
import os
import pickle
import datetime
from lib import lib_bigquery
from conf import bluefolder_endpoints
import csv
import asyncio

#Path variable
path = os.path.dirname(os.path.realpath(__file__))

#Bluefolder API credentials and settings
bluefolderAuth = json.load(open(path + "/auth/bluefolder.json", 'r'))
toDate = datetime.datetime.now() + datetime.timedelta(days=5)
fromDate = datetime.datetime.now() - datetime.timedelta(days=30*6)
payload = bluefolder_endpoints.getEndpoints(fromDate, toDate)
#payload = bluefolder_endpoints.getEndpoints(datetime.datetime(2019, 1, 1), datetime.datetime(2021, 1, 1))

#Logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename=path + '/bluefolder.log',level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


class bluefolderAPI:
    def __init__(self, settingsJson = bluefolderAuth):
        self.settings = settingsJson
        self.startSession()
        self.response = None
        self.timestamp = datetime.datetime.now()

    def startSession(self):
        #Iniaitate Session
        self.session = requests.Session()
        authString = self.settings['token'] + ":" + self.settings['password']
        authString = base64.b64encode(authString.encode("utf-8"))
        self.session.auth = (self.settings['token'], self.settings['password'])
        self.session.headers.update({'Authorization': authString})

    def runAPI(self, payload):
        response = self.session.post(self.settings['url'] + payload['url'], data=payload['filters'])
        response = ET.fromstring(response.text)
        #pickle.dump(response, open('/tmp/' + payload['url'].replace("/", "").replace(".", "") + ".pkl", 'wb'))

        if len(response) > 0:
            try:
                if payload['innerList'] == True:
                    data = [{**{col.tag:[list_col.text for list_col in col.iter()] if len([list_col for list_col in col.iter()]) > 1 else col.text for col in row}, **{"upload_timestamp": str(self.timestamp)[:26]}} for row in response[0]]
                else:
                    data = [{**{col.tag:[list_col.text for list_col in col.iter()] if len([list_col for list_col in col.iter()]) > 1 else col.text for col in row}, **{"upload_timestamp": str(self.timestamp)[:26]}} for row in response]

                del response

                #Append timestamps and key
                data = [{**row, **{"upload_key": row[payload["id_column"]] + "-" + str(self.timestamp)[:26]}} for row in data]
            
                if len(data) > 0:
                    self.response = data
                else:
                    logger.info("API returned no data or parsing failed")
            except:
                if "response" in locals():
                    del response
                logger.info("API data error or API returned no results")


        else:
            del response
            logger.info("API returned no data")
            

    def saveToCsv(self, filename):
        if self.response != None:
            try:
                def deleteOldFile(filename: str):
                    """Removes old files from load folder"""
                    try:
                        os.remove(filename)
                        logger.info("File {} removed".format(filename))
                    except:
                        logger.info("File {} NOT found, NOT removed".format(filename))

                def parse(inputValue) -> str:
                    """ Remove special characters from strings within dictionary """
                    if type(inputValue) == str:
                        for char in [",", "'"]:
                            inputValue = inputValue.replace(char, "")
                        return inputValue
                    elif type(inputValue) == dict:
                        return json.dumps(inputValue)
                    elif type(inputValue) == list:
                        return json.dumps([x for x in inputValue if x != None])

                    else:
                        return inputValue

                deleteOldFile(filename)

                #json.dump(self.response, open(filename, 'w'))
                with open(filename, 'a') as fileObject:
                    for dic in self.response:
                        fileObject.write(json.dumps({k:parse(v) for k, v in dic.items()}) + "\n")
                #with open(filename, 'w') as writeFile:
                #    wr = csv.writer(writeFile)
                #    wr.writerows(self.response['data'])

            except Exception as e:
                logger.info("File save failed: {}".format(e))
        else:
            logger.info("Response has no data")



async def runReport(report):

    logging.info("Running report {}...".format(report))
    filename = "/tmp/{}.json".format(payload[report]['saveTo'])

    client = bluefolderAPI()
    client.runAPI(payload[report])
    await asyncio.sleep(1)
    client.saveToCsv(filename)
    
    if client.response != None:
        db = lib_bigquery.bigqueryWrapper()
        db.settings['table'] = payload[report]['table']
        #db.AddTable()
        db.deleteLoad(payload[report]['id_column'], [x[payload[report]['id_column']] for x in client.response] if payload[report]['id_column_is_string'] == False else ["'" + x[payload[report]['id_column']] + "'" for x in client.response])
        db.load_json_from_file(filename)
        await asyncio.sleep(1)
    else:
        logger.info("Skipping load for {}".format('serviceRequests'))
        
    logging.info("Running report {}... Done".format(report))

def postLog(payload: dict):
    db = lib_bigquery.bigqueryWrapper()
    db.settings['table'] = "Logs"
    #db.AddTable()
    db.loadRows([payload])

    
async def main():
    await asyncio.gather(*[runReport(report) for report in payload.keys()])
        

def accord_bluefolder(*args):
    try:
        asyncio.run(main())
        postLog({"ScriptName": "Bluefolder Daily", "SuccessfulRun": True, "Details": None, "Timestamp": datetime.datetime.now()})
    except:
        postLog({"ScriptName": "Bluefolder Daily", "SuccessfulRun": False, "Details": None, "Timestamp": datetime.datetime.now()})

if __name__ == "__main__":
    accord_bluefolder()