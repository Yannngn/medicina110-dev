import { ViteImageOptimizer } from "vite-plugin-image-optimizer";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig({
  base: "/medicina110-dev/",
  plugins: [
    vue(),
    tailwindcss(),
    ViteImageOptimizer({
      jpg: {
        quality: 80,
        mozjpeg: true,
      },
    }),
  ],
  resolve: {
    alias: [],
  },
});
