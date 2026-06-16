import { Link, useNavigate, useParams } from "react-router-dom";
import PageWrapper from "../components/layout/PageWrapper.jsx";
import Button from "../components/common/Button.jsx";
import Badge from "../components/common/Badge.jsx";
import DropUrgencyBadge from "../components/drops/DropUrgencyBadge.jsx";
import VibeVotePanel from "../components/drops/VibeVotePanel.jsx";
import useDrops from "../hooks/useDrops.js";

export default function DropDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { drops, joinDrop } = useDrops();

  const drop = drops.find((item) => item.id === id);

  if (!drop) {
    return (
      <PageWrapper>
        <div className="rounded-[2rem] bg-white p-8 text-center shadow-soft">
          <div className="text-6xl">🫠</div>
          <h1 className="mt-4 text-3xl font-black text-slate-900">
            Drop not found
          </h1>
          <Link to="/drops">
            <Button className="mt-5">Back to Drops</Button>
          </Link>
        </div>
      </PageWrapper>
    );
  }

  function handleJoin() {
    joinDrop(drop.id);
    navigate("/proposal");
  }

  return (
    <PageWrapper>
      <div className="grid gap-6 lg:grid-cols-[1.4fr_0.8fr]">
        <section className="rounded-[2.5rem] bg-white p-8 shadow-soft">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <Badge className="bg-purple-100 text-purple-700">
              {drop.type} circle
            </Badge>
            <DropUrgencyBadge
              spotsFilled={drop.spotsFilled}
              groupSize={drop.groupSize}
            />
          </div>

          <h1 className="mt-5 text-5xl font-black text-slate-950">
            {drop.title}
          </h1>

          <p className="mt-4 text-lg leading-8 text-slate-600">
            {drop.description}
          </p>

          <div className="mt-6 grid gap-4 md:grid-cols-3">
            <Info emoji="🕒" label="Time" value={`${drop.date}, ${drop.time}`} />
            <Info emoji="📍" label="Place" value={drop.place} />
            <Info
              emoji="👥"
              label="Spots"
              value={`${drop.spotsFilled}/${drop.groupSize} interested`}
            />
          </div>

          <div className="mt-6">
            <p className="font-black text-slate-900">Vibe</p>
            <div className="mt-2 flex flex-wrap gap-2">
              {drop.vibe.map((tag) => (
                <Badge key={tag} className="bg-pink-100 text-pink-700">
                  #{tag}
                </Badge>
              ))}
            </div>
          </div>

          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Button variant="purple" onClick={handleJoin}>
              Join Request
            </Button>
            <Link to="/drops">
              <Button variant="secondary">Back to Drops</Button>
            </Link>
          </div>
        </section>

        <aside className="space-y-5">
          <div className="rounded-[2rem] bg-yellow-100 p-6 shadow-soft">
            <h2 className="text-xl font-black text-slate-900">
              How this stays fair 👻
            </h2>
            <ul className="mt-3 space-y-2 text-sm font-semibold text-slate-600">
              <li>Names are hidden first.</li>
              <li>No public profile browsing.</li>
              <li>Only safe campus places.</li>
              <li>No rejection is shown.</li>
            </ul>
          </div>

          <VibeVotePanel vibes={drop.vibe} />
        </aside>
      </div>
    </PageWrapper>
  );
}

function Info({ emoji, label, value }) {
  return (
    <div className="rounded-3xl bg-slate-50 p-5">
      <div className="text-3xl">{emoji}</div>
      <p className="mt-3 text-xs font-black uppercase tracking-wide text-slate-400">
        {label}
      </p>
      <p className="font-black text-slate-800">{value}</p>
    </div>
  );
}