export default function InterestChip({ label, selected, onClick }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`rounded-full border px-4 py-2 text-sm font-bold transition ${
        selected
          ? "border-purple-300 bg-purple-100 text-purple-700"
          : "border-slate-200 bg-white text-slate-600 hover:bg-slate-50"
      }`}
    >
      {selected ? "✓ " : ""}{label}
    </button>
  );
}