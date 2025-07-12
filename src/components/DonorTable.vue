<script setup lang="ts">

interface DonorRow {
    [key: string]: string
}

defineProps<{
    title: string
    data: DonorRow[]
}>()

</script>

<template>
    <div class="overflow-y-auto flex flex-col items-center justify-top no-scrollbar md:m-4">
        <h2 class="text-xl md:text-4xl font-bold mb-2 md:m-4 md:p-4 text-center">{{ title }}</h2>
        <ul class="space-y-auto overflow-y-auto no-scrollbar">
            <li v-for=" donor in data" :key="donor.name" class="text-center md:text-lg font-medium md:mb-1">
                {{ donor.name }}
            </li>
        </ul>
    </div>
</template>

<style scoped>

</style>