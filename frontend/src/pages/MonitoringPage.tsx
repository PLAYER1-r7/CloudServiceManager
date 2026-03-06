import { useEffect, useMemo, useState } from 'react'
import { fetchAllServices } from '../api/client'
import type { CloudService, MetricBucket, MonitoringSnapshot } from '../types/cloud'

const REFRESH_INTERVAL_MS = 30000

function normalizeStatus(status: string): string {
  const normalized = status.trim().toLowerCase()
  if (normalized.includes('running')) {
    return 'running'
  }
  if (
    normalized.includes('stopped') ||
    normalized.includes('terminated') ||
    normalized.includes('stopping')
  ) {
    return 'stopped'
  }
  return 'other'
}

function makeDistribution(items: CloudService[], selector: (item: CloudService) => string): MetricBucket[] {
  const counts = new Map<string, number>()

  for (const item of items) {
    const key = selector(item)
    counts.set(key, (counts.get(key) ?? 0) + 1)
  }

  return [...counts.entries()]
    .map(([key, value]) => ({ key, value }))
    .sort((a, b) => b.value - a.value)
}

function buildSnapshot(items: CloudService[]): MonitoringSnapshot {
  const runningServices = items.filter((item) => normalizeStatus(item.status) === 'running').length
  const stoppedServices = items.filter((item) => normalizeStatus(item.status) === 'stopped').length

  return {
    totalServices: items.length,
    runningServices,
    stoppedServices,
    regionDistribution: makeDistribution(items, (item) => item.region).slice(0, 6),
    providerDistribution: makeDistribution(items, (item) => item.provider),
    generatedAt: new Date().toISOString(),
  }
}

function DistributionList({ title, buckets }: { title: string; buckets: MetricBucket[] }) {
  if (buckets.length === 0) {
    return <div className="state">No data available.</div>
  }

  const max = Math.max(...buckets.map((bucket) => bucket.value), 1)

  return (
    <article className="panel">
      <h3>{title}</h3>
      <div className="distribution-list">
        {buckets.map((bucket) => (
          <div key={bucket.key} className="distribution-row">
            <div className="distribution-label">{bucket.key}</div>
            <div className="distribution-bar-track">
              <div
                className="distribution-bar"
                style={{ width: `${Math.max(8, (bucket.value / max) * 100)}%` }}
              />
            </div>
            <div className="distribution-value">{bucket.value}</div>
          </div>
        ))}
      </div>
    </article>
  )
}

export function MonitoringPage() {
  const [autoRefresh, setAutoRefresh] = useState(true)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [snapshot, setSnapshot] = useState<MonitoringSnapshot | null>(null)

  async function load(signal?: AbortSignal) {
    setLoading(true)
    setError(null)

    try {
      const services = await fetchAllServices({ sortBy: 'name', sortOrder: 'asc' }, signal)
      setSnapshot(buildSnapshot(services))
    } catch (err) {
      if (err instanceof Error && err.name === 'AbortError') {
        return
      }

      setError(err instanceof Error ? err.message : 'Failed to fetch monitoring data')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    const controller = new AbortController()
    void load(controller.signal)
    return () => controller.abort()
  }, [])

  useEffect(() => {
    if (!autoRefresh) {
      return
    }

    const timer = window.setInterval(() => {
      void load()
    }, REFRESH_INTERVAL_MS)

    return () => window.clearInterval(timer)
  }, [autoRefresh])

  const generatedAtLabel = useMemo(() => {
    if (!snapshot) {
      return '-'
    }

    return new Date(snapshot.generatedAt).toLocaleString()
  }, [snapshot])

  return (
    <section className="monitoring-layout">
      <article className="panel">
        <div className="monitoring-head">
          <div>
            <h2>Monitoring Dashboard</h2>
            <p className="muted">
              Metrics are calculated from the existing `/services` endpoint. Update interval: 30 seconds.
            </p>
          </div>
          <div className="controls">
            <button className="cta" onClick={() => void load()} disabled={loading}>
              {loading ? 'Refreshing...' : 'Refresh now'}
            </button>
            <button onClick={() => setAutoRefresh((prev) => !prev)}>
              Auto refresh: {autoRefresh ? 'on' : 'off'}
            </button>
          </div>
        </div>

        {error ? <div className="state error">Monitoring data unavailable: {error}</div> : null}

        {snapshot ? (
          <div className="metrics-grid">
            <article className="metric-card">
              <p>Total Services</p>
              <h3>{snapshot.totalServices}</h3>
            </article>
            <article className="metric-card ok">
              <p>Running</p>
              <h3>{snapshot.runningServices}</h3>
            </article>
            <article className="metric-card danger">
              <p>Stopped / Terminated</p>
              <h3>{snapshot.stoppedServices}</h3>
            </article>
          </div>
        ) : null}

        <p className="muted">Last updated: {generatedAtLabel}</p>
      </article>

      {snapshot ? <DistributionList title="Region Distribution" buckets={snapshot.regionDistribution} /> : null}
      {snapshot ? <DistributionList title="Provider Distribution" buckets={snapshot.providerDistribution} /> : null}

      {!snapshot && !loading && !error ? (
        <div className="state">No metrics to display yet. Click "Refresh now".</div>
      ) : null}
    </section>
  )
}
