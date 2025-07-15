import { ViteImageOptimizer } from "vite-plugin-image-optimizer";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // Determine base path based on mode
  const getBasePath = () => {
    if (process.env.VITE_BASE_PATH) {
      return process.env.VITE_BASE_PATH;
    }
    
    switch (mode) {
      case 'development':
        return '/medicina110-dev/';
      case 'production':
        return '/';
      default:
        return '/medicina110-dev/';
    }
  };

  return {
    base: getBasePath(),
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
  };
});
