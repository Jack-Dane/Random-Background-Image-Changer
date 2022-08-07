<script setup>

import { RouterLink, RouterView } from "vue-router";
import CurrentImage from "@/components/CurrentImage.vue";
import ChangeBackground from "@/components/ChangeBackground.vue";

import Requests from "@/components/Requests.vue";

var requests = new Requests();

</script>

<template>

  <header>
    <div class="wrapper">
      <div class="greetings">
        <h1>Background Changer</h1>
        <CurrentImage :requests="requests"/>
        <br/>
        <changeBackground :requests="requests"/>
      </div>
    </div>
  </header>

</template>

<style>

@import '@/assets/base.css';

template {
  height: 100vh;
}

header {
  background: linear-gradient(#000e2e, #020817);
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

h1 {
  color: #c4c4c4;
  margin-bottom: 5px;
}

.greetings {
  text-align: center;
  width: 100%;
  height: 100vh;
}

</style>
