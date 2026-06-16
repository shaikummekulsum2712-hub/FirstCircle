import PageWrapper from "../components/layout/PageWrapper.jsx";
import CircleHistoryCard from "../components/circles/CircleHistoryCard.jsx";
import { fakeCircles } from "../data/fakeCircles.js";

export default function CircleHistory() {
  return (
    <PageWrapper>
      <section className="mb-6 rounded-[2rem] bg-gradient-to-br from-yellow-100 via-green-100 to-blue-100 p-8 shadow-soft">
        <p className="font-black text-blue-700">Private to you</p>
        <h1 className="mt-1 text-4xl font-black text-slate-950">
          Your Circle History
        </h1>
        <p className="mt-2 text-slate-600">
          Only you can see your past Circles. This helps you track your campus
          journey.
        </p>
      </section>

      <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
        {fakeCircles.map((circle) => (
          <CircleHistoryCard key={circle.id} circle={circle} />
        ))}
      </div>
    </PageWrapper>
  );
}