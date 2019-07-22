import plunifyutils
import requests
import json
import argparse


def parseCommandLineParameters(args, params):
  if args.type:
    params["type"] = args.type
# end parseCommandLineParameters


def main():
  host = "https://prod8api.plunify.com"
  uri = "cloudapi/v1/listjob"

  description = ""
  description += "Return job details.\n"

  parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=description)
  parser.add_argument("-v", help="Increase output verbosity", action="store_true")
  parser.add_argument("-c", "--credentials", metavar="credentials", help="Location of credential file. Default location is <home directory>/.plunify/credentials")
  parser.add_argument("type", metavar="type", choices=["all", "current"], help="If 'all', all jobs are returned. If 'current', the latest job will be returned")

  args = parser.parse_args()
  v = args.v

  plunify_apiid, plunify_key, plunify_password, plunify_host = plunifyutils.readCredentialsFile(args.credentials)
  if plunify_host:
    host = plunify_host
  endpoint = host + "/" + uri

  params = {}
  params["apiid"] = plunify_apiid
  params["key"] = plunify_key 
  params["type"] = None

  parseCommandLineParameters(args, params)
  plunifyutils.validateParameters(params)

  url = plunifyutils.getSignedURL(endpoint, params, plunify_password)
  if v: print(url)

  print("Listing jobs ... ")
  response = requests.get(url);
  if v: print(json.dumps(res))
  res = response.json()

  if res["code"] == 0:
    print(json.dumps(res["jobs"], indent=4))
    print("Total jobs: {}".format(res["totaljobs"]))
  else:
    print("Error listing jobs: {}".format(res["message"]))
# end main


if __name__ == "__main__":
  main()
