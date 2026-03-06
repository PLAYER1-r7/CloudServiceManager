import type { CloudService } from '../types/cloud'

interface ServiceTableProps {
  services: CloudService[]
}

function statusClass(status: string): string {
  const normalized = status.trim().toLowerCase()
  if (normalized.includes('running')) {
    return 'running'
  }
  if (normalized.includes('stopped') || normalized.includes('terminated')) {
    return 'stopped'
  }
  return 'unknown'
}

function displayCost(service: CloudService): string {
  const value =
    service.metadata.cost ??
    service.metadata.monthly_cost ??
    service.metadata.estimated_monthly_cost

  if (typeof value === 'number') {
    return `$${value.toFixed(2)}`
  }
  if (typeof value === 'string' && value.length > 0) {
    return value
  }
  return '-'
}

export function ServiceTable({ services }: ServiceTableProps) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Provider</th>
            <th>Service Type</th>
            <th>Name</th>
            <th>Region</th>
            <th>Status</th>
            <th>Cost</th>
            <th>Created At</th>
          </tr>
        </thead>
        <tbody>
          {services.map((service) => (
            <tr key={`${service.provider}:${service.name}:${service.region}`}>
              <td>{service.provider}</td>
              <td>{service.service_type}</td>
              <td>{service.name}</td>
              <td>{service.region}</td>
              <td>
                <span className={`status-pill ${statusClass(service.status)}`}>{service.status}</span>
              </td>
              <td>{displayCost(service)}</td>
              <td>{new Date(service.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
