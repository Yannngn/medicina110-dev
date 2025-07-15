<script setup lang="ts">

defineEmits(["donate", "doctors", "donators", "cloud"]);

</script>

<template>
  <section id="hero" class="snap-center">
    <div class="container section-component gap-4 md:gap-8">
      <img src="../assets/brasao-image.png" alt="Brasão da Turma Medicina 110 UFPB" class="resizeble-image" />
      <h1 class="px-8 section-h1 font-fancy font-medium gold-gradient-text text-[var(--color-accent)]">
        Livro de Ouro
      </h1>
      <h2 class="px-8 section-h2 font-semibold text-[var(--color-text)]">
        Turma Medicina 110 UFPB
      </h2>
      <p class="px-8 md:px-16 section-p text-[var(--color-footer)]">
        Este é o nosso Livro de Ouro digital! Contribua com a nossa formatura e
        tenha seu nome eternizado em nossa página.
      </p>
    </div>
  </section>
</template>

<style scoped>
.resizeble-image {
  width: max(8rem, 16vh);
  aspect-ratio: 1 / 1;
}

.gold-gradient-text {
  background:
    radial-gradient(ellipse farthest-corner at right bottom,
      #fedb37 0%,
      #fdb931 8%,
      #9f7928 30%,
      #8a6e2f 40%,
      transparent 80%),
    radial-gradient(ellipse farthest-corner at left top,
      #ffffff 0%,
      #ffffac 8%,
      #d1b464 25%,
      #5d4a1f 62.5%,
      #5d4a1f 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}
</style>
