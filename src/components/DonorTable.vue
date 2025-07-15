<script setup lang="ts">
import type { Donor } from "../services/data-service";

defineProps<{
  title: string;
  data: Donor[];
}>();

function formatCurrency(amount: number) {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(amount);
}
</script>

<template>
  <div class="md:justify-top my-8">
    <h2 class="mb-2 section-h2 font-semibold text-[var(--color-accent)]">
      {{ title }}
    </h2>
    <ul v-if="data.length > 0" class="max-h-40% space-y-auto overflow-y-auto no-scrollbar">
      <li v-for="donor in data" :key="donor.name" class="section-p md:mb-1 text-[var(--color-text)]">
        <span>{{ donor.name }}</span>
        <span v-if="donor.amount" class="section-p md:mb-1 ml-2 text-[var(--color-footer)]">{{
          formatCurrency(donor.amount)
          }}</span>
      </li>
    </ul>
    <div v-else class="section-p text-[var(--color-footer)]">
      Carregando doadores...
    </div>
  </div>
</template>

<style scoped>

</style>
