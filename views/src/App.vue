<script setup>

import { RouterLink, RouterView } from "vue-router";
import CurrentImage from "@/components/CurrentImage.vue";
import ChangeBackground from "@/components/ChangeBackground.vue";
import Pin from "@/components/Pin.vue";

import Requests from "@/components/Requests.vue";
import { io } from 'socket.io-client';

var requests = new Requests();
var socketConnection = io("http://localhost:5000");

</script>

<template>

  <header>
    <div class="wrapper">
      <div class="greetings">
        <h1>Background Changer</h1>
        <CurrentImage :requests="requests" :socketConnection="socketConnection"/>
        <br/>
        <ChangeBackground :requests="requests"/>
        <Pin :requests="requests"/>
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

.baseButton {
    color: #000e2e;
    text-decoration: none;
    background-color: #ffc663;
    padding: 10px 15px 10px 15px;
    border-radius: 5px;
    width: 150px;
}

.mainButton {
    position: absolute;
    bottom: 15px;
}

</style>
