import Badge from "../common/Badge.jsx";
import ProposalTimer from "./ProposalTimer.jsx";
import AcceptSkipActions from "./AcceptSkipActions.jsx";

export default function BlindProposalCard({ onAccept, onSkip }) {
  return (
    <article className="rounded-[2.5rem] bg-white p-8 shadow-soft">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <Badge className="bg-purple-100 text-purple-700">
          Blind Proposal 👻
        </Badge>
        <ProposalTimer />
      </div>

      <h1 className="mt-6 text-4xl font-black text-slate-950">
        Your Circle is ready
      </h1>

      <p className="mt-3 text-slate-600">
        A possible group is ready. Names and contact cards are still hidden.
        Accept only if you are comfortable.
      </p>

      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <Info emoji="🌈" label="Circle" value="Friend Circle" />
        <Info emoji="🕒" label="Time" value="Today, 4:00 PM" />
        <Info emoji="📍" label="Place" value="Library Cafe" />
        <Info emoji="👥" label="Group" value="4 people interested" />
      </div>

      <div className="mt-6 rounded-3xl bg-yellow-50 p-5">
        <p className="font-black text-slate-900">Shared vibe</p>
        <div className="mt-3 flex flex-wrap gap-2">
          {["chill", "freshers", "casual", "introvert-friendly"].map((tag) => (
            <Badge key={tag} className="bg-pink-100 text-pink-700">
              #{tag}
            </Badge>
          ))}
        </div>
      </div>

      <div className="mt-7">
        <AcceptSkipActions onAccept={onAccept} onSkip={onSkip} />
      </div>
    </article>
  );
}

function Info({ emoji, label, value }) {
  return (
    <div className="rounded-3xl bg-slate-50 p-5">
      <div className="text-3xl">{emoji}</div>
      <p className="mt-2 text-xs font-black uppercase tracking-wide text-slate-400">
        {label}
      </p>
      <p className="font-black text-slate-800">{value}</p>
    </div>
  );
}