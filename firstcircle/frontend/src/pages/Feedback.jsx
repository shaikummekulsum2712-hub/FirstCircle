import { useState } from "react";
import { Link } from "react-router-dom";
import PageWrapper from "../components/layout/PageWrapper.jsx";
import Button from "../components/common/Button.jsx";
import FeedbackForm from "../components/feedback/FeedbackForm.jsx";
import ReportForm from "../components/feedback/ReportForm.jsx";

export default function Feedback() {
  const [submitted, setSubmitted] = useState(false);
  const [showReport, setShowReport] = useState(false);

  function handleSubmit(data) {
    console.log("Feedback submitted:", data);
    setSubmitted(true);
  }

  if (submitted) {
    return (
      <PageWrapper>
        <div className="mx-auto max-w-2xl rounded-[2rem] bg-white p-8 text-center shadow-soft">
          <div className="text-6xl">💛</div>
          <h1 className="mt-4 text-3xl font-black text-slate-900">
            Thanks for your feedback
          </h1>
          <p className="mt-2 text-slate-600">
            This helps FirstCircle improve future matching and reliability.
          </p>
          <Link to="/dashboard">
            <Button className="mt-6">Back to Home</Button>
          </Link>
        </div>
      </PageWrapper>
    );
  }

  return (
    <PageWrapper>
      <div className="mx-auto grid max-w-5xl gap-6 lg:grid-cols-[1.3fr_0.8fr]">
        <section className="rounded-[2rem] bg-white p-6 shadow-soft">
          <p className="font-black text-orange-600">Post-meeting feedback</p>
          <h1 className="mt-1 text-4xl font-black text-slate-950">
            How was your Circle?
          </h1>
          <p className="mt-2 text-slate-600">
            Be honest. Feedback stays private and helps the matching engine.
          </p>

          <div className="mt-6">
            <FeedbackForm onSubmit={handleSubmit} />
          </div>
        </section>

        <aside className="space-y-5">
          <div className="rounded-[2rem] bg-yellow-100 p-5 shadow-soft">
            <h2 className="text-xl font-black text-slate-900">
              Why we ask this
            </h2>
            <ul className="mt-3 space-y-2 text-sm font-semibold text-slate-600">
              <li>Good matches get learned.</li>
              <li>No-show users get lower priority.</li>
              <li>Unsafe users can be reported/blocked.</li>
            </ul>
          </div>

          <Button
            variant="secondary"
            className="w-full"
            onClick={() => setShowReport((prev) => !prev)}
          >
            {showReport ? "Hide Report Form" : "Report an Issue"}
          </Button>

          {showReport && <ReportForm />}
        </aside>
      </div>
    </PageWrapper>
  );
}