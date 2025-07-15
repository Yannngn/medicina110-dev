import { defineConfig, loadEnv } from "vite";
import { ViteImageOptimizer } from "vite-plugin-image-optimizer";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  return {
    base: env.VITE_BASE_PATH || "/",
    plugins: [
      vue(),
      tailwindcss(),
      ViteImageOptimizer({
        jpg: {
          quality: 95,
          mozjpeg: true,
        },
      }),
    ],
    resolve: {
      alias: [],
    },
  };
});
