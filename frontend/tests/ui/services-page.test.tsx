import { HttpResponse, http } from 'msw'
import { render, screen, waitFor } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { ServicesPage } from '../../src/pages/ServicesPage'
import { server } from '../../src/test/msw/server'

describe('ServicesPage', () => {
  it('renders services from API', async () => {
    render(<ServicesPage />)

    expect(screen.getByText('Loading services...')).toBeInTheDocument()

    await waitFor(() => {
      expect(screen.getByText('i-01')).toBeInTheDocument()
      expect(screen.getByText('gce-01')).toBeInTheDocument()
    })
  })

  it('shows error state on API failure', async () => {
    server.use(
      http.get('http://localhost:8000/services', () => {
        return new HttpResponse(null, { status: 500 })
      }),
    )

    render(<ServicesPage />)

    await waitFor(() => {
      expect(screen.getByText(/API request failed: 500/)).toBeInTheDocument()
    })
  })
})
