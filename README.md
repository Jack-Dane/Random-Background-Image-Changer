# Random-Background-Image-Changer

## How the Random-Background-Image-Changer works
This application works by running a backend Flask server that handles the background
images. There is a front-end application where you can view this image and change to the
next random background image in the queue. 

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

## FileHandler
You can run the `fileHandler` directly if you don't want to run the front end application. You will
still need to create the virtual environment and run the terminal command: 
```
startFileHandler --clientId <client-id> --clientSecret <client-secret>
```

### Endpoints
Change the desktop background image.

**URL**
```
http://localhost:5000/change-background
```

**Method**
POST GET

Get the current background image

**URL**
```
http://localhost:5000/current-image
```

**Method**
GET

**Response Type**
JSON

## Current Support
Currently, the only supported desktop environment is GNOME using gsettings.
