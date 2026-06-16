import Button from "./Button.jsx";

export default function Modal({ open, title, children, onClose }) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-slate-900/40 p-4 backdrop-blur-sm">
      <div className="w-full max-w-lg rounded-[2rem] bg-white p-6 shadow-soft">
        <div className="mb-4 flex items-center justify-between gap-4">
          <h2 className="text-2xl font-black text-slate-900">{title}</h2>
          <Button variant="ghost" onClick={onClose}>✕</Button>
        </div>
        {children}
      </div>
    </div>
  );
}