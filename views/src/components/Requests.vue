
<script>

export default class{

    constructor() {
        this.authorisationToken = null;
        this.clientId = import.meta.env.VITE_CLIENT_ID;
        this.clientSecret = import.meta.env.VITE_CLIENT_SECRET;
        this.brokenToken = false;
        this.setAuthorisationToken();
    }

    async setNewToken() {
        this.brokenToken = true;
        await this.setAuthorisationToken();
    }

    async setAuthorisationToken() {
        if (localStorage.authorisationToken && !this.brokenToken) {
            this.authorisationToken = localStorage.authorisationToken;
            return;
        }

        let self = this;
        await fetch(
            "http://localhost:5000/token",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "clientId": this.clientId,
                    "clientSecret": this.clientSecret,
                })
            }
        ).then(function(response) {
            return response.json();
        }).then(function(jsonResponse) {
            self.authorisationToken =  jsonResponse["token"];
            localStorage.authorisationToken = self.authorisationToken;
        });
        this.brokenToken = false;
    }
}

</script>
