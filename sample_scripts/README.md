
## Dependencies
```
pip install pycrypto requests
```

## Plunify API Credentials
You need to specify the Plunify API ID and Plunify Key for each API request. These can be downloaded as an `INI` file on [cloud.plunify.com](https://cloud.plunify.com). 

Specify the location of this `INI` file using the `-c` flag. If this argument is not set, the script will look for an `INI` file at $USER_HOME/.plunify/credentials.  
Use `--help` for more information.

## Using a config file to store API request parameters
Parameters for API requests can be stored in an `INI` file for convenience. Store parameters under the `project` section header. Parameters are case sensitive and should match the script arguments exactly. Specify the location of this file as a command line argument using the `-j` flag.

Eg. Instead of passing arguments on the command line,
```
python createjobclient.py -toolname vivado ... 
```
Use a `INI` file.  
```
# config.ini
[project]
toolname=vivado 
```
Pass the `INI` file as the argument instead.
```python
createjobclient.py -j config.ini
```

## Create Job 
**Issue a new job request**  
`python createjobclient.py -toolvendor <toolvendor> -toolname <toolname> -toolversion <toolversion> -platform <platform> -filename <filename>`  
Returns a job id which can be used to start, download or check the status of the job.

### Arguments
All arguments are mandatory unless stated otherwise.
* toolvendor - Tool Vendor name.
* toolname - Tool name.
* toolversion - Tool version.
* platform - Platform.
* filename - Name of file to upload. **Ensure that file is encrypted before upload**

## Start Job 
**Issue a request to start compiling**  
`python startjobclient.py -servertype <server type> -maxtime <maxtime> <jobid>`

### Arguments
All arguments are mandatory unless stated otherwise.
* servertype - The server machine type to use for compiling. Check [here](https://cloud.plunify.com/faq#what_are_the_available_server_machine_types_for_each_cloud_region) for a list of available server machines.
* maxtime (**Optional**) - The maximum allowed time for compilation in hours. The default is 48 hours.
* jobid - Job id.

## Cancel Job 
**Cancels the job specified**  
`python canceljobclient.py <jobid>`

### Arguments
All arguments are mandatory unless stated otherwise.
* jobid - Job id.

## Get Job 
**Download result files for this job**  
`python getjobclient.py -o <output directory> <jobid>`
Files (if any) will be downloaded into the output directory specified.

### Arguments
All arguments are mandatory unless stated otherwise.
* output directory - The output directory for downloaded files. Directory will be created if it does not exist.
* jobid - Job id.

## List Job 
**Returns job details**  
`python listjobclient.py <type>`

### Arguments
All arguments are mandatory unless stated otherwise.
* type - One of the below options.
  * all - All previously ran jobs are returned.
  * current - The latest job is returned.

