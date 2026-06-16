import { Link } from "react-router-dom";
import PageWrapper from "../components/layout/PageWrapper.jsx";
import Button from "../components/common/Button.jsx";
import CircleCard from "../components/circles/CircleCard.jsx";
import UserRevealCard from "../components/circles/UserRevealCard.jsx";
import RescheduleButton from "../components/circles/RescheduleButton.jsx";
import { fakeUsers } from "../data/fakeUsers.js";

export default function ConfirmedCircle() {
  return (
    <PageWrapper>
      <div className="space-y-8">
        <CircleCard
          title="Chill Freshers Circle"
          time="Today, 4:00 PM"
          place="Library Cafe"
        />

        <section>
          <h2 className="mb-4 text-2xl font-black text-slate-900">
            Contact cards unlocked
          </h2>
          <div className="grid gap-5 md:grid-cols-3">
            {fakeUsers.map((user) => (
              <UserRevealCard key={user.id} user={user} />
            ))}
          </div>
        </section>

        <section className="rounded-[2rem] bg-white p-6 shadow-soft">
          <h2 className="text-2xl font-black text-slate-900">Before you go</h2>
          <ul className="mt-3 space-y-2 text-sm font-semibold text-slate-600">
            <li>Meet only at the confirmed public place.</li>
            <li>If you can’t attend, use reschedule instead of no-show.</li>
            <li>Feedback will be asked after the meetup.</li>
          </ul>

          <div className="mt-6 flex flex-col gap-3 sm:flex-row">
            <RescheduleButton />
            <Link to="/feedback">
              <Button variant="purple">Give Feedback Demo</Button>
            </Link>
          </div>
        </section>
      </div>
    </PageWrapper>
  );
}