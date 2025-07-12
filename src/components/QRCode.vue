<script setup lang="ts">
import { ref } from 'vue'

const pixKey = 'seu-pix@exemplo.com' // Altere para sua chave PIX real
const copied = ref(false)

async function copyPixKey() {
  try {
    await navigator.clipboard.writeText(pixKey)
    copied.value = true
    setTimeout(() => (copied.value = false), 2000)
  } catch (e) {
    alert('Não foi possível copiar a chave PIX.')
  }
}
</script>

<template>
    <div class="container section-component">
        <div class="overflow-y-auto flex flex-col items-center justify-top no-scrollbar">
            <div class="size-64 md:size-96 my-4 md:my-8 relative group cursor-pointer border-2 border-transparent rounded-md hover:border-amber-300"
                @click="copyPixKey">
                <img src="../assets/qr-pix.png" alt="QR Code para doação" class="rounded shadow-lg" />
                <div v-if="copied"
                    class="absolute inset-0 flex items-center justify-center backdrop-blur-sm backdrop-brightness-50 text-white text-lg font-semibold transition">
                    PIX copiado!
                </div>
                <div v-else
                    class="absolute bottom-2 left-1/2 -translate-x-1/2 backdrop-blur-sm backdrop-brightness-50 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition">
                    Clique para copiar a chave PIX
                </div>
            </div>
            <div class="columns-component align-top gap-y-2 h-fit">
                <div class="text-center">
                    <h2 class="text-xl md:text-2xl font-bold">Dados Bancários</h2>
                    <p class="">Banco: <span class="font-bold">000</span></p>
                    <p class="">Agência: <span class="font-bold">0000-0</span></p>
                    <p class="">Conta: <span class="font-bold">00000-0</span></p>
                    <p class="">PIX: <span class="font-bold">{{ pixKey }}</span></p>
                </div>
                <div class="text-center">
                    <h2 class="text-xl md:text-2xl font-bold">Contato</h2>
                    <p class="">WhatsApp: <span class="font-bold">(00) 00000-0000</span></p>
                    <p class="">Email: <span class="font-bold">contato@exemplo.com</span></p>
                </div>
            </div>
            <div class="text-center m-4 gap-y-2">
                <button href="https://forms.gle/seu-form-link" target="_blank" rel="noopener"
                    class="p-4 rounded-lg shadow-md transition bg-slate-750">
                    Preencher Google Forms
                </button>
                <p class="text-sm md:text-base">
                    Ao fazer uma doação, preencha o formulário para que possamos registrar sua contribuição.
                </p>
                <p class="text-sm md:text-base">
                    Se preferir, você pode copiar o PIX copia e cola clicando no QR Code acima ou copiando a chave PIX
                </p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.columns-component {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

@media (min-width: 768px) {
    .columns-component {
        flex-direction: row;
        justify-content: center;
        gap: 4rem;
    }
}
</style>