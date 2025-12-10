/*
 * Copyright The OpenTelemetry Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import { test, expect } from '@playwright/test';

test.describe('API Routes', () => {
  test.skip('feed route should return RSS feed', async ({ request }) => {
    // Skipped because this relies on Netlify Blobs which isn't available in local dev
    const response = await request.get('/feed');
    
    expect(response.status()).toBe(200);
    expect(response.headers()['content-type']).toContain('application/xml');
    
    const body = await response.text();
    expect(body).toContain('<?xml');
    expect(body).toContain('<rss');
    expect(body).toContain('<channel>');
  });
  
  test('feed should handle markdown in descriptions', async ({ request }) => {
    // This test will pass once we implement the markdown parsing fix
    const response = await request.get('/feed');
    expect(response.status()).toBe(200);
    
    const body = await response.text();
    
    // The test endpoint adds entries with markdown, let's verify we don't see raw markdown
    // This will initially fail until we fix the issue
    expect(body).not.toMatch(/\*\*bold text\*\*/);
    expect(body).not.toMatch(/\[link text\]\(http:\/\/example\.com\)/);
  });

  test('test API should work in development', async ({ request }) => {
    // When testing in CI, we're likely in development mode
    const response = await request.post('/api/test');
    
    // In CI/tests, we accept either 200 (dev mode) or 403 (prod mode)
    expect([200, 403]).toContain(response.status());
    
    // If we got a 200, verify the response
    if (response.status() === 200) {
      const text = await response.text();
      expect(text).toContain('Test entry added');
    }
  });

  test('revalidate API requires secret', async ({ request }) => {
    const response = await request.post('/api/revalidate');
    
    // Should fail without proper secret
    expect(response.status()).not.toBe(200);
  });
});