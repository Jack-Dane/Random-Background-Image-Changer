<script>

import { io } from 'socket.io-client';

export default {

    data: () => ({
        currentImageHash: null,
        currentImage: null
    }),

    props: {
        requests: Object
    },

    methods: {

        async getNewCurrentImage () {
            let self = this;
            if (!this.checkAuthentication()) {
                return;
            }

            this.currentImage = await fetch(
                "http://localhost:5000/current-image",
                {
                    headers: {
                        "Content-Type": "image/gif",
                        "Authorization": "Bearer " + self.requests.authorisationToken
                    },
                }
            ).then(function(response) {
                if (response.status == 200) {
                    return response.blob();
                }
                throw new Error(response.status);
            }).then(function (blobResponse) {
                return URL.createObjectURL(blobResponse);
            }).catch(function(error) {
                if (error.message == 401) {
                    console.log("Unauthorised, trying to get a new token");
                    self.requests.setNewToken().then(function() {
                        // create the services with the new token
                        self.getNewCurrentImage();
                        self.createSocketConnection();
                    });
                    return;
                }
                console.error(error);
            });
        },

        checkAuthentication () {
            if (!this.requests.authorisationToken) {
                console.log("No Authorisation token has been set yet");
                // we don't get the authorisation token straight away
                // if it is not set, there is no point trying to request data
                return false;
            }
            return true;
        },

        createSocketConnection () {
            this.socketConnection = io("http://localhost:5000",
                {
                    extraHeaders: {
                        "Authorization": "Bearer " + this.requests.authorisationToken
                    }
                }
            );

            this.socketConnection.on("image-change-update", () => {
                this.getNewCurrentImage();
            });

            this.socketConnection.on("disconnect", () => {
                // if the webpage is still running try and reconnect
                this.createSocketConnection();
            });
        },
    },

    mounted: async function() {
        let self = this;

        while (!this.requests.authorisationToken) {
            console.log("Waiting for authorisation token");
            await new Promise(r => setTimeout(r, 1000));
        }

        this.getNewCurrentImage();
        this.createSocketConnection();
    }
}

</script>

<template>
    <img :src="currentImage" id="currentImagePath" class="imageDisplay"/>
</template>

<style scoped>

.imageDisplay {
    max-width: 90%;
    max-height: 80vh;
    border: 5px solid #c4c4c4;
}

</style>
