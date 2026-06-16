import { useState } from "react";
import Button from "../common/Button.jsx";
import Select from "../common/Select.jsx";
import Input from "../common/Input.jsx";

const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

export default function FreeSlotForm({ slots, onAdd, onRemove }) {
  const [slot, setSlot] = useState({
    day: "Monday",
    start: "",
    end: ""
  });

  function handleAdd() {
    if (!slot.start || !slot.end) return;
    onAdd(slot);
    setSlot({ day: "Monday", start: "", end: "" });
  }

  return (
    <div className="rounded-[2rem] bg-white p-5 shadow-soft">
      <h3 className="text-xl font-black text-slate-900">Free slots</h3>

      <div className="mt-4 grid gap-3 md:grid-cols-4">
        <Select
          label="Day"
          value={slot.day}
          onChange={(e) => setSlot({ ...slot, day: e.target.value })}
        >
          {days.map((day) => <option key={day}>{day}</option>)}
        </Select>

        <Input
          label="Start"
          type="time"
          value={slot.start}
          onChange={(e) => setSlot({ ...slot, start: e.target.value })}
        />

        <Input
          label="End"
          type="time"
          value={slot.end}
          onChange={(e) => setSlot({ ...slot, end: e.target.value })}
        />

        <div className="flex items-end">
          <Button className="w-full" onClick={handleAdd}>Add</Button>
        </div>
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        {slots.map((item, index) => (
          <button
            key={`${item.day}-${item.start}-${index}`}
            type="button"
            onClick={() => onRemove(index)}
            className="rounded-full bg-blue-100 px-4 py-2 text-sm font-bold text-blue-700"
          >
            {item.day} {item.start}-{item.end} ✕
          </button>
        ))}
      </div>
    </div>
  );
}