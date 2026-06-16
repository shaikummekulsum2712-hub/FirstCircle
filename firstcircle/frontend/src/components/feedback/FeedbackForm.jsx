import { useState } from "react";
import Button from "../common/Button.jsx";
import Select from "../common/Select.jsx";

export default function FeedbackForm({ onSubmit }) {
  const [form, setForm] = useState({
    didMeet: "yes",
    rating: "good",
    meetAgain: "yes",
    issue: "none",
    comment: "",
  });

  function updateField(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    onSubmit(form);
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <Select
        label="Did your Circle happen?"
        value={form.didMeet}
        onChange={(e) => updateField("didMeet", e.target.value)}
      >
        <option value="yes">Yes, we met</option>
        <option value="no">No, we did not meet</option>
        <option value="chat-only">We chatted but did not meet</option>
        <option value="i-did-not-go">I did not go</option>
      </Select>

      <Select
        label="How was the match?"
        value={form.rating}
        onChange={(e) => updateField("rating", e.target.value)}
      >
        <option value="good">Good</option>
        <option value="okay">Okay</option>
        <option value="not-my-vibe">Not my vibe</option>
        <option value="unsafe">I felt uncomfortable</option>
      </Select>

      <Select
        label="Would you meet similar people again?"
        value={form.meetAgain}
        onChange={(e) => updateField("meetAgain", e.target.value)}
      >
        <option value="yes">Yes</option>
        <option value="maybe">Maybe</option>
        <option value="no">No</option>
      </Select>

      <Select
        label="Any issue?"
        value={form.issue}
        onChange={(e) => updateField("issue", e.target.value)}
      >
        <option value="none">No issue</option>
        <option value="no-show">Someone did not show up</option>
        <option value="bad-behavior">Bad behavior</option>
        <option value="report">I want to report someone</option>
      </Select>

      <label className="block">
        <span className="mb-2 block text-sm font-bold text-slate-700">
          Optional comment
        </span>
        <textarea
          rows="4"
          value={form.comment}
          onChange={(e) => updateField("comment", e.target.value)}
          className="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:border-orange-400 focus:ring-4 focus:ring-orange-100"
          placeholder="Tell us what went well or what should improve..."
        />
      </label>

      <Button type="submit" variant="purple" className="w-full">
        Submit Feedback
      </Button>
    </form>
  );
}