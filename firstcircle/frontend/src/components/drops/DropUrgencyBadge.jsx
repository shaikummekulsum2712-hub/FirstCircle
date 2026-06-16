import Badge from "../common/Badge.jsx";

export default function DropUrgencyBadge({ spotsFilled, groupSize }) {
  const remaining = groupSize - spotsFilled;

  if (remaining <= 1) {
    return <Badge className="bg-red-100 text-red-700">🔥 {spotsFilled}/{groupSize} almost full</Badge>;
  }

  if (spotsFilled === 0) {
    return <Badge className="bg-slate-100 text-slate-600">🌱 new drop</Badge>;
  }

  return <Badge className="bg-emerald-100 text-emerald-700">✨ {spotsFilled}/{groupSize} joined</Badge>;
}