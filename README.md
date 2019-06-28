# Plunify Web FPGA API
This repository contains sample scripts that calls Plunify's Web FPGA API to to run Vivado and Plunify InTime in the cloud. 

## How to use this API
1. [Sign up](https://cloud.plunify.com/register) with Plunify Cloud to obtain API credentials.
2. Call Plunify Web FPGA API using your favourite language or tool!

## API reference
The description of each API is described below:


### Create Job

Creates a new job. A job ID and an URL is returned. Upload your project (zipped) using returned URL.  
End point: `http://cloudapi/v1/createjob`


### Start Job

Starts the job with the specified job ID. A cloud instance with be started and Vivado and Plunify InTime will be run on the project.  
End point: `http://cloudapi/v1/startjob`


### Get Job

Returns a list of urls to download results from the specific job ID.  
End point: `http://cloudapi/v1/getjob`


### List Job

Returns information on all previously ran jobs.  
End point: `http://cloudapi/v1/listjob`


## Signing Request URL
The hmac parameter contains the hashed of the request url to verify that the request is valid and have not been tampered with. Instructions on creating this hash can be found below.

1. From the request url, eg. `http://cloudapi/v1/createjob=apiid=123&key=key&toolvendor=tv&toolname=name&platform=lcd&filename=project.zip&filelen=1000&unixtime=999`
2. Signed the url using sha256 hash algorithm using your Plunify Cloud credential password to obtain the hash
3. Append the hmac parameter and hash to request url