import plunifyutils
import requests
import json
import base64
import argparse
import os
import sys
import hashlib
import struct
from Crypto.Cipher import AES


def decryptFile(key, in_filename, out_filename=None):

    if not out_filename:
        out_filename = in_filename + '.dec'

    chunk_size = 1024 * 1024
    signature = b"[Encrypted by Plunify Pte Ltd. v1]"
    
    in_file = open(in_filename, 'rb')
    signature_found = in_file.read( len(signature) )
    in_file.close()

    if signature_found != signature:
        print("{} has not been encrypted".format(os.path.abspath(in_filename)))
        copyfile(in_filename, out_filename)
        return

    in_file = open(in_filename, 'rb')
    out_file = open(out_filename, 'wb')

    signature_found = in_file.read( len(signature) )
    origsize = struct.unpack('<Q', in_file.read(struct.calcsize('Q')))[0]
    iv = in_file.read( AES.block_size )
    cipher = AES.new( key, AES.MODE_CBC, iv )

    while True:
        chunk = in_file.read(chunk_size)
        if len(chunk) == 0:
            break
        dec_chunk = cipher.decrypt(chunk)
        out_file.write(dec_chunk)
        
    out_file.truncate(origsize)
    in_file.close()
    out_file.close()
# end decryptFile


def parseCommandLineParameters(args, params):
  if args.jobid:
    params["jobid"] = args.jobid
  if args.outdir:
    params["outdir"] = args.outdir
# end parseCommandLineParameters


def main():
  host = "https://prod8api.plunify.com"
  uri = "cloudapi/v1/getjob"

  description = ""
  description += "Download result files for the specified job.\n"
  description += "Files will be downloaded into the output directory specified.\n"
  description += "Note - Files are decrypted autmatically.\n"
  description += "If you prefer to download and decrypt files manually, see getjobclient.py and decrypt.py.\n"

  parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=description)
  parser.add_argument("-v", help="Increase output verbosity", action="store_true")
  parser.add_argument("-c", "--credentials", metavar="credentials", help="Location of credential file. Default location is <home directory>/.plunify/credentials")
  parser.add_argument("jobid", metavar="jobid", type=int, help="Downloads and decrypts job information with the specified Job ID.")
  parser.add_argument("-o", "--outdir", metavar="outdir", help="Ouput directory for downloaded files")

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
  params["outdir"] = None

  parseCommandLineParameters(args, params)
  plunifyutils.validateParameters(params)

  outdir = os.path.abspath(params["outdir"])
  params["outdir"] = None

  url = plunifyutils.getSignedURL(endpoint, params, plunify_password)
  if v: print(url)

  print("Get job {} info ... ".format(params["jobid"]))
  response = requests.get(url);
  res = response.json()
  if v: print(json.dumps(res))

  if res["code"] == 0:
    print("Job status: {}".format(res["action"]))

    if sys.version_info[0] < 3:
        key = hashlib.md5(bytes(plunify_password)).hexdigest()
    else:
        key = hashlib.md5(bytes(plunify_password, "latin-1")).hexdigest()

    files = res["files"]
    urls = res["presigned"]

    if len(files):

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

        filename_no_ext, file_ext = os.path.splitext(downloadfile)
        if file_ext == ".enc":
          print("Decrypting {} to {} ".format(downloadfile, filename_no_ext))
          decryptFile(key, downloadfile, filename_no_ext)
    
      print("Download complete")

    else:
      print("No files to download")

  else:
    print("Error getting job info: {}".format(res["message"]))
# end main


if __name__ == "__main__":
  main()
