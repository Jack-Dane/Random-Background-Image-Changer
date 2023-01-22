
<script>

export default {

    data: () => ({
        currentImageHash: null,
        currentImage: null
    }),

    props: {
        requests: Object,
    },

    methods: {

        async getNewCurrentImage () {
            let self = this;

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

        async setCurrentImage() {
            let self = this;
            if (!this.requests.authorisationToken) {
                console.log("No Authorisation token has been set yet");
                // we don't get the authorisation token straight away
                // if it is not set, there is no point trying to request data
                return;
            }

            let currentImageHash = await fetch(
                "http://localhost:5000/current-image-hash",
                {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + self.requests.authorisationToken
                    },
                }
            ).then(function(response) {
                if (response.status == 200) {
                    return response.json();
                }
                throw new Error(response.status);
            }).then(function(jsonResponse){
                return jsonResponse["hash"];
            }).catch(function(error) {
                if (error.message == 401) {
                    console.log("Unauthorised, trying to get a new token");
                    self.requests.setNewToken();
                    return "unauthorised";
                }
                console.error(error);
            });

            if (currentImageHash == "unauthorised") {
                // we will be getting a new token, so we shouldn't try to get the
                return;
            }

            if (!this.currentImageHash || this.currentImageHash != currentImageHash) {
                // the image only needs to be set if the hash is different or we don't currently have a hash
                // if we don't have a hash, we don't have an image
                this.getNewCurrentImage();
                this.currentImageHash = currentImageHash;
            }
        },
    },

    mounted: async function() {
        let self = this;
        this.setCurrentImage();
        setInterval(function() {
            self.setCurrentImage();
        }, 5000);
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
