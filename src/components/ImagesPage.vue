<script setup lang="ts">
import ImagesCarousel from './ImagesCarousel.vue'

interface Picture {
    src: string
    alt: string
}

const { allGroup, smallGroups } = defineProps<{
    allGroup: Picture[]
    smallGroups: Picture[]
}>()

</script>

<template>
    <section id="images" class="snap-center">
        <div class="container section-component rows-component">
            <ImagesCarousel :pictures="allGroup" />
            <ImagesCarousel :pictures="smallGroups" />
        </div>
    </section>
</template>

<style scoped></style>