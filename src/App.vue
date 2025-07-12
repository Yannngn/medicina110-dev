<script setup lang="ts">

import { onBeforeUnmount, onMounted, ref } from 'vue'
import Background from './components/Background.vue'
import DonorTable from './components/DonorTable.vue'
import Hero from './components/Hero.vue'
import Images from './components/Images.vue'
import QRCode from './components/QRCode.vue'
import MentiMeter from './components/MentiMeter.vue'

// Example data for demonstration
const topDonors = [
  { name: 'Maria' },
  { name: 'João' },
  { name: 'Ana Paula' },
  { name: 'Carlos Eduardo' },
  { name: 'Fernanda Lima' },
  { name: 'Ricardo Silva' },
  { name: 'Patrícia Gomes' }
]

const recentDonations = [
  { name: 'Lucas Souza' },
  { name: 'Beatriz Costa' },
  { name: 'Gabriel Rocha' },
  { name: 'Juliana Alves' },
  { name: 'Marcos Vinícius' },
  { name: 'Larissa Mendes' },
  { name: 'Felipe Oliveira' }
]

const allGroup = [
  {
    src: 'src/assets/church-photo.jpg',
    alt: 'Imagem da Turma na Igreja São Francisco'
  },
  {
    src: 'src/assets/hospital-photo.jpg',
    alt: 'Imagem da Turna no Hospital Universitário Lauro Wanderley'
  },
  {
    src: 'src/assets/comissao.jpg',
    alt: 'Comissão'
  },
]

const smallGroups = [

  {
    src: 'src/assets/grupo_1.jpg',
    alt: 'Grupo 1'
  },
  {
    src: 'src/assets/grupo_2.jpg',
    alt: 'Grupo 2'
  },
  {
    src: 'src/assets/grupo_3.jpg',
    alt: 'Grupo 3'
  },
  {
    src: 'src/assets/grupo_4.jpg',
    alt: 'Grupo 4'
  },
  {
    src: 'src/assets/grupo_5.jpg',
    alt: 'Grupo 5'
  },
  {
    src: 'src/assets/grupo_6.jpg',
    alt: 'Grupo 6'
  },
  {
    src: 'src/assets/grupo_7.jpg',
    alt: 'Grupo 7'
  }
]

const wordCloud = [
  { text: 'Solidariedade', value: 100 },
  { text: 'Comunidade', value: 80 },
  { text: 'Esperança', value: 60 },
  { text: 'Amor', value: 120 },
  { text: 'Doação', value: 90 },
  { text: 'Apoio', value: 70 }
]

const sectionIds = ['hero', 'images', 'qrcode', 'tables', 'wordcloud']
const activeSection = ref(0)

let observers: IntersectionObserver[] = []

onMounted(() => {
  sectionIds.forEach((id, idx) => {
    const el = document.getElementById(id)
    if (el) {
      const observer = new window.IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              activeSection.value = idx
            }
          })
        },
        { threshold: 0.5 }
      )
      observer.observe(el)
      observers.push(observer)
    }
  })
})

onBeforeUnmount(() => {
  observers.forEach((observer) => observer.disconnect())
  observers = []
})

function scrollToSection(idx: number) {
  const el = document.getElementById(sectionIds[idx])
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<template>
  <Background />
  <main class="overflow-y-auto snap-y snap-mandatory no-scrollbar">
    <div class="relative w-full h-screen">
      <section id="hero" class="snap-center">
        <Hero @donate="scrollToSection(1)" @doctors="scrollToSection(2)" @donators="scrollToSection(3)" />
      </section>
      <section id="images" class="snap-center">
        <div class="container section-component rows-component gap-0">
          <Images :pictures="allGroup" />
          <Images :pictures="smallGroups" />
        </div>
      </section>
      <section id="qrcode" class="snap-center">
        <QRCode />
      </section>
      <section id="tables" class="snap-center">
        <div class="container section-component columns-component gap-8">
          <DonorTable title="🏆 Maiores Doadores" :data="topDonors" />
          <DonorTable title="✨ Últimos Doadores" :data="recentDonations" />
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
          :aria-label="`Ir para seção ${id}`"
          class="size-2 rounded-full border-2 border-slate-200 transition-all duration-200"
          :class="activeSection === idx ? 'bg-slate-100 border-slate-800 scale-125 shadow-lg' : 'bg-slate-600'"></button>
      </div>
      <footer class="relative w-full text-center text-sm text-slate-500 mb-8 md:mt-0 md:mb-0 md:bottom-16">
        <p> Agradecimentos à Comissão de Formatura.</p>
        Criado por
        <a href="https://github.com/Yannngn" target="_blank" rel="noopener"
          class="underline hover:text-blue-600">@Yannngn</a>
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
  justify-content: center;
  align-items: center;
  /* background: radial-gradient(circle at center, rgba(48, 65, 88, 1) 25%, rgba(15, 23, 43,0.2) 100%); */
  background: radial-gradient(circle at center, rgba(15, 23, 43, 1) 25%, rgba(15, 23, 43, 0.2) 100%);
  border: 2rem;
  border-radius: 20px;
  transition: box-shadow 0.2s, border-color 0.2s;
}

.columns-component {
  display: flex;
  flex-direction: column;
  gap: 8rem;
}

.rows-component {
  min-width: 100%;
  display: flex;
}

@media (min-width: 768px) {
  .section-component {
    border: 4rem;
    border-radius: 40px;
  }

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