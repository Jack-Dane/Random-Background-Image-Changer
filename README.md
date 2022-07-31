# Random-Background-Image-Changer

## How the Random-Background-Image-Changer works
This application works by running a backend Flask server that handles the background
images. There is a front-end application where you can view this image and change to the
next random background image in the queue. 

## Security
There is token based authentication for each request made to the FileHandler server. The 
token needs to be added to the "Authorization" header. 

## Imgur
The application uses the Imgur API to get random images. It will require you to create an account
and get the client_id and client_secret from your account. To do this you must register your app: 

https://api.imgur.com/#registerapp

## How to run
First run the install script, this will create the Python virtual environemnt and
create a symbolic link allowing the front-end application to access the background 
images. 
```
./install.sh
```
Then run the the start script to run the fileHandler service and the front-end view
```
./start.sh <client_id> <client_secret>
```

The front-end application should be running on port 3000, and the `fileHandler` API
should be running on port 5000. 

When you run the server a window will open asking for you to accept access to your Imgur account. 
Click accept and copy the pin to your clipboard. Using the virtual environment you should run: 
```
addImgurPin --pin <ImgurPin> --clientId <clientId> --clientSecret <clientSecret>
```

There is also another CLI command that allows you to change the background: 
```
updateBackgroundImage --clientId <clientId> --clientSecret <clientSecret>
```

## FileHandler
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

## Current Support
Currently, the only supported desktop environment is GNOME using gsettings.
