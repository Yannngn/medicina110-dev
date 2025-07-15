<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from "vue";
// @ts-expect-error vue3-word-cloud has no types
import Vue3WordCloud from "vue3-word-cloud";

// Theme-aware color lists using CSS variables
const lightColors = [
  "var(--color-accent)",
  "var(--color-slate-900)",
  "var(--color-slate-700)",
  "var(--color-slate-500)",
  "var(--color-slate-400)",
];

const darkColors = [
  "var(--color-accent)",
  "var(--color-slate-100)",
  "var(--color-slate-300)",
  "var(--color-slate-500)",
  "var(--color-slate-600)",
];

const theme = ref(
  document.documentElement.classList.contains("dark") ? "dark" : "light",
);

function getThemeColors() {
  return theme.value === "dark" ? darkColors : lightColors;
}

function updateTheme() {
  theme.value = document.documentElement.classList.contains("dark")
    ? "dark"
    : "light";
}

onMounted(() => {
  window.addEventListener("transitionend", updateTheme);
  window.addEventListener("animationend", updateTheme);
  window.addEventListener("change", updateTheme);
  window.addEventListener("themechange", updateTheme);
  // Also listen for manual toggles
  const observer = new MutationObserver(updateTheme);
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["class"],
  });
  // Store observer for cleanup
  WordCloudThemeObserver.value = observer;
});

const WordCloudThemeObserver = ref<MutationObserver | null>(null);

onUnmounted(() => {
  window.removeEventListener("transitionend", updateTheme);
  window.removeEventListener("animationend", updateTheme);
  window.removeEventListener("change", updateTheme);
  window.removeEventListener("themechange", updateTheme);
  if (WordCloudThemeObserver.value) {
    WordCloudThemeObserver.value.disconnect();
    WordCloudThemeObserver.value = null;
  }
});

const props = defineProps<{
  words: { text: string; value: number }[];
}>();

const wordCloud = computed(() => {
  if (!props.words || props.words.length === 0) {
    return [];
  }
  if (Array.isArray(props.words[0])) {
    return props.words;
  }
  return props.words.map((word) => [word.text, word.value]);
});

// const colorFn = ([text, _weight]: [string, number]) => {
//     // Assign a random slate color based on the text hash
//     let hash = 0
//     for (let i = 0; i < text.length; i++) {
//         hash = text.charCodeAt(i) + ((hash << 5) - hash)
//     }
//     const idx = Math.abs(hash) % slateColors.length
//     return slateColors[idx]
// }

const colorFn = ([, weight]: [string, number]) => {
  // Directly map weight (1-5) to color index (0-4)
  const colors = getThemeColors();
  const idx = Math.max(0, Math.min(colors.length - 1, 5 - weight));
  return colors[idx];
};

const rotationFn = ([text,]: [string, number]) => {
  // Use a hash of the text to get a pseudo-random rotation in 0, 90, 180, or 270 degrees
  let hash = 0;
  for (let i = 0; i < text.length; i++) {
    hash = text.charCodeAt(i) + ((hash << 5) - hash);
  }
  const rotations = [0, 45, 90, 270, 315];
  const idx = Math.abs(hash) % rotations.length;
  return rotations[idx];
};
</script>

<template>
  <section id="wordcloud" class="snap-center">

    <!-- #TODO fix height, it should be dynamic based on screen size -->
    <div class="container section-component justify-center items-center">
      <div class="word-cloud">
        <Vue3WordCloud v-if="wordCloud.length > 0" :words="wordCloud" :color="colorFn" :rotation="rotationFn"
          rotation-unit="deg" :spacing="1" :draw-out-of-bound="false" :shrink-to-fit="true" shape="diamond" />
        <div v-else class="md:text-xl text-[var(--color-footer)]">
          Carregando nuvem de palavras...
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.word-cloud {
  width: 80vw;
  height: 80vh;
}
</style>
