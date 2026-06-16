import Button from "./Button.jsx";

export default function EmptyState({ title, message, actionLabel, onAction }) {
  return (
    <div className="rounded-[2rem] border-2 border-dashed border-slate-200 bg-white/70 p-10 text-center">
      <div className="text-5xl">🌱</div>
      <h3 className="mt-4 text-2xl font-black text-slate-900">{title}</h3>
      <p className="mx-auto mt-2 max-w-md text-slate-600">{message}</p>
      {actionLabel && (
        <Button className="mt-5" onClick={onAction}>
          {actionLabel}
        </Button>
      )}
    </div>
  );
}