export default function ComfortChip({ label, selected, onClick }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`rounded-2xl border px-4 py-3 text-sm font-bold transition ${
        selected
          ? "border-orange-300 bg-orange-100 text-orange-700"
          : "border-slate-200 bg-white text-slate-600 hover:bg-slate-50"
      }`}
    >
      {selected ? "✨ " : ""}{label}
    </button>
  );
}