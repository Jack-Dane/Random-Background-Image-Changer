# Random-Background-Image-Changer

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
./start.sh [production/dev] <client_id> <client_secret>
```

The production mode will run the Flask API with gunicorn (4 workers) and run the
Vue application will be packaged. 

The dev mode (or any other value) will run both applications in dev mode.

When you run the server a window will open asking for you to accept access to your Imgur account. 
Click accept and copy the pin to your clipboard. Using the virtual environment you should run: 
```
addImgurPin --pin <ImgurPin> --clientId <clientId> --clientSecret <clientSecret>
```

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
When running in a development environment you can run the `fileHandler` directly if you don't want to run the front end application. You will
still need to create the virtual environment and run the terminal command: 
```
startFileHandler --clientId <client-id> --clientSecret <client-secret>
```

However, it is suggested to use with gunicorn. 
```
gunicorn -w 4 "randomBackgroundChanger.scripts:startProductionServer('--clientId', '<clientId>', '--clientSecret', '<clientSecret>')" 
```
This will enable concurrent requests to take place. If a request is getting new images by downloading
them from the server, and you make a new request, the new request won't be resolved until the first request
has finished. 

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
