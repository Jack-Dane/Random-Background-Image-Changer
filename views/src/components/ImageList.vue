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
  <div v-for="imagePath in imagePaths">
    <ImageListItem :imageURL="imagePath"/>
  </div>
</template>
