
<script>
export default {
  data: () => ({
    authorisationToken: null,
    clientId: import.meta.env.VITE_CLIENT_ID,
    clientSecret: import.meta.env.VITE_CLIENT_SECRET,
    currentImagePath: null,
  }),

  methods: {
    async getCurrentImagePath() {
      if (!this.authorisationToken) {
        // we don't get the authorisation token straigh away
        // if it is not set, there is no point trying to request data
        return;
      }

      let currentImagePath = await fetch(
        "http://localhost:5000/current-image",
        {
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + this.authorisationToken
          }
        }
      ).then(
        response => response.json()
      ).then(function(jsonResponse){
        return jsonResponse;
      });
      currentImagePath = currentImagePath.substring(currentImagePath.indexOf("backgroundImages") - 1);
      this.currentImagePath = encodeURIComponent(currentImagePath);
    },

    changeBackground() {
      fetch(
        "http://localhost:5000/change-background",
        {
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + this.authorisationToken
          }
        }
      );
    },

    async getAuthorisationToken() {
      if (localStorage.authorisationToken) {
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
      ).then(
        response => response.json()
      ).then(function(jsonResponse){
        return jsonResponse["token"];
      });
      localStorage.authorisationToken = this.authorisationToken;
    }
  },

  mounted: function() {
    this.getAuthorisationToken();

    this.getCurrentImagePath();

    let self = this;
    setInterval(function () {
      self.getCurrentImagePath();
    }, 200); 
  }
}

</script>

<template>
  <div class="greetings">
    <h1>Background Changer</h1>
    <img :src="currentImagePath" id="currentImagePath" class="imageDisplay"/>
    <br/>
    <a href="#" v-on:click="changeBackground();" id="nextImage">Next Image</a>
  </div>
</template>

<style scoped>

template {
  height: 100vh;
}

h1 {
  color: #c4c4c4;
  margin-bottom: 5px;
}

.imageDisplay {
  max-width: 90%;
  max-height: 80vh;
  border: 5px solid #c4c4c4;
}

.greetings {
  text-align: center;
  width: 100%;
  height: 100vh;
}

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
