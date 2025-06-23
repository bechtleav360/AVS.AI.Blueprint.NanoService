# Python REST-API Template

## Introduction 
This is a template project for python services that aims to provide a REST-API.  
By default, it exposes an endpoint `/echo`, which accepts any valid json object and simply echos it back as the result.

## Controller
Controllers are used to create the endpoints of this service, mostly, but not necessarily, REST-Endpoints.  
Each Controller is a class and each Endpoint is an async method of that class. Controller classes should always have
"Controller" in their respective names, like "EchoController".  
This template contains three Controllers by default:

1. **Actuator:** The ActuatorController adds simple actuators to the API, including metrics using prometheus.
2. **Start:** The StartController adds a simple HTML start page on the default route `/`.
3. **Echo:** A simple Controller, echoing back the input.

All controllers should be added in separate python files located in "#projectROOT/src/api". The python files should end
with "_controller".

### BaseController
This template comes with a BaseController class, that forces the implementation of a "register_routes" method.  
All controllers that inherit from BaseController will automatically be added to the app.

## Services
A Service in this context is the connection between the controllers and the actual logic or content provided by this
API. They provide a "process_input" method, that takes the InputModel of the corresponding Controller and creates
an OutputModel, that is returned by the Controller. Controllers should never make changes after the Output has been
created. All manipulation or processing of the input has to take place within the service classes.  
Service classes always have "Service" in their respective names, like "EchoService".  
This template contains one example Service:

1. **Echo:** Directly parses the InputModel into the OutputModel, without any additional logic or processing.

## Processing/Content
Depending on this REST-API's purpose, any Logic that processes or collects content should happen in separate classes.  
If, for instance, this REST-API is supposed to provide data from a database (or any other datasource), a class should be
created, that handles the data retrieval/creation/...  
Those classes should then be used by Service classes to create the connections to the REST-API.

## Models
This API uses pydantic models to represent simple data classes. All pydantic model classes should be added in the
"#projectROOT/src/common/model" folder.

### DataTransferObjects (DTOs)
DataTransferObjects are used to parse in- and output to and from the REST-API. A Controller specifies which input to
accept and what the output should look like. Using FastAPI, the input is automatically parsed and validated.  
DTOs should be added to "#projectROOT/src/common/model/dto". A separate python file should be used for each controller,
that uses a DTO.

## Configuration
The template also provides a default configuration class called "ConfigurationManager". The basis for this class is 
the dynaconf framework, which allows access of configuration variables via both a config.py file (located in the 
folder #projectROOT/config) and environment variables.

### Usage
To use the ConfigurationManager, simply import the class and instantiate it, e.g.:
```python 
from src.config.config import ConfigurationManager

SETTINGS = ConfigurationManager()
```
To reference any configuration variable use the "get_config" method.

## Logs
The Service implements basic logging, including logging to a .log file. The last 300 lines can be returned via the
actuator endpoint `/logs`