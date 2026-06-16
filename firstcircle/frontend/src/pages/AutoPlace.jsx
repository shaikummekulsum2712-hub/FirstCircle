import { useState } from "react";
import { useNavigate } from "react-router-dom";
import PageWrapper from "../components/layout/PageWrapper.jsx";
import Button from "../components/common/Button.jsx";
import Select from "../components/common/Select.jsx";
import DropCard from "../components/drops/DropCard.jsx";
import useDrops from "../hooks/useDrops.js";
import { scoreDropForAutoPlace } from "../utils/dropHelpers.js";

export default function AutoPlace() {
  const navigate = useNavigate();
  const { drops, joinDrop } = useDrops();

  const [preferences, setPreferences] = useState({
    category: "anything",
    time: "today",
  });

  const [suggestedDrop, setSuggestedDrop] = useState(null);

  function updateField(field, value) {
    setPreferences((prev) => ({ ...prev, [field]: value }));
  }

  function findBestDrop() {
    const scored = drops
      .map((drop) => ({
        ...drop,
        autoScore: scoreDropForAutoPlace(drop, preferences),
      }))
      .filter((drop) => drop.autoScore > 0)
      .sort((a, b) => b.autoScore - a.autoScore);

    setSuggestedDrop(scored[0] || null);
  }

  function handleJoin(drop) {
    joinDrop(drop.id);
    navigate("/proposal");
  }

  return (
    <PageWrapper>
      <div className="mx-auto max-w-5xl">
        <section className="rounded-[2.5rem] bg-gradient-to-br from-blue-100 via-purple-100 to-pink-100 p-8 shadow-soft">
          <p className="font-black text-purple-700">Auto-place Me ✨</p>
          <h1 className="mt-1 text-4xl font-black text-slate-950">
            Let FirstCircle choose a Drop for you
          </h1>
          <p className="mt-2 max-w-2xl text-slate-600">
            You choose broad intent and time. The app recommends the best Drop
            using category fit, time fit, urgency, and fairness.
          </p>
        </section>

        <section className="mt-6 rounded-[2rem] bg-white p-6 shadow-soft">
          <div className="grid gap-4 md:grid-cols-3">
            <Select
              label="What are you open to?"
              value={preferences.category}
              onChange={(e) => updateField("category", e.target.value)}
            >
              <option value="anything">Anything</option>
              <option value="friend">Friend Circle</option>
              <option value="study">Study Circle</option>
              <option value="build">Build Circle</option>
              <option value="random">Random Hangout</option>
            </Select>

            <Select
              label="When are you free?"
              value={preferences.time}
              onChange={(e) => updateField("time", e.target.value)}
            >
              <option value="today">Today</option>
              <option value="tomorrow">Tomorrow</option>
              <option value="week">This Week</option>
            </Select>

            <div className="flex items-end">
              <Button variant="purple" className="w-full" onClick={findBestDrop}>
                Find Best Drop
              </Button>
            </div>
          </div>
        </section>

        <section className="mt-8">
          {!suggestedDrop ? (
            <div className="rounded-[2rem] bg-white p-10 text-center shadow-soft">
              <div className="text-6xl">🎯</div>
              <h2 className="mt-4 text-2xl font-black text-slate-900">
                No suggestion yet
              </h2>
              <p className="mt-2 text-slate-600">
                Choose your preference and click Find Best Drop.
              </p>
            </div>
          ) : (
            <div>
              <h2 className="mb-4 text-2xl font-black text-slate-900">
                Best suggestion for you
              </h2>
              <DropCard drop={suggestedDrop} onJoin={handleJoin} />
            </div>
          )}
        </section>
      </div>
    </PageWrapper>
  );
}