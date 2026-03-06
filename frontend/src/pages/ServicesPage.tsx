import { useEffect, useMemo, useState } from 'react'
import { fetchServices } from '../api/client'
import { ServiceTable } from '../components/ServiceTable'
import type { ServiceQuery, ServicesResponse, SortDirection, SortField } from '../types/cloud'

const DEFAULT_LIMIT = 20

const initialData: ServicesResponse = {
  items: [],
  total: 0,
  limit: DEFAULT_LIMIT,
  offset: 0,
  has_more: false,
}

export function ServicesPage() {
  const [provider, setProvider] = useState<ServiceQuery['provider']>('all')
  const [status, setStatus] = useState('')
  const [serviceType, setServiceType] = useState('')
  const [region, setRegion] = useState('')
  const [sortBy, setSortBy] = useState<SortField>('name')
  const [sortOrder, setSortOrder] = useState<SortDirection>('asc')
  const [offset, setOffset] = useState(0)

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [data, setData] = useState<ServicesResponse>(initialData)

  const query = useMemo<ServiceQuery>(
    () => ({
      provider,
      status: status.trim() || undefined,
      serviceType: serviceType.trim() || undefined,
      region: region.trim() || undefined,
      sortBy,
      sortOrder,
      limit: DEFAULT_LIMIT,
      offset,
    }),
    [offset, provider, region, serviceType, sortBy, sortOrder, status],
  )

  useEffect(() => {
    const controller = new AbortController()

    async function load() {
      setLoading(true)
      setError(null)
      try {
        const response = await fetchServices(query, controller.signal)
        setData(response)
      } catch (err) {
        if (err instanceof Error && err.name === 'AbortError') {
          return
        }
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    void load()
    return () => controller.abort()
  }, [query])

  function onApplyFilters() {
    setOffset(0)
  }

  const pageNumber = Math.floor(data.offset / data.limit) + 1

  return (
    <section className="panel">
      <h2>Services</h2>
      <p className="muted">Browse unified resources from `/services` API with pagination, filters, and sorting.</p>

      <div className="form-row">
        <label>
          Provider
          <select value={provider} onChange={(e) => setProvider(e.target.value as ServiceQuery['provider'])}>
            <option value="all">all</option>
            <option value="aws">aws</option>
            <option value="gcp">gcp</option>
            <option value="azure">azure</option>
          </select>
        </label>

        <label>
          Status
          <input
            value={status}
            onChange={(e) => setStatus(e.target.value)}
            placeholder="running / stopped"
          />
        </label>

        <label>
          Service Type
          <input
            value={serviceType}
            onChange={(e) => setServiceType(e.target.value)}
            placeholder="EC2 / Compute Engine"
          />
        </label>
      </div>

      <div className="form-row">
        <label>
          Region
          <input value={region} onChange={(e) => setRegion(e.target.value)} placeholder="us-east-1" />
        </label>

        <label>
          Sort By
          <select value={sortBy} onChange={(e) => setSortBy(e.target.value as SortField)}>
            <option value="name">name</option>
            <option value="status">status</option>
            <option value="region">region</option>
            <option value="service_type">service_type</option>
            <option value="created_at">created_at</option>
            <option value="cost">cost</option>
          </select>
        </label>

        <label>
          Sort Order
          <select value={sortOrder} onChange={(e) => setSortOrder(e.target.value as SortDirection)}>
            <option value="asc">asc</option>
            <option value="desc">desc</option>
          </select>
        </label>
      </div>

      <div className="controls">
        <button className="cta" onClick={onApplyFilters}>
          Apply
        </button>
        <button
          onClick={() => {
            setProvider('all')
            setStatus('')
            setServiceType('')
            setRegion('')
            setSortBy('name')
            setSortOrder('asc')
            setOffset(0)
          }}
        >
          Reset
        </button>
      </div>

      {loading ? <div className="state">Loading services...</div> : null}
      {error ? <div className="state error">{error}</div> : null}

      {!loading && !error && data.items.length === 0 ? (
        <div className="state">No services found for the selected filters.</div>
      ) : null}

      {!loading && !error && data.items.length > 0 ? <ServiceTable services={data.items} /> : null}

      <div className="pagination">
        <span className="muted">
          Page {pageNumber} | total: {data.total}
        </span>
        <div className="controls">
          <button onClick={() => setOffset((prev) => Math.max(0, prev - DEFAULT_LIMIT))} disabled={offset === 0}>
            Previous
          </button>
          <button onClick={() => setOffset((prev) => prev + DEFAULT_LIMIT)} disabled={!data.has_more}>
            Next
          </button>
        </div>
      </div>
    </section>
  )
}
