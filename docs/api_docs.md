# Momo transactions API endpoint documentation
## API Outline
- Name: REST API
- Base URL: http://localhost:8000
- Purpose: This API makes SMS records available in a secure and efficient way, allowing users to retrieve, create, update, and delete SMS.
- Version: V1.0
- Authentication: Basic authantication
## Endpoint & Method

## 1. Get all transactions
   - URL: /transactions
   - Method: GET
   - Description: Retrieves a list of all momo transactions in the system.

### Request Example  
curl command: 

curl -u admin:secret "http://localhost:8000/transactions"

where:
- admin: username
- secret:password 
### Response Example

### Error Codes
- 200 OK: successfully retrieved data
- 401 Unauthorised: for invalid credentials
- 500 Internal server error

## 2. Retrieve Single Transaction
### Endpoint & Method
- URL:
```
/transactions/{id}
```
- Method: GET
- ID: Transaction_id
- Authentication: Basic authentication
- Description: Retrieves a specific transaction using its id

### Response Example

### Error Codes
- 404 Not Found: Transaction with specific id not found/ doesn't exist
- 200 OK: successfully retrieved data
- 401 Unauthorised: for invalid credentials
- 500 Internal server error

## 3. POST ( Create new transaction)
### Endpoint & Method
- URL: /transactions
- Method: POST
- Authentication: Basic authentication
- Description: Creates a new transaction record.

## Example
### Error codes
- 201 Created: Transaction successfully created
- 400 Bad Request: Invalid JSON format or missing required fields
- 401 Unauthorized: Invalid or missing authentication credentials
- 500 Internal Server Error: Server error occurred

## 4. PUT (Update existing transaction)
### Endpoint & Method
- URL: /transactions/{id}
- Method: PUT
- Authentication: Basic authentication
- ID: Transaction_id (for record to be updated)
- Description: Update an already existing transaction with new or added data.

- ### Error codes
- 200 OK: Transaction successfully updated
- 400 Bad Request: Invalid JSON format or missing required fields
- 404 Not Found: Transaction with ID doesn't exist
- 500 Internal Server Error: Server error occurred

## 5. DELETE (Delete transaction)
### Endpoint & Method
- URL: /transactions/{id}
- Method: DELETE
- Authentication: Basic authentication
- ID: Transaction_id (for record to be deleted)
- Description: Deleting a transaction record for good.

### Error Codes
- 200 OK: Transaction successfully deleted
- 401 Unauthorized: Invalid or missing authentication credentials
- 404 Not Found: Transaction with specified ID does not exist
- 500 Internal Server Error: Server error occurred

## Rate Limiting & Performance
- Concurrent Requests: Supported with thread-safe file operations
- Response Time: Typically under 100ms for single operations
- File Storage: JSON file-based persistence (data/transactions.json)
- Memory Usage: Loads full dataset into memory for fast access

## Common Error Responses

### 400 Bad Request
```
{
  "error": "Invalid JSON"
}
```
### 401 Unauthorized
```
HTTP/1.0 401 Unauthorized
WWW-Authenticate: Basic realm="MoMoAPI"
```
### 404 Not Found
```
{
  "error": "Not found"
}
```
### 500 Internal Server Error
```
{
  "error": "Internal server error"
}
```


