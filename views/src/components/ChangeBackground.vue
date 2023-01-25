
<script>

export default {

    data: () => ({
        currentImagePath: null,
    }),

    props: {
        requests: Object,
    },

    methods: {
        changeBackground() {
            let self = this;
            fetch(
                "http://localhost:5000/change-background",
                {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + self.requests.authorisationToken
                    }
                }
            ).then(function(response) {
                if (response.status == 200) {
                    return
                }
                throw new Error(response.status);
            }).catch(function(status) {
                if (error.message == 401) {
                    console.log("Unauthorised, trying to get a new token");
                    self.requests.setNewToken();
                    return;
                }
                console.error(error);
            });
        },
    }
}
</script>

<template>
    <a href="#" v-on:click="changeBackground();" id="nextImage" class="baseButton mainButton">Next Image</a>
</template>

<style>

#nextImage {
    left: calc(50% + 10px);
}

</style>
