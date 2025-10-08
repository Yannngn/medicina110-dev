<script setup lang="ts">
import { ref } from "vue";

const pixCopy = "https://nubank.com.br/cobrar/a4s5t/689a7e48-3ccc-481d-9f8c-bb9309162c6e";
const pixKey = "f2db8c97-953b-4bfd-a1de-18529a763fec";
const emailKey = "medicina110ufpb@gmail.com";
const copied = ref(false);
const emailCopied = ref(false);
const pixKeyCopied = ref(false);

async function copyPixKey() {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(pixCopy);
    } else {
      // Fallback para HTTP/browsers mais antigos
      const textArea = document.createElement('textarea');
      textArea.value = pixCopy;
      textArea.style.position = 'fixed';
      textArea.style.left = '-999999px';
      textArea.style.top = '-999999px';
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
    }
    copied.value = true;
    setTimeout(() => (copied.value = false), 2000);
  } catch (e) {
    alert("Não foi possível copiar a chave PIX.");
    console.error("Erro ao copiar a chave PIX:", e);
  }
}

async function copyEmail() {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(emailKey);
    } else {
      // Fallback para HTTP/browsers mais antigos
      const textArea = document.createElement('textarea');
      textArea.value = emailKey;
      textArea.style.position = 'fixed';
      textArea.style.left = '-999999px';
      textArea.style.top = '-999999px';
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
    }
    emailCopied.value = true;
    setTimeout(() => (emailCopied.value = false), 2000);
  } catch (e) {
    alert("Não foi possível copiar o email.");
    console.error("Erro ao copiar o email:", e);
  }
}

async function copyPixKeyOnly() {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(pixKey);
    } else {
      // Fallback para HTTP/browsers mais antigos
      const textArea = document.createElement('textarea');
      textArea.value = pixKey;
      textArea.style.position = 'fixed';
      textArea.style.left = '-999999px';
      textArea.style.top = '-999999px';
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
    }
    pixKeyCopied.value = true;
    setTimeout(() => (pixKeyCopied.value = false), 2000);
  } catch (e) {
    alert("Não foi possível copiar a chave PIX.");
    console.error("Erro ao copiar a chave PIX:", e);
  }
}
</script>

<template>
  <section id="qrcode" class="snap-center">
    <div class="container section-component">
      <span class="hidden-block"></span>
      <div
        class="resizeble-image relative group cursor-pointer border-2 border-transparent rounded-lg hover:border-[var(--color-accent-soft)]"
        @click="copyPixKey">
        <img src="../assets/8bd815e0-8773-4e88-a7b4-e320739dd507.jpg" alt="QR Code para doação"
          class="rounded shadow-lg" />
        <div v-if="copied"
          class="absolute inset-0 flex items-center justify-center backdrop-blur-sm backdrop-brightness-50 text-white text-lg font-semibold transition">
          PIX copiado!
        </div>
        <div v-else
          class="absolute bottom-2 left-1/2 -translate-x-1/2 backdrop-blur-sm backdrop-brightness-50 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition">
          Clique para copiar a chave PIX
        </div>
      </div>
      <div class="columns-component pt-2 gap-y-2 h-fit">
        <div class="text-center">
          <h2 class="section-h2 font-bold text-[var(--color-accent)] md:mb-2">
            Dados Bancários
          </h2>
          <p class="section-p text-[var(--color-text)]">
            PIX: <span class="font-semibold">Nubank</span>
          </p>
          <p class="section-p text-[var(--color-text)]">
            Chave: <span
              class="font-semibold cursor-pointer hover:text-[var(--color-accent)] transition-colors relative"
              @click="copyPixKeyOnly" title="Clique para copiar a chave PIX">
              {{ pixKey }}
              <span v-if="pixKeyCopied"
                class="absolute -top-8 left-1/2 -translate-x-1/2 bg-[var(--color-accent)] text-white text-xs px-2 py-1 rounded whitespace-nowrap">
                Chave PIX copiada!
              </span>
            </span>
          </p>
        </div>
        <div class="text-center">
          <h2 class="section-h2 font-bold text-[var(--color-accent)] md:mb-2">
            Contato
          </h2>
          <p class="section-p text-[var(--color-text)]">
            Nome: <span class="font-semibold">Matheus Felipe de Macedo Freire</span>
          </p>
          <p class="section-p text-[var(--color-text)]">
            WhatsApp: <a href="https://wa.me/+5581993300128" target="_blank" rel="noopener"
              class="font-semibold cursor-pointer hover:text-[var(--color-accent)] transition-colors"
              title="Clique para abrir no WhatsApp">
              (81) 9 9330-0128
            </a>
          </p>
          <p class="section-p text-[var(--color-text)]">
            Email:
            <span class="font-semibold cursor-pointer hover:text-[var(--color-accent)] transition-colors relative"
              @click="copyEmail" title="Clique para copiar o email">
              {{ emailKey }}
              <span v-if="emailCopied"
                class="absolute -top-8 left-1/2 -translate-x-1/2 bg-[var(--color-accent)] text-white text-xs px-2 py-1 rounded whitespace-nowrap">
                Email copiado!
              </span>
            </span>
          </p>
        </div>
      </div>
      <div class="text-center mb-8 md:mb-0 ">
        <a href="https://forms.gle/HLQgGe3gsJLUv4hcA" target="_blank" rel="noopener"
          class="btn m-2 md:m-4 p-2 md:p-4 rounded-lg md:rounded-xl inline-block">
          Preencher Google Forms
        </a>
      </div>
      <div class="hidden-block">
        <p class="section-p text-[var(--color-footer)]">
          Ao fazer uma doação, sinalize para que um aluno preencha o formulário para que possamos registrar
          sua contribuição.
        </p>
        <p class="section-p text-[var(--color-footer)]">
          Se preferir, você pode copiar o PIX copia e cola clicando no QR Code
          acima ou copiando a chave PIX
        </p>
      </div>
    </div>
  </section>
</template>


<style scoped>
.hidden-block {
  display: none;
}

.resizeble-image {
  width: max(8rem, 24vh);
  aspect-ratio: 1 / 1;
}

.section-component {
  gap: 2rem;
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
  span.hidden-block {
    display: none;
  }

  .hidden-block {
    display: block;
  }

  .section-component {
    justify-content: center;
    gap: 4rem;
  }

  .columns-component {
    flex-direction: row;
    justify-content: center;
    gap: 4rem;
  }
}
</style>
