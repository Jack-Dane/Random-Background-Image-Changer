<script setup>
import { RouterLink, RouterView } from 'vue-router'
import CurrentImage from '@/components/CurrentImage.vue'
import ImageList from '@/components/ImageList.vue'
</script>

<template>
  <header>
    <div class="wrapper">
      <CurrentImage id="currentImage"/>
    </div>
  </header>

  <ImageList/>
</template>

<style>
@import '@/assets/base.css';

header {
  display: inline-block;
  padding: 0px;
  margin: 0px;
  width: calc(50% - 2px);
}

</style>
