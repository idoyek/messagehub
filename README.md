# Message Hub

## Overview
Message Hub is a Django-based project designed to provide messaging functionality. It allows users to send and receive messages via a RESTful API.

## Usage
- The server host is deployed by Render, the URL is https://web-service-5agj.onrender.com.
- The database is PostgreSQL, also deployed by Render.

## Admin
Access the Django admin panel at `https://web-service-5agj.onrender.com/admin/`.
Use the following credentials:
- Username: ido
- Password: ido

## Postman
The Postman collection is in the root directory.
Please import it into Postman, start making requests and interact with the Message Hub API.
First, you will need to login (use the current JSON body and login as karina).  
Please save somewhere the csrftoken that is created after the login. It is in the Response's Headers, under the Set-Cookie key.  
Make sure that you have those headers in the requests you send:  
Key: Referer, Value: https://web-service-5agj.onrender.com.  
Key: X-CSRFToken, Value: user's csrftoken created after the login.  
Then you will be able to see messages karina received, write a message, read messages, and delete a message.  
Have fun!
