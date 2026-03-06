import { expect, test } from '@playwright/test'

test('navigates to services and renders API-backed table', async ({ page }) => {
  await page.route('**/services**', async (route) => {
    const url = new URL(route.request().url())
    const offset = Number(url.searchParams.get('offset') ?? '0')

    const items = [
      {
        provider: 'aws',
        service_type: 'EC2',
        name: 'i-e2e-01',
        region: 'us-east-1',
        status: 'running',
        created_at: '2026-03-06T10:00:00Z',
        metadata: {},
      },
    ]

    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        items: offset === 0 ? items : [],
        total: 1,
        limit: 20,
        offset,
        has_more: false,
      }),
    })
  })

  await page.goto('/')
  await page.locator('nav[aria-label="Primary"]').getByRole('link', { name: 'Services' }).click()

  await expect(page.getByRole('heading', { name: 'Services' })).toBeVisible()
  await expect(page.getByText('i-e2e-01')).toBeVisible()

  await page.locator('nav[aria-label="Primary"]').getByRole('link', { name: 'Monitoring' }).click()
  await expect(page.getByRole('heading', { name: 'Monitoring Dashboard' })).toBeVisible()
})
