import { Link } from 'react-router-dom'

export function HomePage() {
  return (
    <section className="hero">
      <article className="panel">
        <h2>Ops visibility without provider hopping</h2>
        <p>
          Move between AWS, Azure, and GCP services from one surface. Use the Services page to filter,
          sort, and paginate the API response without touching the CLI.
        </p>
        <div className="tag-list">
          <span className="tag">FastAPI backend</span>
          <span className="tag">Unified CloudService model</span>
          <span className="tag">Rate-limited endpoints</span>
        </div>
      </article>

      <article className="panel">
        <h3>Phase 3 scope</h3>
        <p className="muted">Issue #22 to #25</p>
        <ul>
          <li>Frontend foundation and API client</li>
          <li>Service listing UI with paging/filters/sort</li>
          <li>Monitoring dashboard cards</li>
          <li>Frontend test and E2E coverage</li>
        </ul>
        <p>
          <Link to="/services">Open Services View</Link>
          {' | '}
          <Link to="/monitoring">Open Monitoring Dashboard</Link>
        </p>
      </article>
    </section>
  )
}
