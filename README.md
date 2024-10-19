# Lobby Backend

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the server:
   ```
   uvicorn src.main:app --reload
   ```

## Usage

### Create a New User

To create a new user, use the `/users/` endpoint with a POST request. Provide the following information in the request body:

- `username`: The desired username for the new user
- `phone_number`: The phone number of the new user

Example:

# API Documentation

## Users

### 1. Get User
- **Endpoint**: GET `/users/{user_id}`
- **Description**: Retrieve a user by their ID.
- **Parameters**:
  - `user_id` (path): The unique identifier of the user.
- **Response**: User object

### 2. Get User Friends
- **Endpoint**: GET `/users/{user_id}/friends`
- **Description**: Retrieve a list of friends for a specific user.
- **Parameters**:
  - `user_id` (path): The unique identifier of the user.
  - `skip` (query, optional): Number of records to skip. Default: 0
  - `limit` (query, optional): Maximum number of records to return. Default: 100
- **Response**: List of User objects

### 3. Get User by Phone Number
- **Endpoint**: GET `/users/phone/{phone_number}`
- **Description**: Retrieve a user, their friends, and events by phone number.
- **Parameters**:
  - `phone_number` (path): The phone number of the user.
- **Response**: UserWithFriendsAndEvents object

### 4. Add Friend
- **Endpoint**: POST `/users/{user_id}/friends`
- **Description**: Add a friend to a user's friend list.
- **Parameters**:
  - `user_id` (path): The unique identifier of the user.
  - `friend_id` (query): The unique identifier of the friend to add.
- **Response**: Friend object

### 5. Create User
- **Endpoint**: POST `/users/`
- **Description**: Create a new user.
- **Request Body**: UserCreate object
  - `username`: Username of the new user
  - `phone_number`: Phone number of the new user
- **Response**: User object

## Events

### 1. Get User Events
- **Endpoint**: GET `/events/{user_id}/events`
- **Description**: Retrieve all events for a specific user.
- **Parameters**:
  - `user_id` (path): The unique identifier of the user.
  - `skip` (query, optional): Number of records to skip. Default: 0
  - `limit` (query, optional): Maximum number of records to return. Default: 100
- **Response**: List of Event objects

### 2. Get Available Events
- **Endpoint**: GET `/events/{user_id}/available-events`
- **Description**: Retrieve available events for a specific user.
- **Parameters**:
  - `user_id` (path): The unique identifier of the user.
  - `skip` (query, optional): Number of records to skip. Default: 0
  - `limit` (query, optional): Maximum number of records to return. Default: 100
- **Response**: List of Event objects

### 3. Get Available Events by Phone
- **Endpoint**: GET `/events/phone/{phone_number}/available-events`
- **Description**: Retrieve available events for a user by their phone number.
- **Parameters**:
  - `phone_number` (path): The phone number of the user.
  - `skip` (query, optional): Number of records to skip. Default: 0
  - `limit` (query, optional): Maximum number of records to return. Default: 100
- **Response**: List of Event objects

### 4. Create Event for User
- **Endpoint**: POST `/events/{user_id}/createevent`
- **Description**: Create a new event for a specific user.
- **Parameters**:
  - `user_id` (path): The unique identifier of the user creating the event.
- **Request Body**: Event object
  - `name`: Name of the event
  - `description`: Description of the event
  - `date`: Date and time of the event
- **Response**: Event object

### 5. Join Event
- **Endpoint**: POST `/events/{user_id}/join/{event_id}`
- **Description**: Allow a user to join an existing event.
- **Parameters**:
  - `user_id` (path): The unique identifier of the user joining the event.
  - `event_id` (path): The unique identifier of the event to join.
- **Response**: Updated Event object

## Test Endpoint

### 1. Create Test Event
- **Endpoint**: POST `/test/create-event`
- **Description**: Create a test event with a randomly generated user. Used for testing purposes.
- **Response**: Event object

### 4. Upload User Image
- **Endpoint**: POST `/upload/{user_id}`
- **Description**: Upload an image file for a specific user.
- **Parameters**:
  - `user_id` (path): The unique identifier of the user.
  - `file` (form-data): The image file to be uploaded.
- **Response**: 
  - `message`: Confirmation message
  - `image_url`: Public URL of the uploaded image
- **Example**:
  ````
  POST /upload/123e4567-e89b-12d3-a456-426614174000
  Content-Type: multipart/form-data

  file: [binary data]
  ````
  Response:
  ```json
  {
    "message": "Image uploaded successfully",
    "image_url": "https://your-supabase-project.supabase.co/storage/v1/object/public/avatars/123e4567-e89b-12d3-a456-426614174000/image.jpg"
  }
  ````
- **Notes**: 
  - The image will be stored in the "avatars" bucket in Supabase storage.
  - The file path in storage will be `{user_id}/{unique_filename}`.
  - Make sure the user exists before attempting to upload an image.