import { expect, test as base } from '@playwright/test';

import { LoginPage } from '@e2e/fixtures/login-page';

type TestFixtures = {
  loginPage: LoginPage;
};

const testFactory = () =>
  base.extend<TestFixtures>({
    loginPage: async ({ page }, use) => {
      await page.goto('/logout');
      const loginPage = new LoginPage(page);
      await loginPage.goto();
      await use(loginPage);
    },
  });

const test = testFactory();

export { expect, test, testFactory };
