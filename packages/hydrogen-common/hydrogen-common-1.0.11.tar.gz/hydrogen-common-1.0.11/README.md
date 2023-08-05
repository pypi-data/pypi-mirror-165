# <img src="../../hydrogen_icon.jpeg" alt="HydroGEN Icon" style="height: 25px"> HydroGEN Common

The hydrogen_common PIP package provides services to simplify the code of various components used in the hydrogen application. The services support for configuring logging and use of the hydrogen message bus.

These shared functions not only simplfy the code, but they enforce common conventions on where logs are stored and conventions on how components communicate using the message bus. These conventions simplify the code and improve maintainability.

* hydrogen\_setup\_logger()
* get\_data\_directory()
* get\_domain\_directory()
* get\_domain\_path()
* get\_domain\_state()
* update\_domain\_state()
* start\_async\_job()

### Install
This component can be installed for python using the command:

	pip install hydrogen_common

### Build and Release
This component can be released to pypi using the commands from the root directory:

	python setup.py sdist bdist_wheel
	twine upload dist/*

You must enter your twine user/password. Remember to change the version in setup.cfg first.

## Functions

### HydroGEN Setup Logger
Call this method once in a process to configure the python logger.

	from hydrogen_common import hydrogen_setup_logger
	
	hydrogen_setup_logger()

This configures the python logging to write log messages to the folder:
    /home/HYDROAPP/%env%/logs
Where %env% is either main, prod, develop.

### Get data directory
Use this to get the root directory of user domains for the specific environment being used. For example,

	from hydrogen_common import get_data_directory
	dir = get_data_directory()

The directory will contain a list of subfolders for each user. Each user subfolder will contain subfolders for
user domains.

### Get domain directory
Use this to get the full path name to the hydrogen domain directory for the specified user_id and domain_directory name that identifies a domain. This returns the path name
using the hydrogen conventions for the specific environment being used. For example,
the path for the development environment is different than production environment.

    from hydrogen_common import get_domain_directory
	domain_path = get_domain_directory(user_id='myuser', domain_directory='domaindir1')

### Get domain state
Use this to get the JSON contents of the hydrogen state. This is the state associated with a domain
that contains the high level summary of the state of the domain. For example,

	from hydrogen_common import get_domain_state
	domain_state = get_domain_state(user_id="myuser", domain_directory="mydirectory")

or you can pass the json from a nats message containing user\_id and domain\_directory.

	nats_message = {"user_id": "myuser", "domain_directory": "mydirectory"}
	domain_state = get_domain_state(nats_message)

See table below for the attributes in the domain\_state.

If there is no domain state for the user and directory this this returns None.

### Update domain state
Use this to update the domain state of a user domain.

	from hydrogen_common import update_domain_state
	domain_state = {"user_id": "myuser", "domain_directory="mydir", notes="A note about domain"}
	updated_domain_state = update_domain_state(domain_state)

This updates the "notes" attribute of the domain state.

The domain\_state passed as an argument must contain at least the attributes "user\_id" and "domain\_directory".
Other attributes are replaced in the domain state if provided, other attributes in the existing domain state
are not changed. The return value is the complete domain state after the update.

See table below for the attributes in the domain\_state.

### Start\_async\_job
Use this to start an asynchnonous job to execute in the background and possibly on a different server.

	from hydrogen_common import start_async_job
	start_async_job("generate_scenario", user_id="myuser", domain_directory="mydir" parameters={"scenario_ids": "hot"})

The job will return immediately and run the job in background. The job will update the hydrogen domain state when it
finishes. It will set the state to "error" and set the domain_state "error\_message" if the job fails.

This job publishes a message to the NATS message bus if the environment has the NATS\_SERVER and NATS\_PORT environment variables configured. It the environment has the JOB\_SERVER and JOB\_SERVER\_PORT environment variables configured then this will submit the job to the SSH tunnel configured for the JOB\_SERVER and JOB\_SERVER_PORT to execute the job. If neither are configured then this will raise an exception.

# Domain State
This describes the attributes in the domain state returned by the get\_domain\_state() function.

|Domain State Attribute|Purpose|
|------|-------|
|user\_id|Id of the keycloak user who created the domain.|
|name|Name of the domain.|
|description|Description of the domain.|
|domain\_directory|Directory name of the domain that contains all the files of the domain.|
|state|State of the domain. E.g. new, ready, generating\_scenarios, generated\_scenaries, error.|
|grid\_bounds|Array of boundary points of the conus grid of the domain: lowx,lowy,highx,highy. |
|wgs84\_bounds|Array of boundary points of the lat/lon of the domain: lowlon,lowlat,highlon,highlat.|
|shape\_regions|Array of HUC shapes with attribute: huc\id, huc\_name, shape\_index, shapefile\_name, shape\_source.|
|created\_date|Date and time the domain was created.|
|conus1\_bounds|Array of boundary points in the conus1 grid.|
|conus2\_bounds|Array of boundary pointin the conus2 grid.|
|collected\_observations|True if the observations have been collected for this domain.|
|collected\_current\_conditions|True if the current conditions have been collected for this domain.|
|generated\_scenarios|List of scenario\_ids that have been generated for this domain|

# Environment Variables
There are several environment variables that are assumed to be set by the functions in the hydrogen_common package. These variables are set by the Kubernetes and Docker Compose environments that run code. If you execute code in a local development environment you must set these enviroment variables yourself. These variables are set in the scripts in the ~/.hydrogen folder by the install scripts.

|Environment Variable|Purpose|
|------|-------|
|CONTAINER\_HYDRO\_DATA\_PATH|Path name of a directory where files are stored when the code is run within a docker container. The setup logger will create a logs subdirectory here if this directory exists.|
|HOST\_HYDRO\_DATA\_PATH|Path name of a directory where files are stored when the code is run within a kubernetes virtual machine. This is used for logs if the directory specified by CONTAINER\_HYDRO\_DATA\_PATH does not exist.|
|CLIENT\_HYDRO\_DATA\_PATH|Path name of a directory where files are stored when the code is run within the client machine outside of the virtual machine. This is used for logs if neither directory above eixsts.|



# Run Unit Tests

To run the unit tests uninstall the hydrogen-common package and install the latest locally. From the root directory of the repository execute:

	pip uninstall hydrogen-common
	pip install -r requirements
	pytest tests
