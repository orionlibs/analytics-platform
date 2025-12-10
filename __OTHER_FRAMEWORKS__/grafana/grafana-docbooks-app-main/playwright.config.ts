import { defineConfig, devices } from '@playwright/test';
import path from 'path';

export const VIEWER_STORAGE_STATE = path.join(__dirname, 'e2e/.auth/viewer.json');
export const EDITOR_STORAGE_STATE = path.join(__dirname, 'e2e/.auth/editor.json');
export const ADMIN_STORAGE_STATE = path.join(__dirname, 'e2e/.auth/admin.json');

export const PLUGIN_ACCESS_STORAGE_STATE = path.join(__dirname, 'e2e/.auth/pluginAccess.json');
export const baseURL = process.env.CI ? 'http://grafana:3000' : 'http://127.0.0.1:3000';
/**
 * Read environment variables from file.
 * https://github.com/motdotla/dotenv
 */
// require('dotenv').config();

/**
 * See https://playwright.dev/docs/test-configuration.
 */
export default defineConfig({
  expect: {
    toHaveScreenshot: { maxDiffPixelRatio: 0.01 },
  },
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  /* Run tests in files in parallel */
  fullyParallel: true,
  /* Configure projects for major browsers */
  projects: [
    {
      name: 'login-viewer',
      testMatch: 'util/login/viewer.ts',
    },
    {
      name: 'login-editor',
      testMatch: 'util/login/editor.ts',
    },
    {
      name: 'login-admin',
      testMatch: 'util/login/admin.ts',
    },
    {
      dependencies: ['login-viewer'],
      name: 'read-only-viewer-chromium',
      testMatch: '__tests__/ReadOnlyUser/**/*.spec.ts',
      use: { ...devices['Desktop Chrome'], storageState: VIEWER_STORAGE_STATE },
    },
    {
      dependencies: ['login-editor'],
      name: 'read-only-editor-chromium',
      testMatch: '__tests__/ReadOnlyUser/**/*.spec.ts',
      use: { ...devices['Desktop Chrome'], storageState: EDITOR_STORAGE_STATE },
    },
    {
      dependencies: ['login-admin'],
      name: 'edit-admin-chromium',
      testMatch: '__tests__/AdminUser/**/*.spec.ts',
      use: { ...devices['Desktop Chrome'], storageState: ADMIN_STORAGE_STATE },
    },
    {
      name: 'login-per-test',
      testMatch: '__tests__/LoginPerTest/**/*.spec.ts',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: 'html',
  /* Retry on CI only */
  retries: process.env.CI ? 2 : 0,
  testDir: './e2e',
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL to use in actions like `await page.goto('/')`. */
    baseURL,

    screenshot: 'only-on-failure',
    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: 'on-first-retry',
  },

  /* Opt out of parallel tests on CI. */
  workers: process.env.CI ? 1 : undefined,
});
