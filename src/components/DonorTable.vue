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
  <div
    class="overflow-y-auto flex flex-col items-center justify-top no-scrollbar md:m-4"
  >
    <h2
      class="text-xl md:text-4xl font-bold mb-2 md:m-4 md:p-4 text-[var(--color-accent)]"
    >
      {{ title }}
    </h2>
    <ul
      v-if="data.length > 0"
      class="space-y-auto overflow-y-auto no-scrollbar"
    >
      <li
        v-for="donor in data"
        :key="donor.name"
        class="md:text-lg font-medium md:mb-1 text-[var(--color-text)]"
      >
        <span>{{ donor.name }}</span>
        <span
          v-if="donor.amount"
          class="text-sm ml-2 text-[var(--color-footer)]"
          >{{ formatCurrency(donor.amount) }}</span
        >
      </li>
    </ul>
    <div v-else class="text-sm text-[var(--color-footer)]">
      Carregando doadores...
    </div>
  </div>
</template>

<style scoped></style>
