import { resolve } from "path";
import { defineConfig } from "vite";
import { viteStaticCopy } from "vite-plugin-static-copy";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  base: "/repro-backdrop-filter/",
  plugins: [
    react(),
    viteStaticCopy({
      targets: [
        {
          src: resolve(
            __dirname,
            "node_modules/@grafana/ui/dist/public/img/icons/unicons/times.svg"
          ),
          dest: "./public/img/icons/unicons/",
        },
      ],
    }),
  ],
  build: {
    rollupOptions: {
      input: {
        index: resolve(__dirname, "index.html"),
        grafanaUiSimple: resolve(__dirname, "grafana-ui-simple.html"),
        grafanaUiGlobalStyles: resolve(
          __dirname,
          "grafana-ui-global-styles.html"
        ),
        standalone: resolve(__dirname, "standalone.html"),
      },
    },
  },
});
