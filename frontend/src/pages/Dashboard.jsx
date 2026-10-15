import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell, Tooltip as PieTooltip,
} from 'recharts';
import StatCard from '../components/StatCard';
import LoadingSpinner from '../components/LoadingSpinner';

const COLORS = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'];

const fmt = (n) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(n ?? 0);

const MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

const CustomBarTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: '#1e293b', borderRadius: 8, padding: '10px 14px', color: '#fff', fontSize: '0.82rem' }}>
      <div style={{ fontWeight: 700, marginBottom: 6 }}>{label}</div>
      {payload.map((p) => (
        <div key={p.name} style={{ color: p.color }}>
          {p.name}: {fmt(p.value)}
        </div>
      ))}
    </div>
  );
};

const CustomPieTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: '#1e293b', borderRadius: 8, padding: '10px 14px', color: '#fff', fontSize: '0.82rem' }}>
      <div style={{ fontWeight: 700 }}>{payload[0].name}</div>
      <div>{fmt(payload[0].value)}</div>
    </div>
  );
};

const SkeletonBlock = ({ h = 16, w = '100%', mb = 0 }) => (
  <div style={{
    height: h, width: w, background: '#e2e8f0', borderRadius: 6,
    marginBottom: mb, animation: 'shimmer 1.4s infinite',
  }} />
);

