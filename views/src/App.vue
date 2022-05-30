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
  background: linear-gradient(#000e2e, #020817);
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

</style>
