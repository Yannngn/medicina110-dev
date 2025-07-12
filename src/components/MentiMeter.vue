<script setup lang="ts">
import { computed } from 'vue'
// @ts-ignore
import Vue3WordCloud from 'vue3-word-cloud'

// Theme-aware color lists using CSS variables
const lightColors = [
    'var(--color-accent)',
    '#94a3b8',           // slate-800
    '#94a3b8',           // slate-600
    '#cbd5e1',           // slate-500
    '#e2e8f0',           // slate-400
]

const darkColors = [
    'var(--color-accent)',
    '#94a3b8',           // slate-200
    '#64748b',           // slate-300
    '#475569',           // slate-400
    '#334155',           // slate-500
]

function getThemeColors() {
  return document.documentElement.classList.contains('dark') ? darkColors : lightColors
}

const props = defineProps<{
    words: { text: string; value: number }[]
}>()

const wordCloud = computed(() => {
    if (!props.words || props.words.length === 0) {
        return []
    }
    if (Array.isArray(props.words[0])) {
        return props.words
    }
    return props.words.map((word) => [word.text, word.value])
})


// const colorFn = ([text, _weight]: [string, number]) => {
//     // Assign a random slate color based on the text hash
//     let hash = 0
//     for (let i = 0; i < text.length; i++) {
//         hash = text.charCodeAt(i) + ((hash << 5) - hash)
//     }
//     const idx = Math.abs(hash) % slateColors.length
//     return slateColors[idx]
// }

const colorFn = ([_, weight]: [string, number]) => {
  // Directly map weight (1-5) to color index (0-4)
  const colors = getThemeColors()
  const idx = Math.max(0, Math.min(colors.length - 1, 5 - weight))
  return colors[idx]
}

const rotationFn = ([text, _weight]: [string, number]) => {
    // Use a hash of the text to get a pseudo-random rotation in 0, 90, 180, or 270 degrees
    let hash = 0
    for (let i = 0; i < text.length; i++) {
        hash = text.charCodeAt(i) + ((hash << 5) - hash)
    }
    const rotations = [0, 45, 90, 270, 315]
    const idx = Math.abs(hash) % rotations.length
    return rotations[idx]
}
</script>

<template>
    <div class="flex flex-wrap w-full h-164 md:h-128 p-4 items-center justify-center overflow-x-hidden">
        <Vue3WordCloud v-if="wordCloud.length > 0" :words="wordCloud" :color="colorFn" :rotation="rotationFn"
            rotation-unit="deg" :spacing=1 :draw-out-of-bound="false" :shrink-to-fit="true" shape="diamond" />
        <div v-else class="text-sm text-[var(--color-footer)]">
            Carregando nuvem de palavras...
        </div>
    </div>
</template>
