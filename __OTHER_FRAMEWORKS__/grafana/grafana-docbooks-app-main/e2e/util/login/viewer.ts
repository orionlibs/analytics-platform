import { expect, test as setup } from '@e2e/util/test';
import { VIEWER_STORAGE_STATE } from '@root/playwright.config';

setup('login as viewer user', async ({ loginPage, page }) => {
  await loginPage.login('e2eViewer', 'letmein');
  await expect(page.getByText('Welcome to Grafana')).toBeVisible();

  await page.context().storageState({ path: VIEWER_STORAGE_STATE });
});
