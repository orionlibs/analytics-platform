import { expect, test as setup } from '@e2e/util/test';
import { PLUGIN_ACCESS_STORAGE_STATE } from '@root/playwright.config';

setup('login as e2ePluginAccess user', async ({ loginPage, page }) => {
  await loginPage.login('e2ePluginAccess', 'letmein');
  await expect(page.getByText('Welcome to Grafana')).toBeVisible();

  await page.context().storageState({ path: PLUGIN_ACCESS_STORAGE_STATE });
});
