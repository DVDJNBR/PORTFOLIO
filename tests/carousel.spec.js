import { test, expect } from '@playwright/test';

test.describe('Project Carousel', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display the first slide by default', async ({ page }) => {
    const slides = page.locator('.project-slide');
    await expect(slides.first()).toHaveClass(/is-active/);
    await expect(slides.nth(1)).not.toHaveClass(/is-active/);

    const track = page.locator('.project-list');
    await expect(track).toHaveCSS('transform', 'matrix(1, 0, 0, 1, 0, 0)');
  });

  test('should navigate to the next slide when clicking the next button', async ({ page }) => {
    const nextBtn = page.locator('.next-btn');
    const slides = page.locator('.project-slide');
    const track = page.locator('.project-list');

    await nextBtn.click();

    await expect(slides.first()).not.toHaveClass(/is-active/);
    await expect(slides.nth(1)).toHaveClass(/is-active/);

    // Check transform. Note: matrix values might depend on viewport but we expect translateX(-100%)
    // translateX(-100%) on a container that is full width of viewport should be -viewportWidth
    // However, it's easier to check if it changed from the initial 0.
    const transform = await track.evaluate(el => el.style.transform);
    expect(transform).toBe('translateX(-100%)');
  });

  test('should navigate to the previous slide when clicking the prev button', async ({ page }) => {
    const nextBtn = page.locator('.next-btn');
    const prevBtn = page.locator('.prev-btn');
    const slides = page.locator('.project-slide');

    // Go to second slide
    await nextBtn.click();
    await expect(slides.nth(1)).toHaveClass(/is-active/);

    // Go back to first slide
    await prevBtn.click();
    await expect(slides.first()).toHaveClass(/is-active/);
    await expect(slides.nth(1)).not.toHaveClass(/is-active/);
  });

  test('should navigate when clicking on indicators', async ({ page }) => {
    const indicators = page.locator('.indicator');
    const slides = page.locator('.project-slide');

    // Click second indicator
    await indicators.nth(1).click();

    await expect(slides.nth(1)).toHaveClass(/is-active/);
    await expect(indicators.nth(1)).toHaveClass(/active/);
    await expect(indicators.nth(1)).toHaveText('O');
    await expect(indicators.first()).toHaveText('0');
  });

  test('should not navigate past the first slide', async ({ page }) => {
    const prevBtn = page.locator('.prev-btn');
    const slides = page.locator('.project-slide');

    await prevBtn.click();
    await expect(slides.first()).toHaveClass(/is-active/);
  });

  test('should not navigate past the last slide', async ({ page }) => {
    const nextBtn = page.locator('.next-btn');
    const slides = page.locator('.project-slide');
    const slideCount = await slides.count();

    // Move to the last slide
    for (let i = 0; i < slideCount - 1; i++) {
      await nextBtn.click();
    }
    await expect(slides.last()).toHaveClass(/is-active/);

    // Try to move further
    await nextBtn.click();
    await expect(slides.last()).toHaveClass(/is-active/);
  });
});
