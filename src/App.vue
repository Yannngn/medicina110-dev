<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";
import BackgroundPattern from "./components/BackgroundPattern.vue";
import HeroPage from "./components/HeroPage.vue";
import ImagesPage from "./components/ImagesPage.vue";
import QRCode from "./components/QRCode.vue";
import TablesPage from "./components/TablesPage.vue";
import MentiMeter from "./components/WordCloud.vue";
import NavigationMenu from "./components/NavigationMenu.vue";
import ThemeToggle from "./components/ThemeToggle.vue";
import SectionIndicator from "./components/SectionIndicator.vue";
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

</script>

<template>
  <BackgroundPattern />
  <NavigationMenu :sectionIds="sectionIds" @scrollToSection="scrollToSection" />
  <ThemeToggle :theme="theme" @toggleTheme="toggleTheme" />
  <main class="overflow-y-auto snap-y snap-mandatory no-scrollbar">
    <div class="relative w-full h-screen">
      <HeroPage @doctors="scrollToSection(1)" @donate="scrollToSection(2)" @donators="scrollToSection(3)"
        @cloud="scrollToSection(4)" />
      <ImagesPage :allGroup="allGroup" :smallGroups="smallGroups" />
      <QRCode />
      <TablesPage :topDonors="topDonors" :latestDonations="latestDonations" />
      <MentiMeter :words="wordCloud" />
      <SectionIndicator :sectionIds="sectionIds" :activeSection="activeSection" @scrollToSection="scrollToSection" />
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
  justify-content: center;
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

.section-h1 {
  text-align: center;
  font-size: var(--text-6xl);
  line-height: var(--tw-leading, var(--text-6xl--line-height));
}

.section-h2 {
  text-align: center;
  font-size: var(--text-xl);
  line-height: var(--tw-leading, var(--text-xl--line-height));
}

.section-p {
  text-align: center;
  font-size: var(--text-base);
  line-height: var(--tw-leading, var(--text-base--line-height));
}

@media (min-height: 433px) and (min-width: 768px) {
  .section-h1 {
    font-size: var(--text-8xl);
    line-height: var(--tw-leading, var(--text-8xl--line-height));
  }

  .columns-component {
    flex-direction: row;
    justify-content: center;
    max-height: 100%;
    gap: 8rem;
  }

  .rows-component {
    max-height: 50%;
    min-width: none;
    flex-direction: column;
  }

  .section-h2 {
    font-size: var(--text-4xl);
    line-height: var(--tw-leading, var(--text-4xl--line-height));
  }

  .section-p {
    font-size: var(--text-xl);
    line-height: var(--tw-leading, var(--text-xl--line-height));
  }
}
</style>
