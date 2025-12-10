import { defineConfig } from "tsup";

export default defineConfig({
  entry: ['src/**/*.ts'],
  clean: true,
  format: ["cjs", "esm"],
  dts: true,
});
