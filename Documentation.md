# Introduction
In a few lines of code, your excel data can be retrieved and manipulated directly from your web app.

DISCLAIMER: This service is still under construction

# Overview
The Excel MicroAPI can perform the following
1. Parse valid json
2. Print duplicate content present in data
3. Add row to excel data
4. Search file

# Authentication
## Allowed HTTPs requests
PUT     : To create resource 
POST    : Update resource
GET     : Get a resource or list of resources
DELETE  : To delete resource

# Error Codes
* 200 ```OK``` - the request was successful (some API calls may return 201 instead).
* 201 ```Created``` - the request was successful and a resource was created.
* 204 ```No Content``` - the request was successful but there is no representation to return (i.e. the response is empty).
* 400 ```Bad Request``` - the request could not be understood or was missing required parameters.
* 401 ```Unauthorized``` - authentication failed or user doesn't have permissions for requested operation.
* 403 ```Forbidden``` - access denied.
* 404 ```Not Found``` - resource was not found.
* 405 ```Method Not Allowed``` - requested method is not supported for resource.


# Describing Endpoints
```diff
! **POST** 
``` ###### http://127.0.0.1:8000/api/v1/getall/