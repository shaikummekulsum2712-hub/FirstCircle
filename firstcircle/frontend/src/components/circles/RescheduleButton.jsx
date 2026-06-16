import { useNavigate } from "react-router-dom";
import Button from "../common/Button.jsx";

export default function RescheduleButton() {
  const navigate = useNavigate();

  function handleReschedule() {
    alert("We'll try to place you into the next best Drop.");
    navigate("/auto-place");
  }

  return (
    <Button variant="secondary" onClick={handleReschedule}>
      Can’t make it? Reschedule
    </Button>
  );
}