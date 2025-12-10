import { expect, test as setup } from '@e2e/util/test';
import { ADMIN_STORAGE_STATE } from '@root/playwright.config';

setup('login as admin user', async ({ loginPage, page }) => {
  await loginPage.login('e2eAdmin', 'letmein');
  await expect(page.getByText('Welcome to Grafana')).toBeVisible();

  await page.context().storageState({ path: ADMIN_STORAGE_STATE });
});
