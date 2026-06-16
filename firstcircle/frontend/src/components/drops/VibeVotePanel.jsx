import { useState } from "react";
import Badge from "../common/Badge.jsx";

export default function VibeVotePanel({ vibes = [] }) {
  const [votes, setVotes] = useState({});

  function vote(tag, value) {
    setVotes((prev) => ({
      ...prev,
      [tag]: (prev[tag] || 0) + value
    }));
  }

  return (
    <div className="rounded-3xl bg-orange-50 p-4">
      <p className="font-black text-slate-800">Anonymous vibe voting</p>
      <p className="mt-1 text-sm text-slate-500">Help others know what this drop feels like.</p>

      <div className="mt-3 flex flex-wrap gap-2">
        {vibes.map((tag) => (
          <div key={tag} className="flex items-center gap-1 rounded-full bg-white p-1 shadow-sm">
            <Badge className="bg-yellow-100 text-yellow-800">{tag} {votes[tag] ? `(${votes[tag]})` : ""}</Badge>
            <button onClick={() => vote(tag, 1)} className="rounded-full px-2 text-sm hover:bg-green-100">👍</button>
            <button onClick={() => vote(tag, -1)} className="rounded-full px-2 text-sm hover:bg-red-100">👎</button>
          </div>
        ))}
      </div>
    </div>
  );
}