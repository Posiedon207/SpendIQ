const LoadingSpinner = ({ size = 40, color = '#6366f1', fullPage = false }) => {
  const spinnerStyle = {
    width: size,
    height: size,
    border: `4px solid #e5e7eb`,
    borderTop: `4px solid ${color}`,
    borderRadius: '50%',
    animation: 'spin 0.8s linear infinite',
  };

  const containerStyle = fullPage
    ? {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100%',
        width: '100%',
        minHeight: 200,
      }
    : {
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
      };

  return (
    <>
      <style>{`
        @keyframes spin {
          0%   { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
      <div style={containerStyle}>
        <div style={spinnerStyle} role="status" aria-label="Loading" />
      </div>
    </>
  );
};

export default LoadingSpinner;
