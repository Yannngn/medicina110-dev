<script setup lang="ts">
interface ThemeToggleProps {
  theme: string
}

defineProps<ThemeToggleProps>()

const emit = defineEmits<{
  toggleTheme: []
}>()

function handleToggleTheme() {
  emit('toggleTheme')
}
</script>

<template>
  <!-- Theme toggle button (top right) -->
  <div class="fixed top-3 right-3 z-50">
    <button class="flex items-center justify-center size-9 md:size-12 rounded-full shadow-lg transition hover:scale-110"
      @click="handleToggleTheme" :aria-label="theme === 'dark' ? 'Ativar modo claro' : 'Ativar modo escuro'" :style="{
        backgroundColor: 'var(--color-bg-secondary)',
        color: 'var(--color-text)',
      }">
      <span v-if="theme === 'dark'">☀️</span>
      <span v-else>🌙</span>
    </button>
  </div>
</template>
