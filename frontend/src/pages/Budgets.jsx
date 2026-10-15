import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import Modal from '../components/Modal';
import LoadingSpinner from '../components/LoadingSpinner';

const CATEGORIES = [
  'food', 'transport', 'housing', 'utilities',
  'entertainment', 'healthcare', 'education', 'shopping', 'other',
];

const MONTH_NAMES = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
];

const thisYear = new Date().getFullYear();
const thisMonth = new Date().getMonth() + 1;

const EMPTY_FORM = {
  category: 'food',
  amount: '',
  month: thisMonth,
  year: thisYear,
  description: '',
};

const fmt = (n) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n ?? 0);

const capitalize = (s) => s.charAt(0).toUpperCase() + s.slice(1);

const inputStyle = {
  width: '100%', padding: '10px 12px', borderRadius: 8,
  border: '1px solid #e2e8f0', fontSize: '0.88rem', color: '#1e293b',
  outline: 'none', boxSizing: 'border-box', backgroundColor: '#fff',
};

const labelStyle = { fontSize: '0.8rem', fontWeight: 600, color: '#475569', display: 'block', marginBottom: 5 };

const FormField = ({ label, children }) => (
  <div style={{ marginBottom: 14 }}>
    <label style={labelStyle}>{label}</label>
    {children}
  </div>
);

