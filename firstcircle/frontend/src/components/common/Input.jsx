export default function Input({ label, error, className = "", ...props }) {
  return (
    <label className="block">
      {label && <span className="mb-2 block text-sm font-bold text-slate-700">{label}</span>}
      <input
        className={`w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 outline-none transition focus:border-orange-400 focus:ring-4 focus:ring-orange-100 ${className}`}
        {...props}
      />
      {error && <span className="mt-1 block text-sm text-red-500">{error}</span>}
    </label>
  );
}