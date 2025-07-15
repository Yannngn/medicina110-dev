<script setup lang="ts">
interface SectionIndicatorProps {
  sectionIds: string[]
  activeSection: number
}

defineProps<SectionIndicatorProps>()

const emit = defineEmits<{
  scrollToSection: [index: number]
}>()

function handleScrollToSection(index: number) {
  emit('scrollToSection', index)
}
</script>

<template>
  <!-- Section Indicator/Roller -->
  <div class="fixed right-4 md:right-8 top-1/2 -translate-y-1/2 z-50 flex flex-col gap-4 md:gap-8">
    <button v-for="(id, idx) in sectionIds" :key="id" @click="handleScrollToSection(idx)"
      :aria-label="`Ir para seção ${id}`" class="size-2 rounded-full transition-all duration-200" :style="{
        backgroundColor:
          activeSection === idx
            ? 'var(--color-accent)'
            : 'var(--color-bg-secondary)',
        border:
          activeSection === idx
            ? '2px solid var(--color-border)'
            : '2px solid var(--color-border)',
        boxShadow:
          activeSection === idx
            ? '0 0 16px 0 var(--color-accent-soft)'
            : 'none',
        scale: activeSection === idx ? 1.25 : 1,
      }"></button>
  </div>
</template>
