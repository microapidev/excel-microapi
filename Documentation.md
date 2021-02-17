# Introduction
In a few lines of code, your excel data can be retrieved and manipulated directly from your web app.

DISCLAIMER: This service is still under construction

# Overview
The Excel MicroAPI can perform the following (at the time of this publication)
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


# Endpoints
After the following the steps in the README.md file, to clone the Excel MicroAPI on your local machine and run your server: 
Test with postman or simply input the endpoints in the address started by the development server

```diff
+ GET  http://127.0.0.1:8000/api/v1/getall/
```
Returns all the files stored, the titles with which they were stored and the location they were stored at.

```diff
! POST http://127.0.0.1:8000/api/v1/add
```
When testing,
json data: 
{"title":The title(a name the user can remember) that the user wishes to use to store the file "content":File Upload}

```diff
! POST http://127.0.0.1:8000/api/v1/parse
```
When testing,
Key: content, 
Value: Excel file upload Returns: Json with Parsed values and process_time to Parse Excel file

```diff
! POST http://127.0.0.1:8000/api/v1/add_row/
```
During test, 
KEY 1: "content ", 
VALUE1: excel file upload 
KEY 2: "data", VALUE2: {"sheet":, "updated":<list of new row, in square brackets and seperated by comma> SAMPLE_REQUEST: {"sheet":"sheet1", "updated":["May-01",73,455]

```diff
! POST http://127.0.0.1:8000/api/v1/search
```
Inputing a column in which to search and keyword to search for, the response returned is "status: True or False"

```diff
! POST http://127.0.0.1:8000/api/v1/printduplicates/
```
Duplicate content found in excel file is returned. When testing, KEY: "content" VALUE: duplicate content present in uploaded file