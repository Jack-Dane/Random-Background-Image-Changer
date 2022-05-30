<script setup>
import { RouterLink, RouterView } from 'vue-router'
import CurrentImage from '@/components/CurrentImage.vue'
</script>

<template>
  
  <header>
    <div class="wrapper">
      <CurrentImage/>
    </div>
  </header>

</template>

<style>

@import '@/assets/base.css';

header {
  width: 100%;
}

</style>
