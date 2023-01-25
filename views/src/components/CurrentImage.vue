
<script>

export default {

    data: () => ({
        currentImageHash: null,
        currentImage: null
    }),

    props: {
        requests: Object,
        socketConnection: Object
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
                    self.requests.setNewToken();
                    return;
                }
                console.error(error);
            });
        },

        checkAuthentication() {
            if (!this.requests.authorisationToken) {
                console.log("No Authorisation token has been set yet");
                // we don't get the authorisation token straight away
                // if it is not set, there is no point trying to request data
                return false;
            }
            return true;
        },
    },

    mounted: async function() {
        let self = this;
        this.getNewCurrentImage();

        this.socketConnection.on("image-change-update", () => {
            this.getNewCurrentImage();
        });
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
