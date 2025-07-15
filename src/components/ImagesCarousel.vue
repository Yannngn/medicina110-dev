<script setup lang="ts">
// @ts-expect-error splidejs has no types for Vue 3
import { Splide, SplideSlide } from "@splidejs/vue-splide";
// @ts-expect-error splidejs has no types for Vue 3
import "@splidejs/vue-splide/css";

const props = defineProps<{
  pictures: { src: string; alt: string }[];
}>();

const options = {
  type: "loop",
  drag: true,
  perPage: 1,
  rewind: true,
};
</script>

<template>
  <Splide :options="options" aria-label="Image Carousel">
    <SplideSlide v-for="(pic, idx) in props.pictures" :key="pic.src + idx">
      <div class="flex items-center justify-center h-full">
        <img
          :src="pic.src"
          :alt="pic.alt"
          class="max-h-[50vh] w-auto"
        />
      </div>
    </SplideSlide>
  </Splide>
</template>

<style scoped>

</style>
