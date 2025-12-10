/*
 * Copyright The OpenTelemetry Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import { test, expect } from '@playwright/test';

// This test file focuses on the layout structure
test.describe('Layout Tests', () => {
  // Test the two-column layout on desktop
  test('two-column desktop layout', async ({ page }) => {
    // Set viewport to desktop size
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto('/');
    
    // Wait for content to load
    await page.waitForSelector('[data-testid="changelog-entry"]', { timeout: 10000 });
    
    // Check for the SidebarControls component if it exists in the new layout
    const hasSidebar = await page.isVisible('.sidebar-controls, [role="search"], .filters');
    
    if (hasSidebar) {
      // Take a screenshot of the full layout
      await expect(page).toHaveScreenshot('desktop-two-column-layout.png', {
        timeout: 5000,
        maxDiffPixelRatio: 0.05,
        threshold: 0.2,
      });
      
      // Perform a sidebar interaction if possible (like changing a filter)
      // and verify the layout maintains its structure
      if (await page.isVisible('select')) {
        await page.selectOption('select:nth-of-type(1)', 'merged');
        await page.waitForTimeout(500); // Wait for content to update
        
        await expect(page).toHaveScreenshot('desktop-two-column-layout-filtered.png', {
          timeout: 5000,
          maxDiffPixelRatio: 0.05,
          threshold: 0.2,
        });
      }
    } else {
      // If no sidebar is present, just verify the standard layout
      await expect(page).toHaveScreenshot('desktop-layout.png', {
        timeout: 5000,
        maxDiffPixelRatio: 0.05,
        threshold: 0.2,
      });
    }
  });

  // Test responsive layout adaptation on different devices
  test('responsive layout adaptation', async ({ page }) => {
    // Start with mobile view (should be single column)
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    await page.waitForSelector('[data-testid="changelog-entry"]', { timeout: 10000 });
    
    await expect(page).toHaveScreenshot('mobile-layout.png', {
      timeout: 5000,
      maxDiffPixelRatio: 0.05,
      threshold: 0.2,
    });
    
    // Check tablet view
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/');
    await page.waitForSelector('[data-testid="changelog-entry"]', { timeout: 10000 });
    
    await expect(page).toHaveScreenshot('tablet-layout.png', {
      timeout: 5000,
      maxDiffPixelRatio: 0.05,
      threshold: 0.2,
    });
    
    // Check larger desktop view
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto('/');
    await page.waitForSelector('[data-testid="changelog-entry"]', { timeout: 10000 });
    
    await expect(page).toHaveScreenshot('large-desktop-layout.png', {
      timeout: 5000,
      maxDiffPixelRatio: 0.05,
      threshold: 0.2,
    });
  });
});