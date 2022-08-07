
<script>

import Requests from "@/components/Requests.vue";

export default {

    data: () => ({
        requests: new Requests(),
        currentImagePath: null,
    }),

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
    <a href="#" v-on:click="changeBackground();" id="nextImage">Next Image</a>
</template>

<style>

#nextImage {
    width: 150px;
    left: calc(50% - 75px);
    position: absolute;
    bottom: 15px;
    color: #000e2e;
    text-decoration: none;
    background-color: #ffc663;
    padding: 10px 15px 10px 15px;
    border-radius: 5px;
}

</style>
