export default function Button({
  children,
  type = "button",
  variant = "primary",
  className = "",
  disabled = false,
  onClick
}) {
  const base =
    "inline-flex items-center justify-center rounded-2xl px-5 py-3 font-bold transition active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed";

  const variants = {
    primary: "bg-orange-400 text-slate-900 hover:bg-orange-500 shadow-soft",
    secondary: "bg-white text-slate-800 border border-slate-200 hover:bg-slate-50",
    pink: "bg-pink-400 text-white hover:bg-pink-500 shadow-soft",
    purple: "bg-purple-500 text-white hover:bg-purple-600 shadow-soft",
    green: "bg-emerald-400 text-slate-900 hover:bg-emerald-500 shadow-soft",
    ghost: "bg-transparent text-slate-700 hover:bg-white/70"
  };

  return (
    <button
      type={type}
      disabled={disabled}
      onClick={onClick}
      className={`${base} ${variants[variant] || variants.primary} ${className}`}
    >
      {children}
    </button>
  );
}