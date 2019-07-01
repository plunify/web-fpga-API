import sys
import os
import hmac
import hashlib
import time

if sys.version_info[0] < 3:
  import ConfigParser as configparser
else:
  import configparser as configparser


def readCredentialsFile(file_path):
  if not file_path:
    file_path = os.path.join(os.path.expanduser("~"), ".plunify", "credentials")

  file_path = os.path.abspath(file_path)

  if os.path.isdir(file_path):
    print("Credentials file {} is a directory".format(file_path))
    sys.exit()

  if not os.path.exists(file_path):
    print("Credentials file {} does not exist".format(file_path))
    sys.exit()

  print("Reading credentials file: {}".format(file_path))

  section_id = "default"
  option_plunify_apiid_id = "plunify_apiid"
  option_plunify_key_id = "plunify_key"
  option_plunify_password_id = "plunify_password"
  
  parser = configparser.ConfigParser()
  parser.read(file_path)
  
  if not parser.has_option(section_id, option_plunify_apiid_id):
    print("Credentials file error - Unable to get {} property".format(option_plunify_apiid_id))
    sys.exit()
  else:
    plunify_apiid = parser.get(section_id, option_plunify_apiid_id)

  if not parser.has_option(section_id, option_plunify_key_id):
    print("Credentials file error - Unable to get {} property".format(option_plunify_key_id))
    sys.exit()
  else:
    plunify_key = parser.get(section_id, option_plunify_key_id)

  if not parser.has_option(section_id, option_plunify_password_id):
    print("Credentials file error - Unable to get {} property".format(option_plunify_password_id))
    sys.exit()
  else:
    plunify_password = parser.get(section_id, option_plunify_password_id)

  return plunify_apiid, plunify_key, plunify_password
# end readCredentialsFile


def readConfigFile(file_path, params):
  file_path = os.path.abspath(file_path)
  if os.path.isdir(file_path):
    print("Config file {} is a directory".format(file_path))
    sys.exit()

  if not os.path.exists(file_path):
    print("Config file {} does not exist".format(file_path))
    sys.exit()

  print("Reading config file: {}".format(file_path))

  section_id = "project"

  parser = configparser.ConfigParser()
  parser.read(file_path)

  for prop in params:
    if parser.has_option(section_id, prop):
      params[prop] = parser.get(section_id, prop)
# end readConfigFile


def getSignedURL(endpoint, params, plunify_password):
  params["unixtime"] = int(time.time()) 
  url = endpoint + "?" + "&".join([k + "=" + str(params[k]) for k in params])

  if(sys.version_info[0] < 3):
    sign = hmac.new(plunify_password, url, hashlib.sha256)
  else:
    sign = hmac.new(bytes(plunify_password, 'latin-1'), bytes(url, 'latin-1'), hashlib.sha256)
  signature = sign.hexdigest()
  url = url + "&hmac=" + signature
  return url
# end getSignedURL


def validateParameters(params):
  for prop in params:
    if not params[prop]:
      print("Required parameter {} not specified in config file or command line".format(prop))
      sys.exit()
# end validateParameters
