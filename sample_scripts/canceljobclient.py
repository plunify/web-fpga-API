import plunifyutils
import requests
import json
import argparse

def parseCommandLineParameters(args, params):
  if args.jobid:
    params["jobid"] = args.jobid

def main():
  host = "https://prod8api.plunify.com"
  uri = "cloudapi/v1/canceljob"

  description = ""
  description += "Cancels the job specified.\n"

  parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=description)
  parser.add_argument("-v", help="Increase output verbosity", action="store_true")
  parser.add_argument("-c", "--credentials", metavar="credentials", help="Location of credential file. Default location is <home directory>/.plunify/credentials")
  parser.add_argument("jobid", metavar="jobid", type=int, help="Cancels the job with the specified Job ID.")

  args = parser.parse_args()
  v = args.v

  plunify_apiid, plunify_key, plunify_password, plunify_host = plunifyutils.readCredentialsFile(args.credentials)
  if plunify_host:
    host = plunify_host
  endpoint = host + "/" + uri

  params = {}
  params["apiid"] = plunify_apiid
  params["key"] = plunify_key 
  params["jobid"] = None

  parseCommandLineParameters(args, params)
  plunifyutils.validateParameters(params)

  url = plunifyutils.getSignedURL(endpoint, params, plunify_password)
  if v: print(url)

  print("Cancelling job {}".format(params["jobid"]))
  response = requests.get(url);
  res = response.json()
  if v: print(json.dumps(res))

  if res["code"] == 0:
    print("Job cancelled sucessfully")
  else:
    print("Error cancelling job: {}".format(res["message"]))
# end main


if __name__ == "__main__":
  main()
