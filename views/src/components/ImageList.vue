<script setup>
import ImageListItem from './ImageListItem.vue'
</script>

<script>
export default {
  data: () => ({
    imagePaths: null,
  }),

  created() {
    this.getImagePaths();
  },

  methods: {
    async getImagePaths() {
      let imagePaths = await fetch("http://localhost:5000/background-images").then(
        response => response.json()
      ).then(function(jsonResponse) {
        return jsonResponse;
      });
      imagePaths.forEach(function(element, index) {
        imagePaths[index] = element.substring(element.indexOf("backgroundImages") - 1);
      });
      this.imagePaths = imagePaths;
    },
  }
}
</script>

<template>
  <div id="imageList">
    <ImageListItem :imageURL="imagePath" v-for="imagePath in imagePaths" class="ImageListItem"/>
  </div>
</template>

<style>

#imageList {
  vertical-align: top;
  display: inline-block;
  padding: 0px;
  margin: 0px;
  width: calc(50% - 2px);
}

</style>
