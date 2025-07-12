<script setup lang="ts">
import 'vue3-carousel/carousel.css'
import { Carousel, Slide } from 'vue3-carousel'
const props = defineProps<{
  pictures: { src: string; alt: string }[]
}>()
</script>

<template>
  <Carousel :items-to-show="1" :wrap-around="true" :mouse-drag="true">
    <Slide v-for="(pic, idx) in props.pictures" :key="pic.src + idx">
      <div class="flex items-center justify-center">
        <img :src="pic.src" :alt="pic.alt" class="max-h-[40vh] md:max-h-[50vh] w-auto" />
      </div>
    </Slide>
  </Carousel>

</template>

<style scoped>
.carousel__slide {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>