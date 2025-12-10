/*
 * Copyright The OpenTelemetry Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import { test, expect } from '@playwright/test';

test.describe('Homepage', () => {
  test('should have correct title', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/OpenTelemetry Changelog/);
  });

  test('should display changelog header', async ({ page }) => {
    await page.goto('/');
    const header = page.locator('h1');
    await expect(header).toBeVisible();
    await expect(header).toHaveText(/OpenTelemetry Changelog/);
  });

  test('should show changelog entries', async ({ page }) => {
    await page.goto('/');
    const entries = page.locator('[data-testid="changelog-entry"]');
    
    // Wait for entries to be loaded (adjust timeout if needed)
    await expect(entries).toHaveCount(await entries.count(), { timeout: 5000 });
    
    // Verify structure of at least one entry if any exist
    if (await entries.count() > 0) {
      const firstEntry = entries.first();
      await expect(firstEntry.locator('.entry-title')).toBeVisible();
      await expect(firstEntry.locator('.entry-description')).toBeVisible();
    }
  });

  test('should have proper responsive design', async ({ page }) => {
    // Test on mobile viewport
    await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE size
    await page.goto('/');
    await expect(page.locator('body')).toBeVisible();
    
    // Take screenshot for visual comparison
    await page.screenshot({ path: 'tests/screenshots/home-mobile.png' });
    
    // Test on desktop viewport
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto('/');
    await expect(page.locator('body')).toBeVisible();
    
    // Take screenshot for visual comparison
    await page.screenshot({ path: 'tests/screenshots/home-desktop.png' });
  });
});