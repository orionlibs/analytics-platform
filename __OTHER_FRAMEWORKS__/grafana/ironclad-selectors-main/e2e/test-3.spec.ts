import { test, expect } from "@playwright/test"

test("test", async ({ page }) => {
  await page.goto(
    "http://127.0.0.1:5500/tests/fixtures/duplicateText_fallsbackToNthFromBody.html"
  )
  await page.getByTestId("duplicate").nth(1).click()
  await page.goto(
    "http://127.0.0.1:5500/tests/fixtures/duplicateText_useDataTestID.html"
  )
  await page
    .getByTestId("data-id-first")
    .getByText("Heading 1 Paragraph Button")
    .click()
})
