# Random-Background-Image-Changer
Change your background to random Images from Imgur. 

## How the Random-Background-Image-Changer works
A back end Flask API handles the changing of the background, there are various endpoints which are 
detailed below. There is a front-end Vue webpage that will enable changing of the background image 
and viewing of the current background. 

The application uses Imgur API to get the random images. 

## Current Support
Currently, the only supported desktop environment is GNOME using gsettings.

## How to run
First run the install script, this will create the Python virtual environment and
install the relevant npm packages. 
```
./install.sh
```
Then run the start script, see the Imgur section in regard to getting the client 
id and secret. 
```
./start.sh <client_id> <client_secret>
```

You should now be able to view the web application on http://localhost:5050. 

When you run the server a window will open asking for you to accept access to your Imgur account. 
Click accept and copy the pin to your clipboard. Using the virtual environment you should run: 
```
addImgurPin --pin <ImgurPin> --clientId <clientId> --clientSecret <clientSecret>
```

You can also now add this pin through the front-end adding by clicking on the 
"Add Imgur Pin" button. 

## CLI client

There is also another CLI command that allows you to change the background: 
```
updateBackgroundImage --clientId <clientId> --clientSecret <clientSecret>
```
This would enable you to run the backend without needing to run the front-end vue
application if needed. 

## Imgur
The application uses the Imgur API to get random images. It will require you to create an account
and get the client_id and client_secret from your account. To do this you must register your app: 

https://api.imgur.com/#registerapp

## Backend - FileHandler
You can run the back-end API independently of the front-end with the command:
```
startFileHandler --clientId <client-id> --clientSecret <client-secret>
```
The backend API runs in a gunicorn worker. 

### Endpoints
#### Change the desktop background image.

**URL**
```
http://localhost:5000/change-background
```

**Method**
POST GET

#### Get the current background image

**URL**
```
http://localhost:5000/current-image
```

**Method**
GET

**Response Type**
image/gif


#### Get the current background image hash

**URL**
```
http://localhost:5000/current-image-hash
```

**Method**
GET

**Response Type**
JSON

### Token Endpoints
#### Generating a new token.

**URL**
```
http://loalhost:5000/token
```
**Method** 
POST

**Response Type** 
JSON

**JSON Parameters**
```
{
    "clientId": <client-id>,
    "clientSecret": <client-secret>
}
```
These parameters are the same as the ones passed to the command line argument. 

#### Revoking a token

**URL**
```
http://localhost:5000/token
```

**method** 
DELETE

**JSON Parameters**
```
{
    "clientId": <client-id>,
    "clientSecret": <client-secret>,
    "token": <token-to-revoke>
}
```

#### Adding the Imgur Auth Pin

**URL**
```
http://localhost:5000/imgur-pin
```

**method**
POST

**JSON Parameters**
```
{
    "clientId": <client-id>,
    "clientSecret": <client-secret>,
    "pin": <imgur-pin>
}
```
