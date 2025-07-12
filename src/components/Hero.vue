<script setup lang="ts">
defineEmits(['donate', 'doctors', 'donators', 'cloud']);
</script>

<template>
    <div class="container section-component px-auto">
        <img src="../assets/brasao-image.png" alt="Brasão da Turma Medicina 110 UFPB"
            class="size-24 md:size-48 mx-auto mb-4 md:mb-8" />
        <h1
            class="text-6xl md:text-8xl text-center p-4 md:p-8 font-fancy font-medium gold-gradient-text text-[var(--color-accent)]">
            Livro de Ouro
        </h1>
        <h2 class="text-xl md:text-2xl font-semibold text-center py-4 text-[var(--color-text)]">
            Turma Medicina 110 UFPB
        </h2>
        <p class="text-base md:text-lg text-center px-8 mx-4 pb-4 text-[var(--color-footer)]">
            Este é o nosso Livro de Ouro digital! Contribua com a nossa formatura e tenha seu nome eternizado em nossa
            página.
        </p>
        <div class="grid grid-cols-2 gap-2 md:flex md:flex-row md:justify-center md:items-center py-4 md:gap-4">
            <button @click="$emit('donate')"
                class="text-xs md:text-xl m-2 md:m-4 p-2 md:p-4 rounded-lg md:rounded-xl shadow-md transition bg-[var(--color-accent)] text-[var(--color-bg)]">
                Faça sua doação
            </button>
            <button @click="$emit('doctors')"
                class="text-xs md:text-xl m-2 md:m-4 p-2 md:p-4 rounded-lg md:rounded-xl shadow-md transition bg-[var(--color-accent)] text-[var(--color-bg)]">
                Ver a Turma
            </button>
            <button @click="$emit('donators')"
                class="text-xs md:text-xl m-2 md:m-4 p-2 md:p-4 rounded-lg md:rounded-xl shadow-md transition bg-[var(--color-accent)] text-[var(--color-bg)]">
                Ver doadores
            </button>
            <button @click="$emit('cloud')"
                class="text-xs md:text-xl m-2 md:m-4 p-2 md:p-4 rounded-lg md:rounded-xl shadow-md transition bg-[var(--color-accent)] text-[var(--color-bg)]">
                Ver nuvem
            </button>
        </div>

    </div>
</template>

<style scoped>
.gold-gradient-text {
    background: radial-gradient(ellipse farthest-corner at right bottom, #FEDB37 0%, #FDB931 8%, #9f7928 30%, #8A6E2F 40%, transparent 80%),
        radial-gradient(ellipse farthest-corner at left top, #FFFFFF 0%, #FFFFAC 8%, #D1B464 25%, #5d4a1f 62.5%, #5d4a1f 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    color: transparent;
}
</style>