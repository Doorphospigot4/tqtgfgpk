import Link from "next/link";

export default function HomePage() {
  return (
    <main className="min-h-screen">
      {/* Hero */}
      <section className="relative bg-gradient-to-br from-teal-700 via-teal-600 to-ocean-600 text-white overflow-hidden">
        <div className="absolute inset-0 opacity-20 bg-[radial-gradient(circle_at_20%_20%,white,transparent_40%)]" />
        <div className="relative max-w-6xl mx-auto px-6 py-24">
          <div className="max-w-3xl">
            <p className="uppercase tracking-widest text-sand-100 text-sm mb-4">
              Physics-Informed AI for our oceans
            </p>
            <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
              AI that predicts plastic before it pollutes.
            </h1>
            <p className="text-lg md:text-xl text-sand-50 max-w-2xl mb-10">
              TideGuard AI combines Sentinel imagery, ocean currents and citizen reports
              with a Physics-Informed Neural Network to forecast marine debris hotspots
              up to 14 days in advance — and turns predictions into community action.
            </p>
            <div className="flex flex-wrap gap-3">
              <Link
                href="/map"
                className="px-6 py-3 bg-white text-teal-700 font-semibold rounded-lg hover:bg-sand-50 transition"
              >
                Try the map
              </Link>
              <Link
                href="/learn"
                className="px-6 py-3 border border-white/30 rounded-lg hover:bg-white/10 transition"
              >
                Explore EE lessons
              </Link>
              <a
                href="https://github.com/Doorphospigot4/tqtgfgpk"
                className="px-6 py-3 border border-white/30 rounded-lg hover:bg-white/10 transition"
              >
                Open-source repo
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Impact counters */}
      <section className="max-w-6xl mx-auto px-6 py-16 grid grid-cols-2 md:grid-cols-4 gap-6">
        <ImpactCard label="km² monitored" value="50,000+" />
        <ImpactCard label="kg collected" value="1,240" />
        <ImpactCard label="students learning" value="320" />
        <ImpactCard label="partner schools" value="6" />
      </section>

      {/* How it works */}
      <section className="bg-sand-50/50 dark:bg-zinc-900/40 py-20">
        <div className="max-w-6xl mx-auto px-6">
          <h2 className="text-3xl font-bold mb-12 text-center">How TideGuard works</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <Step
              n={1}
              title="Fuse data"
              body="Sentinel-2/3, CMEMS currents, ERA5 wind, citizen reports — all flow into one feature store."
            />
            <Step
              n={2}
              title="Predict with physics"
              body="A PINN solves the 2D advection-diffusion equation while learning windage (α), diffusion (K) and beaching (λ)."
            />
            <Step
              n={3}
              title="Mobilize community"
              body="Schools and NGOs see hotspots on the map, get cleanup missions, learn through 10 EE lessons, earn badges."
            />
          </div>
        </div>
      </section>

      {/* CTA strip */}
      <section className="bg-teal-700 text-white py-16">
        <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-6">
          <div>
            <h3 className="text-2xl md:text-3xl font-bold mb-2">Founded by youth, for the planet.</h3>
            <p className="text-sand-100">
              Built for the Youth Innovation Challenge Taiwan 2026 + Young Climate Prize NY 2026.
            </p>
          </div>
          <div className="flex gap-3">
            <Link href="/leaderboard" className="px-5 py-3 bg-white text-teal-700 font-semibold rounded-lg">
              Community leaderboard
            </Link>
            <Link href="/admin" className="px-5 py-3 border border-white/30 rounded-lg hover:bg-white/10">
              Impact KPI
            </Link>
          </div>
        </div>
      </section>

      <footer className="text-center text-sm text-zinc-500 py-8">
        © 2026 TideGuard AI · MIT-licensed code · CC-BY-4.0 content · contact@tideguard.app
      </footer>
    </main>
  );
}

function ImpactCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="text-center p-6 rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900">
      <div className="text-3xl md:text-4xl font-bold text-teal-600">{value}</div>
      <div className="text-sm text-zinc-500 mt-2 uppercase tracking-wider">{label}</div>
    </div>
  );
}

function Step({ n, title, body }: { n: number; title: string; body: string }) {
  return (
    <div className="p-6 rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900">
      <div className="w-10 h-10 rounded-full bg-teal-100 text-teal-700 flex items-center justify-center font-bold mb-4">
        {n}
      </div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-zinc-600 dark:text-zinc-400">{body}</p>
    </div>
  );
}
