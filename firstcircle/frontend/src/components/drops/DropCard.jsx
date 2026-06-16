import { Link } from "react-router-dom";
import { circleTypes } from "../../data/constants.js";
import Button from "../common/Button.jsx";
import Badge from "../common/Badge.jsx";
import DropUrgencyBadge from "./DropUrgencyBadge.jsx";
import DropStatusBadge from "./DropStatusBadge.jsx";

export default function DropCard({ drop, onJoin }) {
  const circle = circleTypes.find((item) => item.id === drop.type);

  return (
    <article className="card-hover rounded-[2rem] border border-white bg-white p-5 shadow-soft">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className={`mb-3 inline-flex rounded-full border px-3 py-1 text-sm font-black ${circle?.color}`}>
            {circle?.emoji} {circle?.label}
          </div>
          <h3 className="text-2xl font-black text-slate-900">{drop.title}</h3>
          <p className="mt-2 line-clamp-2 text-sm leading-6 text-slate-600">{drop.description}</p>
        </div>
        <DropStatusBadge status={drop.status} />
      </div>

      <div className="mt-5 grid gap-3 rounded-3xl bg-slate-50 p-4 text-sm">
        <p><span className="font-black">🕒 Time:</span> {drop.date}, {drop.time}</p>
        <p><span className="font-black">📍 Place:</span> {drop.place}</p>
        <p><span className="font-black">👥 For:</span> {drop.audience}</p>
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        {drop.vibe.map((tag) => (
          <Badge key={tag} className="bg-pink-100 text-pink-700">#{tag}</Badge>
        ))}
      </div>

      <div className="mt-5 flex items-center justify-between gap-3">
        <DropUrgencyBadge spotsFilled={drop.spotsFilled} groupSize={drop.groupSize} />
        <span className="text-xs font-bold text-slate-400">Expires in {drop.expiresIn}</span>
      </div>

      <div className="mt-5 grid grid-cols-2 gap-3">
        <Link to={`/drops/${drop.id}`}>
          <Button variant="secondary" className="w-full">Details</Button>
        </Link>
        <Button variant="primary" className="w-full" onClick={() => onJoin(drop)}>
          Join Request
        </Button>
      </div>
    </article>
  );
}