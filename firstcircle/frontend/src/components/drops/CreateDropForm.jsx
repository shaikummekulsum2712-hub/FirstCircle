import { useState } from "react";
import Button from "../common/Button.jsx";
import Input from "../common/Input.jsx";
import Select from "../common/Select.jsx";
import { safePlaces, vibeTags } from "../../data/constants.js";

const initialDrop = {
  type: "friend",
  title: "",
  description: "",
  date: "Today",
  time: "",
  place: "Library Cafe",
  groupSize: 4,
  vibe: [],
  audience: "Open to anyone",
};

export default function CreateDropForm({ onCreate }) {
  const [drop, setDrop] = useState(initialDrop);

  function updateField(field, value) {
    setDrop((prev) => ({ ...prev, [field]: value }));
  }

  function toggleVibe(tag) {
    setDrop((prev) => {
      const exists = prev.vibe.includes(tag);
      return {
        ...prev,
        vibe: exists
          ? prev.vibe.filter((item) => item !== tag)
          : [...prev.vibe, tag],
      };
    });
  }

  function handleSubmit(e) {
    e.preventDefault();

    if (!drop.title.trim() || !drop.time.trim()) {
      alert("Please add a title and time.");
      return;
    }

    const newDrop = {
      ...drop,
      id: `drop-${Date.now()}`,
      spotsFilled: 1,
      status: "open",
      expiresIn: "6h 00m",
    };

    onCreate(newDrop);
    setDrop(initialDrop);
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div className="grid gap-4 md:grid-cols-2">
        <Select
          label="Circle type"
          value={drop.type}
          onChange={(e) => updateField("type", e.target.value)}
        >
          <option value="friend">Friend Circle</option>
          <option value="study">Study Circle</option>
          <option value="build">Build Circle</option>
          <option value="random">Random Hangout</option>
        </Select>

        <Select
          label="Date"
          value={drop.date}
          onChange={(e) => updateField("date", e.target.value)}
        >
          <option>Today</option>
          <option>Tomorrow</option>
          <option>Saturday</option>
          <option>This Week</option>
        </Select>

        <Input
          label="Title"
          placeholder="Example: Chill Freshers Circle"
          value={drop.title}
          onChange={(e) => updateField("title", e.target.value)}
        />

        <Input
          label="Time"
          placeholder="Example: 4:00 PM"
          value={drop.time}
          onChange={(e) => updateField("time", e.target.value)}
        />

        <Select
          label="Safe place"
          value={drop.place}
          onChange={(e) => updateField("place", e.target.value)}
        >
          {safePlaces.map((place) => (
            <option key={place}>{place}</option>
          ))}
        </Select>

        <Select
          label="Group size"
          value={drop.groupSize}
          onChange={(e) => updateField("groupSize", Number(e.target.value))}
        >
          <option value={2}>2 people</option>
          <option value={3}>3 people</option>
          <option value={4}>4 people</option>
        </Select>

        <Select
          label="Who can join?"
          value={drop.audience}
          onChange={(e) => updateField("audience", e.target.value)}
        >
          <option>Open to anyone</option>
          <option>Freshers preferred</option>
          <option>Same year preferred</option>
          <option>Same branch preferred</option>
          <option>Beginner-friendly builders</option>
          <option>Anyone learning this topic</option>
        </Select>
      </div>

      <label className="block">
        <span className="mb-2 block text-sm font-bold text-slate-700">
          Description
        </span>
        <textarea
          rows="4"
          value={drop.description}
          onChange={(e) => updateField("description", e.target.value)}
          placeholder="Tell people what this Circle is about..."
          className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 outline-none focus:border-orange-400 focus:ring-4 focus:ring-orange-100"
        />
      </label>

      <div>
        <p className="mb-2 text-sm font-bold text-slate-700">Vibe tags</p>
        <div className="flex flex-wrap gap-2">
          {vibeTags.map((tag) => (
            <button
              key={tag}
              type="button"
              onClick={() => toggleVibe(tag)}
              className={`rounded-full border px-4 py-2 text-sm font-bold transition ${
                drop.vibe.includes(tag)
                  ? "border-pink-300 bg-pink-100 text-pink-700"
                  : "border-slate-200 bg-white text-slate-600 hover:bg-slate-50"
              }`}
            >
              {drop.vibe.includes(tag) ? "✓ " : ""}#{tag}
            </button>
          ))}
        </div>
      </div>

      <Button type="submit" variant="purple" className="w-full">
        Create Circle Drop
      </Button>
    </form>
  );
}