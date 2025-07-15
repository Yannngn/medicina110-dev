<script setup lang="ts">
import DonorTable from './DonorTable.vue'

interface Donor {
  name: string
  amount?: number
}

defineProps<{
  topDonors: Donor[]
  latestDonations: Donor[]
}>()
</script>

<template>
  <section id="tables" class="snap-center">
    <div class="container section-component columns-component">
      <DonorTable title="🏆 Maiores Doadores" :data="topDonors" />
      <DonorTable title="✨ Últimos Doadores" :data="latestDonations" />
    </div>
  </section>
</template>

<style scoped>
  .columns-component {
    justify-content: center;
  }

@media (max-height: 432px) {
  .section-component {
    flex-direction: column;
    align-items: center;
    gap: 0;
  }

  .columns-component {
    flex-direction: row;
    justify-content: center;
    gap: 2rem;
  }
}

@media (min-width: 768px) and (min-height: 433px) {
  .section-component {
    justify-content: center;
    gap: 4rem;
  }

  .columns-component {
    justify-content: center;
    gap: 4rem;
  }
}
</style>