// Simple progress bar for spent vs budget
const SpendBar = ({ spent, budget }) => {
  const pct = budget > 0 ? Math.min(100, (spent / budget) * 100) : 0;
  const color = pct >= 100 ? '#ef4444' : pct >= 80 ? '#f59e0b' : '#10b981';
  return (
    <div style={{ marginTop: 10 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#64748b', marginBottom: 4 }}>
        <span>Spent: {fmt(spent)}</span>
        <span>{pct.toFixed(0)}% of {fmt(budget)}</span>
      </div>
      <div style={{ height: 6, borderRadius: 99, backgroundColor: '#f1f5f9', overflow: 'hidden' }}>
        <div style={{ height: '100%', width: `${pct}%`, backgroundColor: color, borderRadius: 99, transition: 'width 0.4s' }} />
      </div>
    </div>
  );
};

const Budgets = () => {
  const [budgets, setBudgets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Modal
  const [modalOpen, setModalOpen] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [form, setForm] = useState(EMPTY_FORM);
  const [formError, setFormError] = useState('');
  const [saving, setSaving] = useState(false);

  // Delete
  const [deletingId, setDeletingId] = useState(null);

  const fetchBudgets = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const { data } = await axios.get('/api/budgets');
      setBudgets(Array.isArray(data) ? data : (data.budgets ?? []));
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load budgets.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchBudgets(); }, [fetchBudgets]);

  const openAdd = () => {
    setEditingId(null);
    setForm(EMPTY_FORM);
    setFormError('');
    setModalOpen(true);
  };

  const openEdit = (b) => {
    setEditingId(b.id);
    setForm({
      category: b.category || 'food',
      amount: b.amount != null ? String(b.amount) : '',
      month: b.month || thisMonth,
      year: b.year || thisYear,
      description: b.description || '',
    });
    setFormError('');
    setModalOpen(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this budget?')) return;
    setDeletingId(id);
    try {
      await axios.delete(`/api/budgets/${id}`);
      await fetchBudgets();
    } catch (err) {
      alert(err.response?.data?.error || 'Delete failed.');
    } finally {
      setDeletingId(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError('');
    const amount = parseFloat(form.amount);
    if (isNaN(amount) || amount <= 0) return setFormError('Enter a valid positive budget amount.');
    if (!form.category) return setFormError('Category is required.');

    setSaving(true);
    try {
      const payload = { ...form, amount, month: Number(form.month), year: Number(form.year) };
      if (editingId) {
        await axios.put(`/api/budgets/${editingId}`, payload);
      } else {
        await axios.post('/api/budgets', payload);
      }
      setModalOpen(false);
      await fetchBudgets();
    } catch (err) {
      setFormError(err.response?.data?.error || 'Save failed. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const styles = {
    pageHeader: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 24 },
    heading: { fontSize: '1.6rem', fontWeight: 800, color: '#1e293b', margin: 0 },
    subHeading: { fontSize: '0.85rem', color: '#94a3b8', marginTop: 4 },
    addBtn: {
      backgroundColor: '#6366f1', color: '#fff', border: 'none',
      borderRadius: 10, padding: '10px 20px', fontSize: '0.88rem',
      fontWeight: 600, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 6,
      transition: 'background 0.15s',
    },
    grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: 20 },
    card: {
      backgroundColor: '#fff', borderRadius: 12,
      boxShadow: '0 1px 3px rgba(0,0,0,0.07), 0 4px 16px rgba(0,0,0,0.04)',
      padding: 24, display: 'flex', flexDirection: 'column', gap: 0,
    },
    cardHeader: { display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: 4 },
    cardCategory: { fontSize: '1rem', fontWeight: 700, color: '#1e293b', textTransform: 'capitalize' },
    cardPeriod: { fontSize: '0.78rem', color: '#94a3b8', marginBottom: 12 },
    cardAmount: { fontSize: '1.4rem', fontWeight: 800, color: '#6366f1' },
    actionRow: { display: 'flex', gap: 8, marginTop: 16 },
    actionBtn: (color) => ({
      flex: 1, background: 'none', border: `1px solid ${color}`,
      borderRadius: 7, color, padding: '7px 0', fontSize: '0.8rem',
      cursor: 'pointer', fontWeight: 600, transition: 'background 0.12s',
    }),
    errorBox: {
      backgroundColor: '#fef2f2', border: '1px solid #fecaca',
      borderRadius: 10, padding: '14px 18px', color: '#dc2626',
      display: 'flex', alignItems: 'center', gap: 10, marginBottom: 20,
    },
    emptyState: {
      textAlign: 'center', padding: '80px 20px', color: '#94a3b8',
    },
  };

  const formGrid = { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0 16px' };

  const years = Array.from({ length: 5 }, (_, i) => thisYear - 2 + i);

  return (
    <div style={{ maxWidth: 1100 }}>
      <div style={styles.pageHeader}>
        <div>
          <h1 style={styles.heading}>Budgets</h1>
          <p style={styles.subHeading}>{budgets.length} budget{budgets.length !== 1 ? 's' : ''} configured</p>
        </div>
        <button
          style={styles.addBtn}
          onClick={openAdd}
          onMouseEnter={(e) => { e.currentTarget.style.background = '#4f46e5'; }}
          onMouseLeave={(e) => { e.currentTarget.style.background = '#6366f1'; }}
        >
          + Add Budget
        </button>
      </div>

      {error && (
        <div style={styles.errorBox}>
          ⚠️ {error}
          <button onClick={fetchBudgets} style={{ marginLeft: 'auto', background: '#ef4444', color: '#fff', border: 'none', borderRadius: 6, padding: '4px 12px', cursor: 'pointer', fontSize: '0.8rem' }}>Retry</button>
        </div>
      )}

      {loading ? (
        <div style={{ marginTop: 60 }}><LoadingSpinner fullPage color="#6366f1" /></div>
      ) : budgets.length === 0 ? (
        <div style={styles.emptyState}>
          <div style={{ fontSize: '3rem', marginBottom: 12 }}>🎯</div>
          <div style={{ fontWeight: 700, fontSize: '1rem', color: '#475569' }}>No budgets yet</div>
          <div style={{ marginTop: 6, fontSize: '0.85rem' }}>Create your first budget to start tracking spending.</div>
          <button
            onClick={openAdd}
            style={{ ...styles.addBtn, margin: '20px auto 0', display: 'inline-flex' }}
          >
            + Create First Budget
          </button>
        </div>
      ) : (
        <div style={styles.grid}>
          {budgets.map((b) => {
            const spent = b.spent ?? 0;
            return (
              <div
                key={b.id}
                style={styles.card}
                onMouseEnter={(e) => { e.currentTarget.style.boxShadow = '0 4px 20px rgba(99,102,241,0.12)'; }}
                onMouseLeave={(e) => { e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.07), 0 4px 16px rgba(0,0,0,0.04)'; }}
              >
                <div style={styles.cardHeader}>
                  <div>
                    <div style={styles.cardCategory}>{capitalize(b.category)}</div>
                    <div style={styles.cardPeriod}>
                      {MONTH_NAMES[(b.month ?? 1) - 1]} {b.year}
                    </div>
                  </div>
                  <div style={{ fontSize: '1.5rem' }}>
                    {b.category === 'food' ? '🍔' : b.category === 'transport' ? '🚗' : b.category === 'housing' ? '🏠' : b.category === 'utilities' ? '💡' : b.category === 'entertainment' ? '🎬' : b.category === 'healthcare' ? '🏥' : b.category === 'education' ? '📚' : b.category === 'shopping' ? '🛍️' : '💼'}
                  </div>
                </div>

                <div style={styles.cardAmount}>{fmt(b.amount)}</div>
                <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Budget limit</div>

                <SpendBar spent={spent} budget={b.amount} />

                {b.description && (
                  <div style={{ fontSize: '0.78rem', color: '#94a3b8', marginTop: 10, fontStyle: 'italic' }}>
                    {b.description}
                  </div>
                )}

                <div style={styles.actionRow}>
                  <button
                    style={styles.actionBtn('#6366f1')}
                    onClick={() => openEdit(b)}
                    onMouseEnter={(e) => { e.currentTarget.style.background = '#eef2ff'; }}
                    onMouseLeave={(e) => { e.currentTarget.style.background = 'none'; }}
                  >
                    Edit
                  </button>
                  <button
                    style={styles.actionBtn('#ef4444')}
                    onClick={() => handleDelete(b.id)}
                    disabled={deletingId === b.id}
                    onMouseEnter={(e) => { e.currentTarget.style.background = '#fef2f2'; }}
                    onMouseLeave={(e) => { e.currentTarget.style.background = 'none'; }}
                  >
                    {deletingId === b.id ? '…' : 'Delete'}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Add / Edit Modal */}
      <Modal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        title={editingId ? 'Edit Budget' : 'Add Budget'}
      >
        <form onSubmit={handleSubmit}>
          <div style={formGrid}>
            <div style={{ gridColumn: '1 / -1' }}>
              <FormField label="Category *">
                <select
                  style={inputStyle}
                  value={form.category}
                  onChange={(e) => setForm(f => ({ ...f, category: e.target.value }))}
                >
                  {CATEGORIES.map((c) => (
                    <option key={c} value={c}>{capitalize(c)}</option>
                  ))}
                </select>
              </FormField>
            </div>

            <div style={{ gridColumn: '1 / -1' }}>
              <FormField label="Budget Amount *">
                <input
                  style={inputStyle}
                  type="number"
                  min="0.01"
                  step="0.01"
                  value={form.amount}
                  onChange={(e) => setForm(f => ({ ...f, amount: e.target.value }))}
                  placeholder="0.00"
                  required
                />
              </FormField>
            </div>

            <FormField label="Month *">
              <select
                style={inputStyle}
                value={form.month}
                onChange={(e) => setForm(f => ({ ...f, month: Number(e.target.value) }))}
              >
                {MONTH_NAMES.map((name, i) => (
                  <option key={i + 1} value={i + 1}>{name}</option>
                ))}
              </select>
            </FormField>

            <FormField label="Year *">
              <select
                style={inputStyle}
                value={form.year}
                onChange={(e) => setForm(f => ({ ...f, year: Number(e.target.value) }))}
              >
                {years.map((y) => (
                  <option key={y} value={y}>{y}</option>
                ))}
              </select>
            </FormField>

            <div style={{ gridColumn: '1 / -1' }}>
              <FormField label="Description">
                <textarea
                  style={{ ...inputStyle, resize: 'vertical', minHeight: 70 }}
                  value={form.description}
                  onChange={(e) => setForm(f => ({ ...f, description: e.target.value }))}
                  placeholder="Optional notes about this budget…"
                />
              </FormField>
            </div>
          </div>

          {formError && (
            <div style={{ marginTop: 4, color: '#ef4444', fontSize: '0.82rem', backgroundColor: '#fef2f2', padding: '8px 12px', borderRadius: 6 }}>
              ⚠️ {formError}
            </div>
          )}

          <div style={{ display: 'flex', gap: 12, justifyContent: 'flex-end', marginTop: 20 }}>
            <button
              type="button"
              onClick={() => setModalOpen(false)}
              style={{ padding: '10px 20px', borderRadius: 8, border: '1px solid #e2e8f0', background: '#fff', color: '#475569', fontSize: '0.88rem', cursor: 'pointer', fontWeight: 600 }}
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={saving}
              style={{ padding: '10px 24px', borderRadius: 8, border: 'none', background: '#6366f1', color: '#fff', fontSize: '0.88rem', cursor: saving ? 'not-allowed' : 'pointer', fontWeight: 600, display: 'flex', alignItems: 'center', gap: 8 }}
            >
              {saving && <LoadingSpinner size={15} color="#fff" />}
              {saving ? 'Saving…' : editingId ? 'Update Budget' : 'Add Budget'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default Budgets;
