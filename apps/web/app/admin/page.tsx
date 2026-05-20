import Link from "next/link";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchKPI() {
  try {
    const res = await fetch(`${API}/admin/kpi`, {
      headers: { Authorization: "Bearer admin@tideguard.app" },
      next: { revalidate: 30 },
    });
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

export default async function AdminPage() {
  const kpi = await fetchKPI();
  return (
    <main className="min-h-screen max-w-5xl mx-auto px-6 py-12">
      <Link href="/" className="text-teal-700 text-sm">← Back home</Link>
      <h1 className="text-4xl font-bold mt-2 mb-2">Impact KPI</h1>
      <p className="text-zinc-600 dark:text-zinc-400 mb-8">
        Read-only dashboard for jury & partners. Requires an admin user in production.
      </p>
      {!kpi ? (
        <p className="text-zinc-600">
          Could not load KPI — make sure the API is up and an admin user exists.
        </p>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <KPICard label="Users" value={kpi.users} />
          <KPICard label="Reports" value={kpi.reports_total} sub={`${kpi.reports_approved} approved`} />
          <KPICard label="Cleanups" value={kpi.cleanups} />
          <KPICard label="kg collected" value={kpi.kg_collected.toFixed(1)} />
          <KPICard label="Schools" value={kpi.schools} />
          <KPICard label="Lessons completed" value={kpi.lessons_completed} />
        </div>
      )}
    </main>
  );
}

function KPICard({ label, value, sub }: { label: string; value: number | string; sub?: string }) {
  return (
    <div className="p-6 rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900">
      <div className="text-3xl font-bold text-teal-700">{value}</div>
      <div className="text-sm text-zinc-500 mt-1">{label}</div>
      {sub && <div className="text-xs text-zinc-400 mt-1">{sub}</div>}
    </div>
  );
}
