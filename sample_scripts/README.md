
## Dependencies
```
pip install pycrypto requests
```

## Sample Scripts Usage 

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

### Create Job 
**Issue a new job request**  
`python createjobclient.py -toolvendor <toolvendor> -toolname <toolname> -toolversion <toolversion> -platform <platform> -filename <filename>`

#### Arguments
All arguments are mandatory unless stated otherwise
* toolvendor - Tool Vendor name
* toolname - Tool name 
* toolversion - Tool version
* platform - Platform
* filename - Name of file to upload. **Ensure that file is encrypted before upload**
