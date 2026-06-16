import { circleTypes } from "../../data/constants.js";

export default function DropFilters({ activeFilter, onChange }) {
  return (
    <div className="flex flex-wrap gap-2">
      <button
        onClick={() => onChange("all")}
        className={`rounded-full px-4 py-2 text-sm font-black transition ${
          activeFilter === "all" ? "bg-slate-900 text-white" : "bg-white text-slate-600 hover:bg-slate-100"
        }`}
      >
        All
      </button>

      {circleTypes.map((type) => (
        <button
          key={type.id}
          onClick={() => onChange(type.id)}
          className={`rounded-full px-4 py-2 text-sm font-black transition ${
            activeFilter === type.id ? "bg-slate-900 text-white" : "bg-white text-slate-600 hover:bg-slate-100"
          }`}
        >
          {type.emoji} {type.label}
        </button>
      ))}
    </div>
  );
}