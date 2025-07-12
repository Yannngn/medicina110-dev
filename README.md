
# Livro de Ouro - Medicina 110 UFPB

[![Vite](https://img.shields.io/badge/Vite-4.x-646CFF?logo=vite)](https://vitejs.dev/)
[![Vue 3](https://img.shields.io/badge/Vue-3.x-42b883?logo=vue.js)](https://vuejs.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.x-38bdf8?logo=tailwindcss)](https://tailwindcss.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178c6?logo=typescript)](https://www.typescriptlang.org/)
[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue?logo=python)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas)](https://pandas.pydata.org/)
[![Google Sheets](https://img.shields.io/badge/Google%20Sheets-API-34A853?logo=google)](https://developers.google.com/sheets/api)


---

## 📖 Sobre o Projeto

Este é o **Livro de Ouro Digital** da Turma de Medicina 110 da UFPB.  
Aqui você pode visualizar os doadores, contribuir para a formatura e eternizar seu nome na história da turma!

O site é moderno, responsivo e seguro, feito para ser fácil de usar por todos.

---

## 👩‍💻 Para Desenvolvedores

### Tecnologias Utilizadas

- **Frontend:** [Vue 3](https://vuejs.org/) + [Vite](https://vitejs.dev/) + [TailwindCSS](https://tailwindcss.com/)
- **Backend/Data Pipeline:** [Python 3.13](https://www.python.org/) + [Pandas](https://pandas.pydata.org/) + [Google Sheets API](https://developers.google.com/sheets/api)

### Estrutura do Projeto

```
medicina110-dev/
├── src/
│   ├── assets/           # Imagens e SVGs
│   ├── components/       # Componentes Vue
│   ├── services/         # Scripts Python e TypeScript
│   ├── style.css         # Estilos globais (Tailwind + CSS Variables)
│   ├── App.vue           # Componente principal
│   └── main.ts           # Bootstrap do Vue
├── public/
│   └── assets/donors.json # Dados estáticos gerados pelo Python
├── README.md
```

### Como Rodar Localmente

1. **Pré-requisitos:**  
   - Node.js 18+  
   - Python 3.13+  
   - Conta Google com acesso à planilha de doações

2. **Instale as dependências do frontend:**
   ```bash
   npm install
   ```

3. **Execute o site em modo desenvolvimento:**
   ```bash
   npm run dev
   ```

4. **Atualize os dados dos doadores (Python):**
   - Configure suas credenciais do Google Sheets.
   - Execute o script:
     ```bash
     python src/services/update_donors.py
     ```
   - O arquivo `donors.json` será gerado em `public/assets/donors.json`.

5. **Build para produção:**
   ```bash
   npm run build
   npm run preview
   ```

---

## 👩‍🎓 Para Colegas e Visitantes

- **Como doar:**  
  Clique no botão "Faça sua doação", copie a chave PIX ou escaneie o QR Code.
- **Como aparecer no Livro de Ouro:**  
  Após doar, preencha o formulário Google Forms para registrar seu nome.
- **Visualize:**  
  - Maiores doadores
  - Últimos doadores
  - Nuvem de palavras dos doadores

O site funciona em qualquer dispositivo (celular, tablet, computador) e tem modo claro/escuro para melhor conforto visual.

---

## 💡 Dúvidas Frequentes

- **Meu nome não apareceu, o que faço?**  
  Aguarde alguns minutos após preencher o formulário. Se não aparecer, entre em contato com a comissão.

- **Posso doar mais de uma vez?**  
  Sim! Seu nome e valor serão atualizados automaticamente.

- **Como funciona a segurança dos dados?**  
  Nenhuma informação sensível é exposta. Os dados vêm diretamente da planilha do Google, processados por um script Python seguro.

---

## 🛠️ Contribuição

Sugestões, correções ou novas ideias são bem-vindas!  
Abra uma issue ou envie um pull request.

---

## 📄 Licença

Projeto livre para uso pela Turma Medicina 110 UFPB.

---

Feito com ❤️ por [@Yannngn](https://github.com/Yannngn) e Comissão de Formatura.
