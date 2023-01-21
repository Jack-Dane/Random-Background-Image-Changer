
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
                return response.blob();
            }).then(function (blobResponse) {
                return URL.createObjectURL(blobResponse);
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
                return response.json();
            }).then(function(jsonResponse){
                return jsonResponse["hash"];
            }).catch(function(error) {
                self.requests.handleAuthErrors(error);
            });
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
        setInterval(function() {
            self.setCurrentImage();
        }, 500);
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
