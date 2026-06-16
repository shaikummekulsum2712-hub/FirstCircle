export default function LoadingState({ message = "Loading..." }) {
  return (
    <div className="grid min-h-[240px] place-items-center">
      <div className="text-center">
        <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-orange-200 border-t-orange-500"></div>
        <p className="mt-4 font-bold text-slate-600">{message}</p>
      </div>
    </div>
  );
}