import { useState } from "react";
import Button from "../common/Button.jsx";
import Select from "../common/Select.jsx";

export default function ReportForm() {
  const [reason, setReason] = useState("bad-behavior");

  function handleSubmit(e) {
    e.preventDefault();
    alert("Report saved in demo mode. Later this will go to backend/admin.");
  }

  return (
    <form onSubmit={handleSubmit} className="rounded-[2rem] bg-red-50 p-5">
      <h3 className="text-xl font-black text-red-700">Report an issue</h3>
      <p className="mt-1 text-sm text-red-600">
        Use this only for safety or behavior problems.
      </p>

      <div className="mt-4">
        <Select
          label="Reason"
          value={reason}
          onChange={(e) => setReason(e.target.value)}
        >
          <option value="bad-behavior">Bad behavior</option>
          <option value="unsafe">Unsafe situation</option>
          <option value="harassment">Harassment</option>
          <option value="fake-profile">Fake profile</option>
          <option value="other">Other</option>
        </Select>
      </div>

      <Button type="submit" variant="secondary" className="mt-4 w-full">
        Submit Report
      </Button>
    </form>
  );
}