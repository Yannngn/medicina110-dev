<script setup lang="ts">
import { ref } from 'vue'

interface NavigationProps {
  sectionIds: string[]
}

defineProps<NavigationProps>()

const emit = defineEmits<{
  scrollToSection: [index: number]
}>()

const isMenuOpen = ref(false)

function handleScrollToSection(index: number) {
  emit('scrollToSection', index)
  isMenuOpen.value = false
}
</script>

<template>
  <!-- Mobile: Drop-down floating menu (top left) -->
  <div class="fixed top-3 left-3 z-50">
    <button @click="isMenuOpen = !isMenuOpen"
      class="flex items-center justify-center size-9 md:size-12 rounded-full shadow-lg transition hover:scale-110">
      <span class="text-2xl">☰</span>
    </button>
    <transition name="dropup-menu">
      <div v-if="isMenuOpen" class="flex flex-col gap-2 p-2 absolute left-0 mt-2 rounded-lg shadow-lg backdrop-blur"
        style="min-width:max-content; width:auto;">
        <button @click="handleScrollToSection(0)" class="text-xs m-2 p-2 rounded-lg shadow-md transition">
          🏠 Início
        </button>
        <button @click="handleScrollToSection(1)" class="text-xs m-2 p-2 rounded-lg shadow-md transition">
          👩‍⚕️ Conheça a Turma
        </button>
        <button @click="handleScrollToSection(2)" class="text-xs m-2 p-2 rounded-lg shadow-md transition">
          💰 Faça sua Doação
        </button>
        <button @click="handleScrollToSection(3)" class="text-xs m-2 p-2 rounded-lg shadow-md transition">
          🏆 Ver Doadores
        </button>
        <button @click="handleScrollToSection(4)" class="text-xs m-2 p-2 rounded-lg shadow-md transition">
          ✨ Nuvem de Doadores
        </button>
        <a href="https://github.com/Yannngn" target="_blank" rel="noopener" class="underline text-xs hover:text-accent"
          style="color: var(--color-background)">@Yannngn</a>
      </div>
    </transition>
  </div>
</template>

<style scoped>
/* Transição do menu drop-up */
.dropup-menu-enter-active,
.dropup-menu-leave-active {
  transition: all 0.3s ease;
}

.dropup-menu-enter-from,
.dropup-menu-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.dropup-menu-enter-to,
.dropup-menu-leave-from {
  opacity: 1;
  transform: translateY(0);
}
</style>
