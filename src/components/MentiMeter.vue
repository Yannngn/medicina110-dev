<script setup lang="ts">
import { computed } from 'vue'
// @ts-ignore
import Vue3WordCloud from 'vue3-word-cloud' 

const props = withDefaults(defineProps<{
    words: { text: string; value: number }[]
    minFontSize?: number
    maxFontSize?: number
}>(), {
    minFontSize: 16,
    maxFontSize: 64,
})

const values = computed(() => props.words.map(w => w.value))
const minValue = computed(() => Math.min(...values.value))
const maxValue = computed(() => Math.max(...values.value))

const wordCloudData = computed(() => {
    const fontRange = props.maxFontSize - props.minFontSize
    const valueRange = maxValue.value - minValue.value || 1

    return props.words.map(word => {
        const normalizedValue = (word.value - minValue.value) / valueRange
        const fontSize = props.minFontSize + normalizedValue * fontRange
        return [word.text, fontSize]
    })
})

const colorFn = ([_text, weight]: [string, number]) => {
    const midSize = (props.minFontSize + props.maxFontSize) / 2
    const highSize = midSize + (props.maxFontSize - midSize) / 2
    if (weight > highSize) return '#a0deff' // Larger words
    if (weight > midSize) return '#58b5e1' // Medium words
    return '#2a8dc2' // Smaller words
}
</script>

<template>
    <div class="w-full h-128 p-4 flex items-center justify-center">
        <Vue3WordCloud :words="wordCloudData" font-family="Arial, sans-serif" :color="colorFn">
            <template #default="{ text, weight, color }">
                <div :style="{ color: color, fontSize: `${weight}px` }"
                    class="transition-all duration-300 hover:scale-110 cursor-pointer">
                    {{ text }}
                </div>
            </template>
        </Vue3WordCloud>
    </div>
</template>
