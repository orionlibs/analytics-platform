import { expect, test as setup } from '@e2e/util/test';
import { EDITOR_STORAGE_STATE } from '@root/playwright.config';

setup('login as editor user', async ({ loginPage, page }) => {
  await loginPage.login('e2eEditor', 'letmein');
  await expect(page.getByText('Welcome to Grafana')).toBeVisible();

  await page.context().storageState({ path: EDITOR_STORAGE_STATE });
});
