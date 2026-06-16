import { Link } from "react-router-dom";
import PageWrapper from "../components/layout/PageWrapper.jsx";
import Button from "../components/common/Button.jsx";
import useProfile from "../hooks/useProfile.js";
import { fakeDrops } from "../data/fakeDrops.js";

export default function Dashboard() {
  const { profile } = useProfile();

  return (
    <PageWrapper>
      <section className="rounded-[2.5rem] bg-gradient-to-br from-yellow-100 via-pink-100 to-purple-100 p-8 shadow-soft">
        <p className="font-black text-purple-700">Welcome back 👋</p>
        <h1 className="mt-2 text-4xl font-black text-slate-950">
          {profile.name ? `Hi ${profile.name}, ready to find your Circle?` : "Ready to find your Circle?"}
        </h1>
        <p className="mt-3 max-w-2xl text-slate-600">
          Browse existing Drops, create your own, or let FirstCircle auto-place you into the best one.
        </p>
      </section>

      <section className="mt-8 grid gap-5 md:grid-cols-3">
        <ActionCard
          emoji="🔍"
          title="Browse Drops"
          text="See what circles are open right now."
          to="/drops"
          button="Browse"
        />
        <ActionCard
          emoji="➕"
          title="Create Drop"
          text="Start a circle for a specific time and purpose."
          to="/create-drop"
          button="Create"
        />
        <ActionCard
          emoji="✨"
          title="Auto-place Me"
          text="Let the app suggest the best drop for you."
          to="/auto-place"
          button="Try it"
        />
      </section>

      <section className="mt-10">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-2xl font-black text-slate-900">Recommended Drops</h2>
          <Link to="/drops" className="font-bold text-orange-600">View all</Link>
        </div>

        <div className="grid gap-5 md:grid-cols-3">
          {fakeDrops.slice(0, 3).map((drop) => (
            <div key={drop.id} className="rounded-[2rem] bg-white p-5 shadow-soft">
              <p className="text-sm font-black text-pink-600">{drop.date}, {drop.time}</p>
              <h3 className="mt-2 text-xl font-black text-slate-900">{drop.title}</h3>
              <p className="mt-2 text-sm text-slate-600">{drop.place}</p>
              <Link to={`/drops/${drop.id}`}>
                <Button variant="secondary" className="mt-4 w-full">View Drop</Button>
              </Link>
            </div>
          ))}
        </div>
      </section>
    </PageWrapper>
  );
}

function ActionCard({ emoji, title, text, to, button }) {
  return (
    <div className="card-hover rounded-[2rem] bg-white p-6 shadow-soft">
      <div className="text-5xl">{emoji}</div>
      <h2 className="mt-4 text-2xl font-black text-slate-900">{title}</h2>
      <p className="mt-2 text-slate-600">{text}</p>
      <Link to={to}>
        <Button className="mt-5 w-full">{button}</Button>
      </Link>
    </div>
  );
}