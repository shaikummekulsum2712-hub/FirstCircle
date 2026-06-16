import Button from "../common/Button.jsx";

export default function AcceptSkipActions({ onAccept, onSkip }) {
  return (
    <div className="grid gap-3 sm:grid-cols-2">
      <Button variant="secondary" onClick={onSkip}>
        Skip
      </Button>
      <Button variant="purple" onClick={onAccept}>
        Accept Circle
      </Button>
    </div>
  );
}