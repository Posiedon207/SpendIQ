import { useEffect, useRef } from 'react';

const Modal = ({ isOpen, onClose, title, children, maxWidth = 560 }) => {
  const overlayRef = useRef(null);

  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handleKeyDown);
    document.body.style.overflow = 'hidden';

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = '';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const handleOverlayClick = (e) => {
    if (e.target === overlayRef.current) onClose();
  };

  const styles = {
    overlay: {
      position: 'fixed',
      inset: 0,
      backgroundColor: 'rgba(15, 23, 42, 0.55)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '16px',
      backdropFilter: 'blur(2px)',
    },
    dialog: {
      backgroundColor: '#ffffff',
      borderRadius: '12px',
      boxShadow: '0 20px 60px rgba(0,0,0,0.2)',
      width: '100%',
      maxWidth,
      maxHeight: '90vh',
      display: 'flex',
      flexDirection: 'column',
      animation: 'modalFadeIn 0.2s ease',
    },
    header: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '20px 24px 16px',
      borderBottom: '1px solid #f1f5f9',
    },
    title: {
      margin: 0,
      fontSize: '1.1rem',
      fontWeight: 700,
      color: '#1e293b',
    },
    closeBtn: {
      background: 'none',
      border: 'none',
      cursor: 'pointer',
      color: '#94a3b8',
      fontSize: '1.4rem',
      lineHeight: 1,
      padding: '4px 8px',
      borderRadius: '6px',
      transition: 'background 0.15s, color 0.15s',
    },
    body: {
      padding: '20px 24px 24px',
      overflowY: 'auto',
    },
  };

  return (
    <>
      <style>{`
        @keyframes modalFadeIn {
          from { opacity: 0; transform: scale(0.96) translateY(-8px); }
          to   { opacity: 1; transform: scale(1) translateY(0); }
        }
      `}</style>
      <div style={styles.overlay} ref={overlayRef} onClick={handleOverlayClick} role="dialog" aria-modal="true" aria-labelledby="modal-title">
        <div style={styles.dialog}>
          <div style={styles.header}>
            <h2 id="modal-title" style={styles.title}>{title}</h2>
            <button
              style={styles.closeBtn}
              onClick={onClose}
              aria-label="Close modal"
              onMouseEnter={(e) => { e.currentTarget.style.background = '#f1f5f9'; e.currentTarget.style.color = '#475569'; }}
              onMouseLeave={(e) => { e.currentTarget.style.background = 'none'; e.currentTarget.style.color = '#94a3b8'; }}
            >
              ✕
            </button>
          </div>
          <div style={styles.body}>
            {children}
          </div>
        </div>
      </div>
    </>
  );
};

export default Modal;
