import { test, expect } from '@playwright/test';

test.describe('Project Carousel', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display the first slide by default', async ({ page }) => {
    const slides = page.locator('.project-slide');
    await expect(slides.first()).toHaveClass(/is-active/);
    await expect(slides.nth(1)).not.toHaveClass(/is-active/);

    // Initial transform shouldn't be matrix(1,0,0,1,0,0) in coverflow, as it offsets even the first slide to center it.
    // Instead, verify it has *some* transform set.
    const track = page.locator('.project-list');
    const transform = await track.evaluate(el => el.style.transform);
    expect(transform).toContain('translateX');
  });

  test('should navigate to the next slide when clicking the next button', async ({ page }) => {
    const nextBtn = page.locator('.next-btn');
    const slides = page.locator('.project-slide');
    const track = page.locator('.project-list');

    const initialTransform = await track.evaluate(el => el.style.transform);

    await nextBtn.click();

    await expect(slides.first()).not.toHaveClass(/is-active/);
    await expect(slides.nth(1)).toHaveClass(/is-active/);

    // Check transform changed. It's dynamically calculated based on viewport width
    // in coverflow mode, so we just verify it moved from its initial position.
    const newTransform = await track.evaluate(el => el.style.transform);
    expect(newTransform).not.toBe(initialTransform);
    expect(newTransform).toContain('translateX');
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

    // In the new layout, the indicators are: [<, indicator1, indicator2, indicator3, >]
    // The first project indicator (index 0) is at nth(1). The second (index 1) is at nth(2).
    await indicators.nth(2).click();

    await expect(slides.nth(1)).toHaveClass(/is-active/);
    await expect(indicators.nth(2)).toHaveClass(/active/);
    await expect(indicators.nth(2)).toHaveText('O');

    // Check that the first indicator (now at nth(1)) is inactive ('0')
    await expect(indicators.nth(1)).toHaveText('0');
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
