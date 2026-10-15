import { NavLink } from 'react-router-dom';

const navItems = [
  {
    to: '/',
    label: 'Dashboard',
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="3" width="7" height="7" rx="1" />
        <rect x="14" y="3" width="7" height="7" rx="1" />
        <rect x="3" y="14" width="7" height="7" rx="1" />
        <rect x="14" y="14" width="7" height="7" rx="1" />
      </svg>
    ),
  },
  {
    to: '/transactions',
    label: 'Transactions',
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <line x1="12" y1="1" x2="12" y2="23" />
        <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
      </svg>
    ),
  },
  {
    to: '/budgets',
    label: 'Budgets',
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
        <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
        <line x1="12" y1="22.08" x2="12" y2="12" />
      </svg>
    ),
  },
];

const SIDEBAR_WIDTH = 240;
const PRIMARY = '#6366f1';

const Layout = ({ children }) => {
  const styles = {
    shell: {
      display: 'flex',
      minHeight: '100vh',
      backgroundColor: '#f8fafc',
      fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    },
    sidebar: {
      width: SIDEBAR_WIDTH,
      minHeight: '100vh',
      backgroundColor: '#1e1b4b',
      display: 'flex',
      flexDirection: 'column',
      position: 'fixed',
      left: 0,
      top: 0,
      bottom: 0,
      zIndex: 100,
      boxShadow: '2px 0 16px rgba(0,0,0,0.12)',
    },
    logoArea: {
      padding: '28px 24px 24px',
      borderBottom: '1px solid rgba(255,255,255,0.08)',
    },
    logoRow: {
      display: 'flex',
      alignItems: 'center',
      gap: '10px',
    },
    logoIcon: {
      width: 36,
      height: 36,
      borderRadius: '9px',
      background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexShrink: 0,
    },
    logoText: {
      fontSize: '1.2rem',
      fontWeight: 800,
      color: '#ffffff',
      letterSpacing: '-0.02em',
    },
    logoSubtext: {
      fontSize: '0.7rem',
      color: '#a5b4fc',
      marginTop: '2px',
      letterSpacing: '0.04em',
    },
    nav: {
      flex: 1,
      padding: '16px 12px',
      display: 'flex',
      flexDirection: 'column',
      gap: '4px',
    },
    navSection: {
      fontSize: '0.65rem',
      fontWeight: 700,
      color: '#6366f1',
      textTransform: 'uppercase',
      letterSpacing: '0.1em',
      padding: '12px 12px 6px',
    },
    footer: {
      padding: '16px 24px',
      borderTop: '1px solid rgba(255,255,255,0.08)',
    },
    footerText: {
      fontSize: '0.7rem',
      color: '#6366f1',
      opacity: 0.7,
    },
    main: {
      marginLeft: SIDEBAR_WIDTH,
      flex: 1,
      padding: '32px',
      minHeight: '100vh',
      boxSizing: 'border-box',
    },
  };

  const linkBase = {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    padding: '10px 14px',
    borderRadius: '10px',
    textDecoration: 'none',
    color: '#a5b4fc',
    fontSize: '0.9rem',
    fontWeight: 500,
    transition: 'background 0.15s, color 0.15s',
  };

  const linkActive = {
    ...linkBase,
    backgroundColor: `${PRIMARY}22`,
    color: '#c7d2fe',
    fontWeight: 600,
    borderLeft: `3px solid ${PRIMARY}`,
    paddingLeft: '11px',
  };

  return (
    <div style={styles.shell}>
      <aside style={styles.sidebar}>
        <div style={styles.logoArea}>
          <div style={styles.logoRow}>
            <div style={styles.logoIcon}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <line x1="12" y1="1" x2="12" y2="23" />
                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
              </svg>
            </div>
            <div>
              <div style={styles.logoText}>FinPilot</div>
              <div style={styles.logoSubtext}>Finance Manager</div>
            </div>
          </div>
        </div>

        <nav style={styles.nav}>
          <div style={styles.navSection}>Main Menu</div>
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              style={({ isActive }) => (isActive ? linkActive : linkBase)}
              onMouseEnter={(e) => {
                if (!e.currentTarget.classList.contains('active')) {
                  e.currentTarget.style.background = 'rgba(99,102,241,0.1)';
                  e.currentTarget.style.color = '#e0e7ff';
                }
              }}
              onMouseLeave={(e) => {
                if (!e.currentTarget.getAttribute('aria-current')) {
                  e.currentTarget.style.background = '';
                  e.currentTarget.style.color = '#a5b4fc';
                }
              }}
            >
              <span style={{ opacity: 0.9 }}>{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div style={styles.footer}>
          <div style={styles.footerText}>v1.0.0 · FinPilot</div>
        </div>
      </aside>

      <main style={styles.main}>
        {children}
      </main>
    </div>
  );
};

export default Layout;
