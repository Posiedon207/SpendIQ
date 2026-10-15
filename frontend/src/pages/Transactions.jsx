import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import Modal from '../components/Modal';
import LoadingSpinner from '../components/LoadingSpinner';

const CATEGORIES = [
  'salary', 'freelance', 'investment',
  'food', 'transport', 'housing', 'utilities',
  'entertainment', 'healthcare', 'education', 'shopping', 'other',
];

const INCOME_CATS = new Set(['salary', 'freelance', 'investment']);

const EMPTY_FORM = {
  title: '', amount: '', type: 'expense', category: 'food',
  date: new Date().toISOString().slice(0, 10), description: '', is_recurring: false,
};

const fmt = (n) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n ?? 0);

const capitalize = (s) => s.charAt(0).toUpperCase() + s.slice(1);

const ROWS_PER_PAGE = 10;

const inputStyle = {
  width: '100%', padding: '10px 12px', borderRadius: 8,
  border: '1px solid #e2e8f0', fontSize: '0.88rem', color: '#1e293b',
  outline: 'none', boxSizing: 'border-box', backgroundColor: '#fff',
  transition: 'border-color 0.15s',
};

const labelStyle = { fontSize: '0.8rem', fontWeight: 600, color: '#475569', display: 'block', marginBottom: 5 };

const FormField = ({ label, children }) => (
  <div style={{ marginBottom: 14 }}>
    <label style={labelStyle}>{label}</label>
    {children}
  </div>
);

