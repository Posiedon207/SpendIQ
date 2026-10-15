const StatCard = ({ title, value, icon, color = '#6366f1', subtitle, loading = false }) => {
  const styles = {
    card: {
      backgroundColor: '#ffffff',
      borderRadius: '12px',
      padding: '24px',
      boxShadow: '0 1px 3px rgba(0,0,0,0.07), 0 4px 16px rgba(0,0,0,0.04)',
      display: 'flex',
      flexDirection: 'column',
      gap: '12px',
      transition: 'transform 0.2s, box-shadow 0.2s',
      cursor: 'default',
    },
    header: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
    },
    title: {
      fontSize: '0.8rem',
      fontWeight: 600,
      color: '#64748b',
      textTransform: 'uppercase',
      letterSpacing: '0.05em',
    },
    iconWrapper: {
      width: 42,
      height: 42,
      borderRadius: '10px',
      backgroundColor: `${color}18`,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: '1.2rem',
    },
    value: {
      fontSize: '1.75rem',
      fontWeight: 800,
      color,
      lineHeight: 1.1,
      letterSpacing: '-0.02em',
    },
    subtitle: {
      fontSize: '0.78rem',
      color: '#94a3b8',
    },
    skeleton: {
      height: '2rem',
      width: '70%',
      backgroundColor: '#e2e8f0',
      borderRadius: '6px',
      animation: 'shimmer 1.4s infinite',
    },
  };

  return (
    <>
      <style>{`
        @keyframes shimmer {
          0%   { opacity: 1; }
          50%  { opacity: 0.4; }
          100% { opacity: 1; }
        }
      `}</style>
      <div
        style={styles.card}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'translateY(-2px)';
          e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1), 0 8px 24px rgba(0,0,0,0.06)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'translateY(0)';
          e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.07), 0 4px 16px rgba(0,0,0,0.04)';
        }}
      >
        <div style={styles.header}>
          <span style={styles.title}>{title}</span>
          {icon && <div style={styles.iconWrapper}>{icon}</div>}
        </div>
        {loading ? (
          <div style={styles.skeleton} />
        ) : (
          <div style={styles.value}>{value}</div>
        )}
        {subtitle && !loading && (
          <div style={styles.subtitle}>{subtitle}</div>
        )}
      </div>
    </>
  );
};

export default StatCard;
