
<script>

export default {

    data: () => ({
        currentImagePath: null,
    }),

    props: {
        requests: Object,
    },

    methods: {

        async getCurrentImagePath() {
            let self = this;
            if (!this.requests.authorisationToken) {
                console.log("No Authorisation token has been set yet");
                // we don't get the authorisation token straigh away
                // if it is not set, there is no point trying to request data
                return;
            }

            let currentImagePath = await fetch(
                "http://localhost:5000/current-image",
                {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + self.requests.authorisationToken
                    }
                }
            ).then(function(response) {
                return response.json();
            }).catch(function(error) {
                self.requests.handleAuthErrors(error);
            });
            if (currentImagePath) {
                currentImagePath = currentImagePath.substring(currentImagePath.indexOf("backgroundImages") - 1);
                this.currentImagePath = encodeURIComponent(currentImagePath);
                this.requests.passedAuth();
            }
        },
    },

    mounted: async function() {
        let self = this;
        setInterval(function() {
            self.getCurrentImagePath();
        }, 500);
    }
}

</script>

<template>
    <img :src="currentImagePath" id="currentImagePath" class="imageDisplay"/>
</template>

<style scoped>

.imageDisplay {
    max-width: 90%;
    max-height: 80vh;
    border: 5px solid #c4c4c4;
}

</style>
