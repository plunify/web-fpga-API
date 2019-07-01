import plunifyutils
import requests
import json
import base64
import argparse
import os
import sys


def parseCommandLineParameters(args, params):
  if args.servertype:
    params["servertype"] = args.servertype
  if args.jobid:
    params["jobid"] = args.jobid
# end parseCommandLineParameters


def main():
  endpoint = "https://test1api.plunify.com/cloudapi/v1/startjob"

  parser = argparse.ArgumentParser()
  parser.add_argument("-v", help="Increase output verbosity", action="store_true")
  parser.add_argument("-c", "--credentials", metavar="credentials", help="Location of credential file. Default location is <home directory>/.plunify/credentials")
  parser.add_argument("-j", "--jobconfig", metavar="jobconfig", help="Location of job config file. Properties of this file will be overwritten by properties set on the command line.")
  parser.add_argument("-servertype", metavar="servertype", help="Server Type")
  parser.add_argument("jobid", metavar="jobid", type=int, help="Starts the job with the specified Job ID.")

  args = parser.parse_args()
  v = args.v

  plunify_apiid, plunify_key, plunify_password = plunifyutils.readCredentialsFile(args.credentials)

  params = {}
  params["apiid"] = plunify_apiid
  params["key"] = plunify_key 
  params["servertype"] = None
  params["jobid"] = None

  if args.jobconfig: plunifyutils.readConfigFile(args.jobconfig, params)

  parseCommandLineParameters(args, params)
  plunifyutils.validateParameters(params)

  url = plunifyutils.getSignedURL(endpoint, params, plunify_password)
  if v: print(url)

  print("Starting job {} ...".format(params["jobid"]))
  response = requests.get(url);
  res = response.json()
  if res["code"] == 0:
    print("Job started");
  else:
    print("Error starting job: {}".format(res["message"]))
# end main


if __name__ == "__main__":
  main()
