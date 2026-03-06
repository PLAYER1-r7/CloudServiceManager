import type {
  CloudService,
  ServiceQuery,
  ServicesResponse,
  SortDirection,
  SortField,
} from '../types/cloud'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'
const API_KEY = import.meta.env.VITE_API_KEY

const BACKEND_SORT_FIELDS = new Set<SortField>([
  'name',
  'provider',
  'status',
  'created_at',
  'region',
  'service_type',
])

function buildServiceParams(query: ServiceQuery): URLSearchParams {
  const params = new URLSearchParams()

  if (query.provider && query.provider !== 'all') {
    params.set('provider', query.provider)
  }
  if (query.region) {
    params.set('region', query.region)
  }
  if (query.status) {
    params.set('status', query.status)
  }
  if (query.serviceType) {
    params.set('service_type', query.serviceType)
  }

  const sortField = query.sortBy ?? 'name'
  if (BACKEND_SORT_FIELDS.has(sortField)) {
    params.set('sort_by', sortField)
  }
  params.set('sort_order', query.sortOrder ?? 'asc')
  params.set('limit', String(query.limit ?? 20))
  params.set('offset', String(query.offset ?? 0))

  return params
}

function buildRequestInit(signal?: AbortSignal): RequestInit {
  const headers: Record<string, string> = {}
  if (API_KEY) {
    headers['X-API-Key'] = API_KEY
  }

  return {
    signal,
    headers,
  }
}

function parseCost(service: CloudService): number {
  const costKeys = ['cost', 'monthly_cost', 'estimated_monthly_cost']

  for (const key of costKeys) {
    const value = service.metadata[key]
    if (typeof value === 'number') {
      return value
    }
    if (typeof value === 'string') {
      const parsed = Number(value)
      if (!Number.isNaN(parsed)) {
        return parsed
      }
    }
  }

  return Number.POSITIVE_INFINITY
}

function sortByCost(items: CloudService[], direction: SortDirection): CloudService[] {
  const clone = [...items]
  clone.sort((a, b) => {
    const diff = parseCost(a) - parseCost(b)
    return direction === 'desc' ? -diff : diff
  })
  return clone
}

export async function fetchServices(
  query: ServiceQuery,
  signal?: AbortSignal,
): Promise<ServicesResponse> {
  const params = buildServiceParams(query)
  const response = await fetch(`${API_BASE_URL}/services?${params.toString()}`, buildRequestInit(signal))

  if (!response.ok) {
    const message = `API request failed: ${response.status}`
    throw new Error(message)
  }

  const data = (await response.json()) as ServicesResponse
  if (query.sortBy === 'cost') {
    return {
      ...data,
      items: sortByCost(data.items, query.sortOrder ?? 'asc'),
    }
  }

  return data
}

export async function fetchAllServices(
  query: Omit<ServiceQuery, 'limit' | 'offset'>,
  signal?: AbortSignal,
): Promise<CloudService[]> {
  const pageSize = 500
  let offset = 0
  const allItems: CloudService[] = []

  while (true) {
    const page = await fetchServices(
      {
        ...query,
        limit: pageSize,
        offset,
      },
      signal,
    )

    allItems.push(...page.items)
    if (!page.has_more) {
      break
    }

    offset += page.limit
  }

  return allItems
}
