
<script>
export default {
  data: () => ({
    imagePaths: null,
    currentImagePath: null,
  }),

  created() {
    this.getCurrentImagePath();
  },

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
  }
}

</script>

<template>
  <div class="greetings">
    <h1>Current Image</h1>
    <img :src="currentImagePath"/>
    <br/>
    <a href="#" v-on:click="changeBackground();">Next Image</a>
  </div>
</template>

<style scoped>
img {
  width: 400px;
}

h1 {
  font-weight: 500;
  font-size: 2.6rem;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
