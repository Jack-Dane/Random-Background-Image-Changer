
<script>
export default {
  data: () => ({
    currentImagePath: null,
  }),

  methods: {
    async getCurrentImagePath() {
      let currentImagePath = await fetch("http://localhost:5000/current-image").then(
        response => response.json()
      ).then(function(jsonResponse){
        return jsonResponse;
      });
      this.currentImagePath = currentImagePath.substring(currentImagePath.indexOf("backgroundImages") - 1);
    },

    changeBackground() {
      fetch("http://localhost:5000/change-background");
    }
  },

  mounted: function() {
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
    <a href="#" v-on:click="changeBackground();">Next Image</a>
  </div>
</template>

<style scoped>

.imageDisplay {
  max-width: 90%;
  max-height: 80vh;
}

.greetings {
  text-align: center;
  width: 100%;
}
</style>
