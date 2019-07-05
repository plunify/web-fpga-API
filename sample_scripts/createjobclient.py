import plunifyutils
import requests
import json
import base64
import argparse
import os
import sys

def parseCommandLineParameters(args, params):
  if args.toolvendor:
    params["toolvendor"] = args.toolvendor
  if args.toolname:
    params["toolname"] = args.toolname
  if args.toolversion:
    params["toolversion"] = args.toolversion
  if args.platform:
    params["platform"] = args.platform
  if args.filename:
    params["filename"] = args.filename
# end parseCommandLineParameters


def createFileLenParam(params):
  filename = os.path.abspath(params["filename"])

  if os.path.isdir(filename):
    print("Specified file for upload {} is a directory".format(filename))
    sys.exit()

  if not os.path.exists(filename):
    print("Specified file for upload {} does not exist".format(filename))
    sys.exit()

  params["filelen"] = str(os.path.getsize(filename))
# end createFileLenParam


def main():
  endpoint = "https://test1api.plunify.com/cloudapi/v1/createjob"

  parser = argparse.ArgumentParser()
  parser.add_argument("-v", help="Increase output verbosity", action="store_true")
  parser.add_argument("-c", "--credentials", metavar="credentials", help="Location of credential file. Default location is <home directory>/.plunify/credentials")
  parser.add_argument("-j", "--jobconfig", metavar="jobconfig", help="Location of job config file. Properties of this file will be overwritten by properties set on the command line.")
  parser.add_argument("-toolvendor", metavar="toolvendor", help="Tool Vendor")
  parser.add_argument("-toolname", metavar="toolname", help="Tool Name")
  parser.add_argument("-toolversion", metavar="toolversion", help="Tool Version")
  parser.add_argument("-platform", metavar="platform", help="Platform to run")
  parser.add_argument("-filename", metavar="filename", help="Zip file to upload")

  args = parser.parse_args()
  v = args.v

  plunify_apiid, plunify_key, plunify_password = plunifyutils.readCredentialsFile(args.credentials)

  params = {}
  params["apiid"] = plunify_apiid
  params["key"] = plunify_key 
  params["toolvendor"] = None
  params["toolname"] = None
  params["toolversion"] = None
  params["platform"] = None
  params["filename"] = None

  if args.jobconfig: plunifyutils.readConfigFile(args.jobconfig, params)

  parseCommandLineParameters(args, params)
  plunifyutils.validateParameters(params)
  createFileLenParam(params)

  url = plunifyutils.getSignedURL(endpoint, params, plunify_password)
  if v: print(url)

  print("Creating job ... ")
  response = requests.get(url);
  res = response.json()
  if v: print(json.dumps(res))

  if res["code"] == 0:
    base64presignURL = res["presigned"]
    presignUploadURL = base64.b64decode(base64presignURL);  
    print("Uploading {}".format(os.path.abspath(params["filename"])))
    with open(params["filename"], 'rb') as data:
      requests.put(presignUploadURL, data=data)
    print("Upload successful")
    print("Job Created. Job ID: {}".format(res["jobid"]))
  else:
    print("Error creating job: {}".format(res["message"]))
# end main


if __name__ == "__main__":
  main()

