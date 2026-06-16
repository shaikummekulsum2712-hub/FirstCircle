import Badge from "../common/Badge.jsx";

export default function CircleHistoryCard({ circle }) {
  return (
    <article className="rounded-[2rem] bg-white p-5 shadow-soft">
      <div className="flex items-center justify-between gap-3">
        <Badge className="bg-blue-100 text-blue-700">{circle.type}</Badge>
        <Badge
          className={
            circle.status === "confirmed"
              ? "bg-purple-100 text-purple-700"
              : "bg-green-100 text-green-700"
          }
        >
          {circle.status}
        </Badge>
      </div>

      <h3 className="mt-4 text-xl font-black text-slate-900">{circle.title}</h3>
      <p className="mt-2 text-sm font-semibold text-slate-600">
        {circle.date}, {circle.time}
      </p>
      <p className="text-sm text-slate-500">{circle.place}</p>
      <p className="mt-3 text-sm font-bold text-slate-500">
        {circle.peopleCount} people
      </p>
    </article>
  );
}