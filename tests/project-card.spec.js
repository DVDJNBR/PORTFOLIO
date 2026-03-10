import { test, expect } from '@playwright/test';

test.describe('ProjectCard Component', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display the brief badge when briefNumber is provided', async ({ page }) => {
    // The first project has briefNumber: 1
    const firstProject = page.locator('.project-slide').first();
    const briefBadge = firstProject.locator('.brief-badge');

    await expect(briefBadge).toBeVisible();
    await expect(briefBadge).toHaveText('Brief #1');
  });

  test('should not display the brief badge when briefNumber is not provided', async ({ page }) => {
    // The second project does not have briefNumber
    const secondProject = page.locator('.project-slide').nth(1);
    const briefBadge = secondProject.locator('.brief-badge');

    await expect(briefBadge).not.toBeAttached();
  });
});
