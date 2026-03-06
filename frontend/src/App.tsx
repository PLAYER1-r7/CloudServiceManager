import { NavLink, Route, Routes } from 'react-router-dom'
import { HomePage } from './pages/HomePage'
import { MonitoringPage } from './pages/MonitoringPage'
import { ServicesPage } from './pages/ServicesPage'

function App() {
  return (
    <div className="shell">
      <header className="shell-header">
        <div>
          <p className="eyebrow">Cloud Service Manager</p>
          <h1>Multi-Cloud Control Surface</h1>
        </div>
        <nav className="top-nav" aria-label="Primary">
          <NavLink to="/" end>
            Home
          </NavLink>
          <NavLink to="/services">Services</NavLink>
          <NavLink to="/monitoring">Monitoring</NavLink>
        </nav>
      </header>

      <main className="shell-main">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/services" element={<ServicesPage />} />
          <Route path="/monitoring" element={<MonitoringPage />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
