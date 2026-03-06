import { HttpResponse, http } from 'msw'

const sampleServices = [
  {
    provider: 'aws',
    service_type: 'EC2',
    name: 'i-01',
    region: 'us-east-1',
    status: 'running',
    created_at: '2026-03-06T10:00:00Z',
    metadata: { instance_type: 't3.micro', estimated_monthly_cost: 10.2 },
  },
  {
    provider: 'gcp',
    service_type: 'Compute Engine',
    name: 'gce-01',
    region: 'us-central1-a',
    status: 'TERMINATED',
    created_at: '2026-03-06T11:00:00Z',
    metadata: { machine_type: 'e2-small', estimated_monthly_cost: 7.3 },
  },
]

export const handlers = [
  http.get('http://localhost:8000/services', ({ request }) => {
    const url = new URL(request.url)
    const limit = Number(url.searchParams.get('limit') ?? '20')
    const offset = Number(url.searchParams.get('offset') ?? '0')
    const pageItems = sampleServices.slice(offset, offset + limit)

    return HttpResponse.json({
      items: pageItems,
      total: sampleServices.length,
      limit,
      offset,
      has_more: offset + limit < sampleServices.length,
    })
  }),
]
