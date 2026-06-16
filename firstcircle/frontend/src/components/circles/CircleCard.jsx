import Button from "../common/Button.jsx";

export default function CircleCard({ title, time, place }) {
  return (
    <div className="rounded-[2.5rem] bg-gradient-to-br from-green-100 via-blue-100 to-purple-100 p-8 shadow-soft">
      <p className="font-black text-green-700">Circle confirmed 🎉</p>

      <h1 className="mt-2 text-4xl font-black text-slate-950">
        {title}
      </h1>

      <p className="mt-3 text-lg font-bold text-slate-700">
        {time}
      </p>

      <p className="text-slate-600">
        {place}
      </p>

      <div className="mt-6 flex flex-col gap-3 sm:flex-row">
        <Button variant="green">Open Group Chat</Button>
        <Button variant="secondary">Add Reminder</Button>
      </div>
    </div>
  );
}