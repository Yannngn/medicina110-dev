<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";
import BackgroundPattern from "./components/BackgroundPattern.vue";
import DonorTable from "./components/DonorTable.vue";
import HeroPage from "./components/HeroPage.vue";
import ImagesCarousel from "./components/ImagesCarousel.vue";
import QRCode from "./components/QRCode.vue";
import MentiMeter from "./components/WordCloud.vue";
import {
  fetchData,
  topDonors,
  latestDonations,
  wordCloud,
} from "./services/data-service";

// Data is now managed by data-service.ts

const allGroup = [
  {
    src: "/medicina110-dev/church-photo.jpg",
    alt: "Imagem da Turma na Igreja São Francisco",
  },
  {
    src: "/medicina110-dev/hospital-photo.jpg",
    alt: "Imagem da Turna no Hospital Universitário Lauro Wanderley",
  },
  {
    src: "/medicina110-dev/comissao.jpg",
    alt: "Comissão",
  },
];

const smallGroups = [
  {
    src: "/medicina110-dev/grupo_1.jpg",
    alt: "Grupo 1",
  },
  {
    src: "/medicina110-dev/grupo_2.jpg",
    alt: "Grupo 2",
  },
  {
    src: "/medicina110-dev/grupo_3.jpg",
    alt: "Grupo 3",
  },
  {
    src: "/medicina110-dev/grupo_4.jpg",
    alt: "Grupo 4",
  },
  {
    src: "/medicina110-dev/grupo_5.jpg",
    alt: "Grupo 5",
  },
  {
    src: "/medicina110-dev/grupo_6.jpg",
    alt: "Grupo 6",
  },
  {
    src: "/medicina110-dev/grupo_7.jpg",
    alt: "Grupo 7",
  },
];

const sectionIds = ["hero", "images", "qrcode", "tables", "wordcloud"];
const activeSection = ref(0);
const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
const theme = ref(prefersDark ? "dark" : "light");

let observers: IntersectionObserver[] = [];

onMounted(() => {
  // Set initial theme based on user/system preference
  document.documentElement.classList.toggle("dark", theme.value === "dark");

  fetchData(); // Fetch data when the component mounts

  sectionIds.forEach((id, idx) => {
    const el = document.getElementById(id);
    if (el) {
      const observer = new window.IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              activeSection.value = idx;
            }
          });
        },
        { threshold: 0.5 },
      );
      observer.observe(el);
      observers.push(observer);
    }
  });
});

onBeforeUnmount(() => {
  observers.forEach((observer) => observer.disconnect());
  observers = [];
});

function scrollToSection(idx: number) {
  const el = document.getElementById(sectionIds[idx]);
  if (el) {
    el.scrollIntoView({ behavior: "smooth" });
  }
}

function toggleTheme() {
  theme.value = theme.value === "light" ? "dark" : "light";
  document.documentElement.classList.toggle("dark", theme.value === "dark");
}


const isMenuOpen = ref(false);

</script>

<template>
  <BackgroundPattern />
  <!-- Mobile: Drop-down floating menu (top left) -->
  <div class="fixed top-3 left-3 z-50">
    <button @click="isMenuOpen = !isMenuOpen"
      class="flex items-center justify-center size-9 md:size-12 rounded-full shadow-lg transition hover:scale-110">
      <span class="text-2xl">☰</span>
    </button>
    <transition name="dropup-menu">
      <div v-if="isMenuOpen" class="flex flex-col gap-2 p-2 absolute left-0 mt-2 rounded-lg shadow-lg backdrop-blur"
        style="min-width:max-content; width:auto;">
        <button @click="scrollToSection(0); isMenuOpen = false;"
          class="text-xs m-2 p-2 rounded-lg shadow-md transition">
          🏠 Início
        </button>
        <button @click="scrollToSection(1); isMenuOpen = false;"
          class="text-xs m-2 p-2 rounded-lg shadow-md transition">
          👩‍⚕️ Conheça a Turma
        </button>
        <button @click="scrollToSection(2); isMenuOpen = false;"
          class="text-xs m-2 p-2 rounded-lg shadow-md transition">
          💰 Faça sua Doação
        </button>
        <button @click="scrollToSection(3); isMenuOpen = false;"
          class="text-xs m-2 p-2 rounded-lg shadow-md transition">
          🏆 Ver Doadores
        </button>
        <button @click="scrollToSection(4); isMenuOpen = false;"
          class="text-xs m-2 p-2 rounded-lg shadow-md transition">
          ✨ Nuvem de Doadores
        </button>
      </div>
    </transition>
  </div>
  <div class="fixed top-3 right-3 z-50">
    <button
      class="flex items-center justify-center size-9 md:size-12 rounded-full shadow-lg transition hover:scale-110"
      @click="toggleTheme" :aria-label="theme === 'dark' ? 'Ativar modo claro' : 'Ativar modo escuro'" :style="{
        backgroundColor: 'var(--color-bg-secondary)',
        color: 'var(--color-text)',
      }">
      <span v-if="theme === 'dark'">☀️</span>
      <span v-else>🌙</span>
    </button>
  </div>
  <main class="overflow-y-auto snap-y snap-mandatory no-scrollbar">
    <div class="relative w-full h-screen">
      <section id="hero" class="snap-center">
        <HeroPage @doctors="scrollToSection(1)" @donate="scrollToSection(2)" @donators="scrollToSection(3)"
          @cloud="scrollToSection(4)" />
      </section>
      <section id="images" class="snap-center">
        <div class="container section-component rows-component">
          <ImagesCarousel :pictures="allGroup" />
          <ImagesCarousel :pictures="smallGroups" />
        </div>
      </section>
      <section id="qrcode" class="snap-center">
        <QRCode />
      </section>
      <section id="tables" class="snap-center">
        <div class="container section-component columns-component md:gap-8">
          <DonorTable title="🏆 Maiores Doadores" :data="topDonors" />
          <DonorTable title="✨ Últimos Doadores" :data="latestDonations" />
        </div>
      </section>
      <section id="wordcloud" class="snap-center">
        <div class="container section-component">
          <MentiMeter :words="wordCloud" />
        </div>
      </section>
      <!-- Roller/Indicator -->
      <div class="fixed right-4 md:right-8 top-1/2 -translate-y-1/2 z-50 flex flex-col gap-4 md:gap-8">
        <button v-for="(id, idx) in sectionIds" :key="id" @click="scrollToSection(idx)"
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
      <footer class="relative w-full mb-8 md:mb-0 md:bottom-16" style="color: var(--color-footer)">
        <p>Agradecimentos à Comissão de Formatura.</p>
        Criado por
        <a href="https://github.com/Yannngn" target="_blank" rel="noopener" class="underline hover:text-blue-600"
          style="color: var(--color-accent)">@Yannngn</a>
      </footer>
    </div>
  </main>
</template>

<style>
section {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.section-component {
  min-height: 100vh;
  min-width: 100vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: var(--color-bg-gradient);
  transition:
    box-shadow 0.2s,
    border-color 0.2s;
}

.columns-component {
  display: flex;
  flex-direction: column;
}

.rows-component {
  min-width: 100%;
  display: flex;
  justify-content: center;
}

@media (min-width: 768px) {
  .columns-component {
    flex-direction: row;
    justify-content: center;
    gap: 4rem;
  }

  .rows-component {
    max-height: 50%;
    min-width: none;
    flex-direction: column;
  }
}
</style>
