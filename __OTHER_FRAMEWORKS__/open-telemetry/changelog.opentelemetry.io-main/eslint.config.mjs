// eslint.config.mjs

import { FlatCompat } from "@eslint/eslintrc";
import pluginHeader from "eslint-plugin-header";

pluginHeader.rules.header.meta.schema = false;

const compat = new FlatCompat({
  // import.meta.dirname is available after Node.js v20.11.0
  baseDirectory: import.meta.dirname,
});

const eslintConfig = [
  ...compat.config({
    extends: ["next", "next/core-web-vitals", "next/typescript"],
    rules: {
      "header/header": "off" // Temporarily disable header check
    }
  }),
];

export default eslintConfig;
