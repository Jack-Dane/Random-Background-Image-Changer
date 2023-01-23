
<script>

export default {

    data: () => ({
        pin: null,
        displayPin: "None"
    }),

    props: {
        requests: Object,
    },

    methods: {

        sendPinToFileHandler () {
            let self = this;
            fetch (
                "http://localhost:5000/imgur-pin",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + self.requests.authorisationToken
                    },
                    body: JSON.stringify({"pin": this.pin})
                }
            ).then(function (response) {
                // close the modal dialog window
                self.addPin();
                if (response.status == 400) {
                    alert("Pin isn't accepted by Imgur");
                }
            }).catch(function (error) {
                alert("Something went wrong, check the file handler logs");
            });
        },

        addPin () {
            this.displayPin = (this.displayPin == "None" ? "Block" : "None");
        }
    }
}
</script>

<template>
    <a href="#" v-on:click="addPin();" id="addPin" class="baseButton mainButton">Add Imgur Pin</a>
    <div id="addPinModalDialog" :style="{display: displayPin}">
        <input type="text" v-model="pin" class="modalDialogItem" placeholder="Imgur Pin"/>
        <a href="#" v-on:click="sendPinToFileHandler" id="sendPinToFileHandler" class="baseButton modalDialogItem">Send Pin</a>
    </div>
</template>

<style>

#addPin {
    left: calc(50% - 160px);
}

#addPinModalDialog {
    position: absolute;
    left: calc(50% - 150px);
    top: calc(50% - 125px);
    width: 300px;
    background: linear-gradient(#000e2e, #020817);
    border: 5px solid #ffc663;
}

.modalDialogItem {
    display: block;
    margin: 20px;
    width: calc(100% - 40px) !important;
}

</style>
