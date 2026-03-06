export type Provider = 'aws' | 'gcp' | 'azure'

export interface CloudService {
  provider: Provider
  service_type: string
  name: string
  region: string
  status: string
  created_at: string
  metadata: Record<string, unknown>
}

export interface ServicesResponse {
  items: CloudService[]
  total: number
  limit: number
  offset: number
  has_more: boolean
}

export type SortDirection = 'asc' | 'desc'
export type SortField =
  | 'name'
  | 'provider'
  | 'status'
  | 'created_at'
  | 'region'
  | 'service_type'
  | 'cost'

export interface ServiceQuery {
  provider?: 'all' | Provider
  region?: string
  status?: string
  serviceType?: string
  sortBy?: SortField
  sortOrder?: SortDirection
  limit?: number
  offset?: number
}

export interface MetricBucket {
  key: string
  value: number
}

export interface MonitoringSnapshot {
  totalServices: number
  runningServices: number
  stoppedServices: number
  regionDistribution: MetricBucket[]
  providerDistribution: MetricBucket[]
  generatedAt: string
}
