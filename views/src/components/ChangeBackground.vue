
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
            try {
                fetch(
                    "http://localhost:5000/change-background",
                    {
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": "Bearer " + self.requests.authorisationToken
                        }
                    }
                );
                self.requests.passedAuth();
            } catch(error) {
                self.requests.handleAuthErrors(error);
            }
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
