# Open Source Contribution Finder API Contract
## Base URL and Versioning Strategy
The base URL for the API is `https://api.oscf.com/v1`. The API uses a versioning strategy to ensure backwards compatibility.

## Authentication Scheme
The API uses a JWT Bearer token authentication scheme. All requests must include a valid JWT token in the `Authorization` header.

## Global Error Format
All error responses will follow the following format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "ERROR_MESSAGE"
  }
}
```
## Rate Limiting Policy
The API has a rate limiting policy to prevent abuse. The policy is as follows:
* 100 requests per minute for authenticated users
* 10 requests per minute for unauthenticated users

## Endpoints

### 1. Register Contributor
#### HTTP Method + Path
`POST /api/v1/contributors`
#### Description
Registers a new contributor.
#### Authentication
Required, JWT Bearer token
#### Request Body
```json
{
  "name": "string",
  "email": "string",
  "skills": ["string"]
}
```
#### Success Response
* HTTP Status Code: 201
* JSON Response Schema:
```json
{
  "id": "integer",
  "name": "string",
  "email": "string",
  "skills": ["string"]
}
```
#### Error Responses
* 400: Invalid request body
* 401: Unauthorized
* 409: Contributor already exists
#### Example Request/Response Pair
```bash
curl -X POST \
  https://api.oscf.com/v1/contributors \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"name": "John Doe", "email": "john.doe@example.com", "skills": ["Python", "JavaScript"]}'
```
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "skills": ["Python", "JavaScript"]
}
```

### 2. Get Contributor Profile
#### HTTP Method + Path
`GET /api/v1/contributors/{id}`
#### Description
Retrieves a contributor's profile.
#### Authentication
Required, JWT Bearer token
#### Request Body
None
#### Success Response
* HTTP Status Code: 200
* JSON Response Schema:
```json
{
  "id": "integer",
  "name": "string",
  "email": "string",
  "skills": ["string"]
}
```
#### Error Responses
* 401: Unauthorized
* 404: Contributor not found
#### Example Request/Response Pair
```bash
curl -X GET \
  https://api.oscf.com/v1/contributors/1 \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN'
```
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "skills": ["Python", "JavaScript"]
}
```

### 3. Create Project
#### HTTP Method + Path
`POST /api/v1/projects`
#### Description
Creates a new project.
#### Authentication
Required, JWT Bearer token
#### Request Body
```json
{
  "name": "string",
  "description": "string",
  "requiredSkills": ["string"]
}
```
#### Success Response
* HTTP Status Code: 201
* JSON Response Schema:
```json
{
  "id": "integer",
  "name": "string",
  "description": "string",
  "requiredSkills": ["string"]
}
```
#### Error Responses
* 400: Invalid request body
* 401: Unauthorized
* 409: Project already exists
#### Example Request/Response Pair
```bash
curl -X POST \
  https://api.oscf.com/v1/projects \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"name": "Example Project", "description": "This is an example project", "requiredSkills": ["Python", "JavaScript"]}'
```
```json
{
  "id": 1,
  "name": "Example Project",
  "description": "This is an example project",
  "requiredSkills": ["Python", "JavaScript"]
}
```

### 4. Get Project
#### HTTP Method + Path
`GET /api/v1/projects/{id}`
#### Description
Retrieves a project.
#### Authentication
Required, JWT Bearer token
#### Request Body
None
#### Success Response
* HTTP Status Code: 200
* JSON Response Schema:
```json
{
  "id": "integer",
  "name": "string",
  "description": "string",
  "requiredSkills": ["string"]
}
```
#### Error Responses
* 401: Unauthorized
* 404: Project not found
#### Example Request/Response Pair
```bash
curl -X GET \
  https://api.oscf.com/v1/projects/1 \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN'
```
```json
{
  "id": 1,
  "name": "Example Project",
  "description": "This is an example project",
  "requiredSkills": ["Python", "JavaScript"]
}
```

### 5. Search Projects
#### HTTP Method + Path
`GET /api/v1/projects`
#### Description
Searches for projects based on skills and interests.
#### Authentication
Required, JWT Bearer token
#### Request Body
None
#### Query Parameters
* `skills`: comma-separated list of skills
* `interests`: comma-separated list of interests
#### Success Response
* HTTP Status Code: 200
* JSON Response Schema:
```json
[
  {
    "id": "integer",
    "name": "string",
    "description": "string",
    "requiredSkills": ["string"]
  }
]
```
#### Error Responses
* 401: Unauthorized
#### Example Request/Response Pair
```bash
curl -X GET \
  https://api.oscf.com/v1/projects?skills=Python,JavaScript&interests=web-development \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN'
```
```json
[
  {
    "id": 1,
    "name": "Example Project",
    "description": "This is an example project",
    "requiredSkills": ["Python", "JavaScript"]
  }
]
```

### 6. Assign Issue
#### HTTP Method + Path
`POST /api/v1/projects/{projectId}/issues/{issueId}/assign`
#### Description
Assigns an issue to a contributor.
#### Authentication
Required, JWT Bearer token
#### Request Body
```json
{
  "contributorId": "integer"
}
```
#### Success Response
* HTTP Status Code: 200
* JSON Response Schema:
```json
{
  "id": "integer",
  "projectId": "integer",
  "issueId": "integer",
  "contributorId": "integer"
}
```
#### Error Responses
* 400: Invalid request body
* 401: Unauthorized
* 404: Project or issue not found
#### Example Request/Response Pair
```bash
curl -X POST \
  https://api.oscf.com/v1/projects/1/issues/1/assign \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"contributorId": 1}'
```
```json
{
  "id": 1,
  "projectId": 1,
  "issueId": 1,
  "contributorId": 1
}
```

### 7. Get Contribution Analytics
#### HTTP Method + Path
`GET /api/v1/contributors/{id}/analytics`
#### Description
Retrieves a contributor's analytics.
#### Authentication
Required, JWT Bearer token
#### Request Body
None
#### Success Response
* HTTP Status Code: 200
* JSON Response Schema:
```json
{
  "contributions": "integer",
  "projects": "integer",
  "issues": "integer"
}
```
#### Error Responses
* 401: Unauthorized
* 404: Contributor not found
#### Example Request/Response Pair
```bash
curl -X GET \
  https://api.oscf.com/v1/contributors/1/analytics \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN'
```
```json
{
  "contributions": 10,
  "projects": 5,
  "issues": 20
}
```