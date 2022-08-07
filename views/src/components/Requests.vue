
<script>

export default class{

    constructor() {
        this.authorisationToken = null;
        this.clientId = import.meta.env.VITE_CLIENT_ID;
        this.clientSecret = import.meta.env.VITE_CLIENT_SECRET;
        this.tryReauthenticate = false;
        this.authenticationError = false;
        this.mount();
    }
    
    mount() {
        this.getAuthorisationToken();

        let self = this;
        setInterval(function () {
            self.pollMethod();
        }, 500);
    }
        
    pollMethod() {
        if (self.authenticationError) {
            console.error(self.authenticationError);
            return; 
        }

        if (self.tryReauthenticate) {
            console.log("Getting New Token");
            self.getAuthorisationToken();
        }
    }

    handleAuthErrors(error) {
        if (!this.tryReauthenticate) {
            this.tryReauthenticate = true;
            return;
        }

        this.authenticationError = error;
    }

    passedAuth() {
        this.tryReauthenticate = false;
        this.authenticationError = false;
    }

    async getAuthorisationToken() {
        if (localStorage.authorisationToken && !this.tryReauthenticate) {
            this.authorisationToken = localStorage.authorisationToken;
            return;
        }

        this.authorisationToken = await fetch(
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
            return jsonResponse["token"];
        });
        localStorage.authorisationToken = this.authorisationToken;
    }
}

</script>