const Dashboard = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [seeding, setSeeding] = useState(false);
  const [seedMsg, setSeedMsg] = useState('');

  const fetchAnalytics = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const { data } = await axios.get('/api/analytics');
      setAnalytics(data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load analytics data.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchAnalytics(); }, [fetchAnalytics]);

  const handleSeed = async () => {
    setSeeding(true);
    setSeedMsg('');
    try {
      const { data } = await axios.post('/api/seed');
      setSeedMsg(data.message || 'Sample data seeded successfully!');
      await fetchAnalytics();
    } catch (err) {
      setSeedMsg(err.response?.data?.error || 'Failed to seed data.');
    } finally {
      setSeeding(false);
    }
  };

  const summary = analytics?.summary || {};
  const monthlyData = (analytics?.monthly_data || []).map((row) => ({
    ...row,
    month: MONTH_NAMES[(row.month ?? 1) - 1],
  }));
  const categoryData = analytics?.category_breakdown || [];

  const styles = {
    page: { maxWidth: 1200 },
    pageHeader: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 28 },
    heading: { fontSize: '1.6rem', fontWeight: 800, color: '#1e293b', margin: 0 },
    subHeading: { fontSize: '0.85rem', color: '#94a3b8', marginTop: 4 },
    seedBtn: {
      display: 'flex', alignItems: 'center', gap: 8,
      backgroundColor: '#6366f1', color: '#fff',
      border: 'none', borderRadius: 10, padding: '10px 20px',
      fontSize: '0.88rem', fontWeight: 600, cursor: 'pointer',
      transition: 'background 0.15s, transform 0.1s',
    },
    statsGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 20, marginBottom: 28 },
    chartsGrid: { display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 20, marginBottom: 28 },
    card: {
      backgroundColor: '#fff', borderRadius: 12,
      boxShadow: '0 1px 3px rgba(0,0,0,0.07), 0 4px 16px rgba(0,0,0,0.04)',
      padding: 24,
    },
    cardTitle: { fontSize: '0.9rem', fontWeight: 700, color: '#1e293b', marginBottom: 20 },
    errorBox: {
      backgroundColor: '#fef2f2', border: '1px solid #fecaca',
      borderRadius: 10, padding: '14px 18px', color: '#dc2626',
      display: 'flex', alignItems: 'center', gap: 10, marginBottom: 24,
    },
    seedMsg: { fontSize: '0.82rem', marginTop: 8, color: seedMsg.includes('success') || seedMsg.includes('seeded') ? '#10b981' : '#ef4444' },
  };

  return (
    <>
      <style>{`
        @keyframes shimmer { 0%,100%{opacity:1} 50%{opacity:0.4} }
      `}</style>
      <div style={styles.page}>
        <div style={styles.pageHeader}>
          <div>
            <h1 style={styles.heading}>Dashboard</h1>
            <p style={styles.subHeading}>Your financial overview at a glance</p>
          </div>
          <div>
            <button
              style={styles.seedBtn}
              onClick={handleSeed}
              disabled={seeding}
              onMouseEnter={(e) => { e.currentTarget.style.background = '#4f46e5'; }}
              onMouseLeave={(e) => { e.currentTarget.style.background = '#6366f1'; }}
            >
              {seeding ? <LoadingSpinner size={16} color="#fff" /> : '🌱'}
              {seeding ? 'Seeding…' : 'Seed Sample Data'}
            </button>
            {seedMsg && <div style={styles.seedMsg}>{seedMsg}</div>}
          </div>
        </div>

        {error && (
          <div style={styles.errorBox}>
            <span>⚠️</span>
            <span>{error}</span>
            <button
              onClick={fetchAnalytics}
              style={{ marginLeft: 'auto', background: '#ef4444', color: '#fff', border: 'none', borderRadius: 6, padding: '4px 12px', cursor: 'pointer', fontSize: '0.8rem' }}
            >
              Retry
            </button>
          </div>
        )}

        {/* Stat Cards */}
        <div style={styles.statsGrid}>
          <StatCard
            title="Total Income"
            value={loading ? '' : fmt(summary.total_income)}
            icon="💰"
            color="#10b981"
            subtitle="All time"
            loading={loading}
          />
          <StatCard
            title="Total Expenses"
            value={loading ? '' : fmt(summary.total_expenses)}
            icon="💸"
            color="#ef4444"
            subtitle="All time"
            loading={loading}
          />
          <StatCard
            title="Net Balance"
            value={loading ? '' : fmt(summary.net_balance)}
            icon="📊"
            color="#6366f1"
            subtitle="Income − Expenses"
            loading={loading}
          />
          <StatCard
            title="Transactions"
            value={loading ? '' : (summary.transaction_count ?? 0)}
            icon="🔢"
            color="#f59e0b"
            subtitle="Total records"
            loading={loading}
          />
        </div>

        {/* Charts */}
        <div style={styles.chartsGrid}>
          {/* Bar Chart */}
          <div style={styles.card}>
            <div style={styles.cardTitle}>Monthly Income vs Expenses</div>
            {loading ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                <SkeletonBlock h={200} />
              </div>
            ) : monthlyData.length === 0 ? (
              <div style={{ color: '#94a3b8', textAlign: 'center', padding: '40px 0' }}>No monthly data yet. Seed some data!</div>
            ) : (
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={monthlyData} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="month" tick={{ fontSize: 12, fill: '#64748b' }} />
                  <YAxis tick={{ fontSize: 11, fill: '#64748b' }} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
                  <Tooltip content={<CustomBarTooltip />} />
                  <Legend wrapperStyle={{ fontSize: '0.82rem' }} />
                  <Bar dataKey="income" name="Income" fill="#10b981" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="expenses" name="Expenses" fill="#ef4444" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>

          {/* Pie Chart */}
          <div style={styles.card}>
            <div style={styles.cardTitle}>Expense by Category</div>
            {loading ? (
              <SkeletonBlock h={220} />
            ) : categoryData.length === 0 ? (
              <div style={{ color: '#94a3b8', textAlign: 'center', padding: '40px 0' }}>No category data yet.</div>
            ) : (
              <>
                <ResponsiveContainer width="100%" height={180}>
                  <PieChart>
                    <Pie
                      data={categoryData}
                      dataKey="total"
                      nameKey="category"
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      innerRadius={45}
                      paddingAngle={2}
                    >
                      {categoryData.map((_, i) => (
                        <Cell key={i} fill={COLORS[i % COLORS.length]} />
                      ))}
                    </Pie>
                    <PieTooltip content={<CustomPieTooltip />} />
                  </PieChart>
                </ResponsiveContainer>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px 12px', marginTop: 8 }}>
                  {categoryData.map((d, i) => (
                    <div key={d.category} style={{ display: 'flex', alignItems: 'center', gap: 5, fontSize: '0.75rem', color: '#475569' }}>
                      <div style={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: COLORS[i % COLORS.length] }} />
                      <span style={{ textTransform: 'capitalize' }}>{d.category}</span>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default Dashboard;