const Transactions = () => {
  const [transactions, setTransactions] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Filters
  const [typeFilter, setTypeFilter] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [search, setSearch] = useState('');
  const [searchInput, setSearchInput] = useState('');

  // Modal
  const [modalOpen, setModalOpen] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [form, setForm] = useState(EMPTY_FORM);
  const [formError, setFormError] = useState('');
  const [saving, setSaving] = useState(false);

  // Delete
  const [deletingId, setDeletingId] = useState(null);

  const totalPages = Math.max(1, Math.ceil(total / ROWS_PER_PAGE));

  const fetchTransactions = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params = { page, per_page: ROWS_PER_PAGE };
      if (typeFilter) params.type = typeFilter;
      if (categoryFilter) params.category = categoryFilter;
      if (search) params.search = search;
      const { data } = await axios.get('/api/transactions', { params });
      setTransactions(data.transactions ?? data);
      setTotal(data.total ?? (data.transactions ?? data).length);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load transactions.');
    } finally {
      setLoading(false);
    }
  }, [page, typeFilter, categoryFilter, search]);

  useEffect(() => { fetchTransactions(); }, [fetchTransactions]);

  // Reset page when filters change
  useEffect(() => { setPage(1); }, [typeFilter, categoryFilter, search]);

  const openAdd = () => {
    setEditingId(null);
    setForm(EMPTY_FORM);
    setFormError('');
    setModalOpen(true);
  };

  const openEdit = (tx) => {
    setEditingId(tx.id);
    setForm({
      title: tx.title || '',
      amount: tx.amount != null ? String(tx.amount) : '',
      type: tx.type || 'expense',
      category: tx.category || 'other',
      date: tx.date ? tx.date.slice(0, 10) : new Date().toISOString().slice(0, 10),
      description: tx.description || '',
      is_recurring: !!tx.is_recurring,
    });
    setFormError('');
    setModalOpen(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this transaction?')) return;
    setDeletingId(id);
    try {
      await axios.delete(`/api/transactions/${id}`);
      await fetchTransactions();
    } catch (err) {
      alert(err.response?.data?.error || 'Delete failed.');
    } finally {
      setDeletingId(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError('');
    if (!form.title.trim()) return setFormError('Title is required.');
    const amount = parseFloat(form.amount);
    if (isNaN(amount) || amount <= 0) return setFormError('Enter a valid positive amount.');
    if (!form.date) return setFormError('Date is required.');

    setSaving(true);
    try {
      const payload = { ...form, amount };
      if (editingId) {
        await axios.put(`/api/transactions/${editingId}`, payload);
      } else {
        await axios.post('/api/transactions', payload);
      }
      setModalOpen(false);
      await fetchTransactions();
    } catch (err) {
      setFormError(err.response?.data?.error || 'Save failed. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const handleSearchKey = (e) => {
    if (e.key === 'Enter') setSearch(searchInput.trim());
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
    filtersRow: {
      display: 'flex', gap: 12, marginBottom: 20, flexWrap: 'wrap', alignItems: 'center',
    },
    filterSelect: {
      padding: '9px 14px', borderRadius: 8, border: '1px solid #e2e8f0',
      fontSize: '0.85rem', color: '#475569', backgroundColor: '#fff', cursor: 'pointer',
      outline: 'none',
    },
    searchInput: {
      padding: '9px 14px', borderRadius: 8, border: '1px solid #e2e8f0',
      fontSize: '0.85rem', color: '#1e293b', outline: 'none', minWidth: 200,
    },
    clearBtn: {
      fontSize: '0.8rem', color: '#6366f1', background: 'none',
      border: 'none', cursor: 'pointer', textDecoration: 'underline',
    },
    tableWrapper: {
      backgroundColor: '#fff', borderRadius: 12,
      boxShadow: '0 1px 3px rgba(0,0,0,0.07), 0 4px 16px rgba(0,0,0,0.04)',
      overflow: 'hidden',
    },
    table: { width: '100%', borderCollapse: 'collapse', fontSize: '0.87rem' },
    th: {
      padding: '13px 16px', textAlign: 'left', fontSize: '0.75rem',
      fontWeight: 700, color: '#64748b', textTransform: 'uppercase',
      letterSpacing: '0.05em', backgroundColor: '#f8fafc',
      borderBottom: '1px solid #f1f5f9',
    },
    td: { padding: '13px 16px', borderBottom: '1px solid #f8fafc', color: '#374151' },
    badge: (type) => ({
      display: 'inline-block', padding: '3px 10px', borderRadius: 20,
      fontSize: '0.72rem', fontWeight: 700,
      backgroundColor: type === 'income' ? '#dcfce7' : '#fee2e2',
      color: type === 'income' ? '#15803d' : '#b91c1c',
      textTransform: 'uppercase',
    }),
    catBadge: {
      display: 'inline-block', padding: '2px 8px', borderRadius: 6,
      fontSize: '0.73rem', backgroundColor: '#f1f5f9', color: '#475569',
      textTransform: 'capitalize',
    },
    amountCell: (type) => ({ fontWeight: 700, color: type === 'income' ? '#10b981' : '#ef4444' }),
    actionBtn: (color) => ({
      background: 'none', border: `1px solid ${color}`, borderRadius: 7,
      color, padding: '4px 10px', fontSize: '0.78rem', cursor: 'pointer',
      fontWeight: 600, transition: 'background 0.12s',
    }),
    emptyState: {
      textAlign: 'center', padding: '60px 20px', color: '#94a3b8',
    },
    pagination: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '14px 20px', borderTop: '1px solid #f1f5f9' },
    pageInfo: { fontSize: '0.82rem', color: '#64748b' },
    pageBtn: (disabled) => ({
      padding: '6px 14px', borderRadius: 7, border: '1px solid #e2e8f0',
      fontSize: '0.82rem', cursor: disabled ? 'not-allowed' : 'pointer',
      backgroundColor: disabled ? '#f8fafc' : '#fff', color: disabled ? '#cbd5e1' : '#475569',
    }),
    errorBox: {
      backgroundColor: '#fef2f2', border: '1px solid #fecaca',
      borderRadius: 10, padding: '14px 18px', color: '#dc2626',
      display: 'flex', alignItems: 'center', gap: 10, marginBottom: 20,
    },
  };

  const formGrid = { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0 16px' };

  return (
    <div style={{ maxWidth: 1100 }}>
      <div style={styles.pageHeader}>
        <div>
          <h1 style={styles.heading}>Transactions</h1>
          <p style={styles.subHeading}>{total} record{total !== 1 ? 's' : ''} found</p>
        </div>
        <button
          style={styles.addBtn}
          onClick={openAdd}
          onMouseEnter={(e) => { e.currentTarget.style.background = '#4f46e5'; }}
          onMouseLeave={(e) => { e.currentTarget.style.background = '#6366f1'; }}
        >
          + Add Transaction
        </button>
      </div>

      {error && (
        <div style={styles.errorBox}>
          ⚠️ {error}
          <button onClick={fetchTransactions} style={{ marginLeft: 'auto', background: '#ef4444', color: '#fff', border: 'none', borderRadius: 6, padding: '4px 12px', cursor: 'pointer', fontSize: '0.8rem' }}>Retry</button>
        </div>
      )}

      {/* Filters */}
      <div style={styles.filtersRow}>
        <select
          style={styles.filterSelect}
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
        >
          <option value="">All Types</option>
          <option value="income">Income</option>
          <option value="expense">Expense</option>
        </select>

        <select
          style={styles.filterSelect}
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
        >
          <option value="">All Categories</option>
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>{capitalize(c)}</option>
          ))}
        </select>

        <input
          style={styles.searchInput}
          placeholder="Search by title… (Enter)"
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          onKeyDown={handleSearchKey}
        />
        {(typeFilter || categoryFilter || search) && (
          <button
            style={styles.clearBtn}
            onClick={() => { setTypeFilter(''); setCategoryFilter(''); setSearch(''); setSearchInput(''); }}
          >
            Clear filters
          </button>
        )}
      </div>

      {/* Table */}
      <div style={styles.tableWrapper}>
        {loading ? (
          <div style={{ padding: 40 }}><LoadingSpinner fullPage color="#6366f1" /></div>
        ) : transactions.length === 0 ? (
          <div style={styles.emptyState}>
            <div style={{ fontSize: '2.5rem', marginBottom: 12 }}>📭</div>
            <div style={{ fontWeight: 700, fontSize: '1rem', color: '#475569' }}>No transactions found</div>
            <div style={{ marginTop: 6, fontSize: '0.85rem' }}>Try adjusting your filters or add a new transaction.</div>
          </div>
        ) : (
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>Date</th>
                <th style={styles.th}>Title</th>
                <th style={styles.th}>Category</th>
                <th style={styles.th}>Type</th>
                <th style={styles.th}>Amount</th>
                <th style={styles.th}>Recurring</th>
                <th style={styles.th}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map((tx) => (
                <tr
                  key={tx.id}
                  onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = '#fafafa'; }}
                  onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = ''; }}
                >
                  <td style={styles.td}>{tx.date ? tx.date.slice(0, 10) : '—'}</td>
                  <td style={styles.td}>
                    <div style={{ fontWeight: 600 }}>{tx.title}</div>
                    {tx.description && <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: 2 }}>{tx.description}</div>}
                  </td>
                  <td style={styles.td}><span style={styles.catBadge}>{tx.category}</span></td>
                  <td style={styles.td}><span style={styles.badge(tx.type)}>{tx.type}</span></td>
                  <td style={{ ...styles.td, ...styles.amountCell(tx.type) }}>
                    {tx.type === 'income' ? '+' : '-'}{fmt(tx.amount)}
                  </td>
                  <td style={styles.td}>{tx.is_recurring ? '🔄 Yes' : '—'}</td>
                  <td style={styles.td}>
                    <div style={{ display: 'flex', gap: 8 }}>
                      <button
                        style={styles.actionBtn('#6366f1')}
                        onClick={() => openEdit(tx)}
                        onMouseEnter={(e) => { e.currentTarget.style.background = '#eef2ff'; }}
                        onMouseLeave={(e) => { e.currentTarget.style.background = 'none'; }}
                      >
                        Edit
                      </button>
                      <button
                        style={styles.actionBtn('#ef4444')}
                        onClick={() => handleDelete(tx.id)}
                        disabled={deletingId === tx.id}
                        onMouseEnter={(e) => { e.currentTarget.style.background = '#fef2f2'; }}
                        onMouseLeave={(e) => { e.currentTarget.style.background = 'none'; }}
                      >
                        {deletingId === tx.id ? '…' : 'Delete'}
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {/* Pagination */}
        {!loading && transactions.length > 0 && (
          <div style={styles.pagination}>
            <span style={styles.pageInfo}>
              Page {page} of {totalPages} · {total} total
            </span>
            <div style={{ display: 'flex', gap: 8 }}>
              <button style={styles.pageBtn(page === 1)} onClick={() => setPage(1)} disabled={page === 1}>«</button>
              <button style={styles.pageBtn(page === 1)} onClick={() => setPage(p => p - 1)} disabled={page === 1}>‹ Prev</button>
              <button style={styles.pageBtn(page === totalPages)} onClick={() => setPage(p => p + 1)} disabled={page === totalPages}>Next ›</button>
              <button style={styles.pageBtn(page === totalPages)} onClick={() => setPage(totalPages)} disabled={page === totalPages}>»</button>
            </div>
          </div>
        )}
      </div>

      {/* Add / Edit Modal */}
      <Modal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        title={editingId ? 'Edit Transaction' : 'Add Transaction'}
      >
        <form onSubmit={handleSubmit}>
          <div style={formGrid}>
            <div style={{ gridColumn: '1 / -1' }}>
              <FormField label="Title *">
                <input
                  style={inputStyle}
                  value={form.title}
                  onChange={(e) => setForm(f => ({ ...f, title: e.target.value }))}
                  placeholder="e.g. Monthly Salary"
                  required
                />
              </FormField>
            </div>

            <FormField label="Amount *">
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

            <FormField label="Date *">
              <input
                style={inputStyle}
                type="date"
                value={form.date}
                onChange={(e) => setForm(f => ({ ...f, date: e.target.value }))}
                required
              />
            </FormField>

            <FormField label="Type *">
              <select
                style={inputStyle}
                value={form.type}
                onChange={(e) => {
                  const t = e.target.value;
                  const defaultCat = t === 'income' ? 'salary' : 'food';
                  setForm(f => ({ ...f, type: t, category: INCOME_CATS.has(f.category) !== (t === 'income') ? defaultCat : f.category }));
                }}
              >
                <option value="income">Income</option>
                <option value="expense">Expense</option>
              </select>
            </FormField>

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

            <div style={{ gridColumn: '1 / -1' }}>
              <FormField label="Description">
                <textarea
                  style={{ ...inputStyle, resize: 'vertical', minHeight: 70 }}
                  value={form.description}
                  onChange={(e) => setForm(f => ({ ...f, description: e.target.value }))}
                  placeholder="Optional notes…"
                />
              </FormField>
            </div>

            <div style={{ gridColumn: '1 / -1' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: 10, cursor: 'pointer', fontSize: '0.88rem', color: '#475569' }}>
                <input
                  type="checkbox"
                  checked={form.is_recurring}
                  onChange={(e) => setForm(f => ({ ...f, is_recurring: e.target.checked }))}
                  style={{ width: 16, height: 16, accentColor: '#6366f1' }}
                />
                <span>Recurring transaction</span>
              </label>
            </div>
          </div>

          {formError && (
            <div style={{ marginTop: 12, color: '#ef4444', fontSize: '0.82rem', backgroundColor: '#fef2f2', padding: '8px 12px', borderRadius: 6 }}>
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
              {saving ? 'Saving…' : editingId ? 'Update' : 'Add Transaction'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default Transactions;
