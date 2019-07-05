import plunifyutils
import requests
import json
import base64
import argparse
import os


def parseCommandLineParameters(args, params):
  if args.jobid:
    params["jobid"] = args.jobid
  if args.outdir:
    params["outdir"] = args.outdir
# end parseCommandLineParameters


def main():
  endpoint = "https://test1api.plunify.com/cloudapi/v1/getjob"

  parser = argparse.ArgumentParser()
  parser.add_argument("-v", help="Increase output verbosity", action="store_true")
  parser.add_argument("-c", "--credentials", metavar="credentials", help="Location of credential file. Default location is <home directory>/.plunify/credentials")
  parser.add_argument("jobid", metavar="jobid", type=int, help="Starts the job with the specified Job ID.")
  parser.add_argument("-o", "--outdir", metavar="outdir", help="Ouput directory for downloaded files")

  args = parser.parse_args()
  v = args.v

  plunify_apiid, plunify_key, plunify_password = plunifyutils.readCredentialsFile(args.credentials)

  params = {}
  params["apiid"] = plunify_apiid
  params["key"] = plunify_key 
  params["jobid"] = None
  params["outdir"] = None

  parseCommandLineParameters(args, params)
  plunifyutils.validateParameters(params)

  url = plunifyutils.getSignedURL(endpoint, params, plunify_password)
  if v: print(url)

  print("Get job {} info ... ".format(params["jobid"]))
  response = requests.get(url);
  res = response.json()
  if v: print(json.dumps(res))

  if res["code"] == 0:
    print("Job status: {}".format(res["action"]))

    files = res["files"]
    urls = res["presigned"]

    if len(files):

      outdir = os.path.abspath(params["outdir"])
      if not os.path.exists(outdir) or not os.path.isdir(outdir):
        print("Creating output directory {}".format(outdir))
        os.makedirs(outdir);

      for i in range(len(files)):
        presignurl = base64.b64decode(urls[i])
        downloadfile = os.path.join(outdir, files[i]);
        print("Downloading {}. ({} of {})".format(downloadfile, i+1, len(files)))

        downloadresponse = requests.get(presignurl)
        with open(downloadfile, "wb") as f:
          f.write(downloadresponse.content)
    
      print("Download complete")

    else:
      print("No files to download")

  else:
    print("Error getting job info: {}".format(res["message"]))
# end main


if __name__ == "__main__":
  main()
