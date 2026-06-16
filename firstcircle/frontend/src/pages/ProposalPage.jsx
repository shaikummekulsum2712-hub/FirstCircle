import { useNavigate } from "react-router-dom";
import PageWrapper from "../components/layout/PageWrapper.jsx";
import BlindProposalCard from "../components/proposals/BlindProposalCard.jsx";

export default function ProposalPage() {
  const navigate = useNavigate();

  function handleAccept() {
    navigate("/confirmed-circle");
  }

  function handleSkip() {
    alert("No worries. This rejection will not be shown to anyone.");
    navigate("/drops");
  }

  return (
    <PageWrapper>
      <div className="mx-auto max-w-3xl">
        <BlindProposalCard onAccept={handleAccept} onSkip={handleSkip} />
      </div>
    </PageWrapper>
  );
}