<template>
  <div class="item">
    <div class="details">
      <img :src="imageURL"/>
    </div>
  </div>
</template>

<script>
export default {
  props: ['imageURL']
}
</script>

<style scoped>

img {
  width: 100%;
}

</style>
