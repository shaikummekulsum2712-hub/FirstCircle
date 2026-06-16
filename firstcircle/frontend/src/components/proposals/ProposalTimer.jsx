import { useEffect, useState } from "react";

export default function ProposalTimer({ initialSeconds = 1200 }) {
  const [seconds, setSeconds] = useState(initialSeconds);

  useEffect(() => {
    const timer = setInterval(() => {
      setSeconds((prev) => Math.max(0, prev - 1));
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;

  return (
    <div className="rounded-2xl bg-orange-100 px-4 py-3 text-center font-black text-orange-700">
      Expires in {minutes}:{String(remainingSeconds).padStart(2, "0")}
    </div>
  );
}