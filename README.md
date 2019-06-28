# Plunify Web FPGA API
This repository contains sample scripts that call Plunify's Web FPGA API to run applications like Vivado, InTime or your preferred Plunify Partner applications in Plunify Cloud.

## How to use this API
1. Obtain your API ID from your Plunify Partner.
2. [Sign up](https://cloud.plunify.com/register) with Plunify Cloud to obtain API credentials.
3. Call Plunify Web FPGA API using your favourite language or tool!

## API reference
Refer to the API description below:


### Create Job

Creates a new execution task.
Returns a Job ID and an URL. Upload your project (in ZIP format) using the URL.  
End point: `http://cloudapi/v1/createjob`

### Start Job

Starts the execution task with the specified Job ID.
A cloud instance will be started to run your application.  
End point: `http://cloudapi/v1/startjob`

### Get Job

Returns a list of URLs to download results of the specified job ID.  
End point: `http://cloudapi/v1/getjob`

### List Job

Returns information on all completed tasks.  
End point: `http://cloudapi/v1/listjob`
