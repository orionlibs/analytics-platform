import type { Locator, Page } from '@playwright/test';

export class LoginPage {
  private readonly username: Locator;
  private readonly password: Locator;
  private readonly loginButton: Locator;
  constructor(readonly page: Page) {
    this.username = this.page.getByPlaceholder('email or username');
    this.password = this.page.getByPlaceholder('password');
    this.loginButton = this.page.getByTestId('data-testid Login button');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(username: string, password: string) {
    await this.username.fill(username);
    await this.password.fill(password);
    await this.loginButton.click();
    await this.page.waitForURL('/');
    await this.page.waitForLoadState('networkidle');
  }
}
