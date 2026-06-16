import { Link } from "react-router-dom";
import { Sparkles, Users, ShieldCheck, Wand2 } from "lucide-react";
import Button from "../components/common/Button.jsx";

export default function Landing() {
  return (
    <div className="min-h-screen overflow-hidden">
      <header className="mx-auto flex max-w-7xl items-center justify-between px-5 py-6">
        <Link to="/" className="flex items-center gap-3">
          <div className="grid h-12 w-12 place-items-center rounded-2xl bg-gradient-to-br from-yellow-300 via-pink-300 to-purple-400 text-lg font-black text-white shadow-soft">
            FC
          </div>
          <div>
            <p className="text-2xl font-black text-slate-900">FirstCircle</p>
            <p className="-mt-1 text-xs font-bold text-slate-500">Campus circles, not awkward DMs</p>
          </div>
        </Link>

        <Link to="/profile">
          <Button variant="purple">Get Started</Button>
        </Link>
      </header>

      <main className="mx-auto grid max-w-7xl items-center gap-12 px-5 py-12 lg:grid-cols-2 lg:py-20">
        <section>
          <div className="inline-flex items-center gap-2 rounded-full bg-white px-4 py-2 text-sm font-black text-orange-600 shadow-soft">
            <Sparkles size={16} /> Joyful campus matching for freshers
          </div>

          <h1 className="mt-6 text-5xl font-black leading-tight text-slate-950 md:text-7xl">
            Find your people,
            <span className="block bg-gradient-to-r from-orange-400 via-pink-500 to-purple-500 bg-clip-text text-transparent">
              one circle at a time.
            </span>
          </h1>

          <p className="mt-6 max-w-xl text-lg leading-8 text-slate-600">
            FirstCircle helps students join safe, colourful, small campus meetups based on time,
            purpose, comfort, and shared vibe — without swiping or profile judging.
          </p>

          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Link to="/profile">
              <Button variant="primary" className="w-full sm:w-auto">Create My Profile</Button>
            </Link>
            <Link to="/drops">
              <Button variant="secondary" className="w-full sm:w-auto">Explore Drops</Button>
            </Link>
          </div>

          <div className="mt-8 grid gap-3 sm:grid-cols-3">
            <MiniPoint icon={<Users />} text="Small group circles" />
            <MiniPoint icon={<ShieldCheck />} text="Safe public spots" />
            <MiniPoint icon={<Wand2 />} text="Auto-place me" />
          </div>
        </section>

        <section className="relative">
          <div className="absolute -left-10 top-10 h-40 w-40 rounded-full bg-yellow-300/50 blur-3xl"></div>
          <div className="absolute -right-10 bottom-10 h-48 w-48 rounded-full bg-pink-300/60 blur-3xl"></div>

          <div className="relative rounded-[2.5rem] bg-white p-6 shadow-soft">
            <div className="rounded-[2rem] bg-gradient-to-br from-yellow-100 via-pink-100 to-purple-100 p-6">
              <p className="text-sm font-black text-purple-700">Today’s almost-full Drop</p>
              <h2 className="mt-2 text-3xl font-black text-slate-900">Chill Freshers Circle</h2>
              <p className="mt-3 text-slate-600">Meet friendly freshers at Library Cafe today.</p>

              <div className="mt-5 grid gap-3">
                <Info label="Time" value="Today, 4:00 PM" />
                <Info label="Place" value="Library Cafe" />
                <Info label="Spots" value="3/4 joined — almost full!" />
              </div>

              <div className="mt-5 flex flex-wrap gap-2">
                {["chill", "freshers", "casual", "introvert-friendly"].map((tag) => (
                  <span key={tag} className="rounded-full bg-white px-3 py-1 text-xs font-black text-pink-600">
                    #{tag}
                  </span>
                ))}
              </div>

              <Link to="/drops">
                <Button variant="pink" className="mt-6 w-full">Join a Drop</Button>
              </Link>

              <p className="mt-4 text-center text-sm font-bold text-slate-500">
                Names stay hidden until everyone accepts 👻
              </p>
            </div>
          </div>
        </section>
      </main>

      <section className="mx-auto max-w-7xl px-5 pb-20">
        <div className="grid gap-5 md:grid-cols-4">
          <Feature emoji="🌈" title="Friend Circle" text="Find chill people with shared vibes." />
          <Feature emoji="📚" title="Study Circle" text="Study the same topic together." />
          <Feature emoji="🚀" title="Build Circle" text="Meet project and hackathon teammates." />
          <Feature emoji="🎲" title="Random Hangout" text="Join safe random campus meetups." />
        </div>
      </section>
    </div>
  );
}

function MiniPoint({ icon, text }) {
  return (
    <div className="flex items-center gap-2 rounded-2xl bg-white px-4 py-3 font-bold text-slate-700 shadow-soft">
      <span className="text-orange-500">{icon}</span>
      {text}
    </div>
  );
}

function Info({ label, value }) {
  return (
    <div className="rounded-2xl bg-white/80 p-4">
      <p className="text-xs font-black uppercase tracking-wide text-slate-400">{label}</p>
      <p className="font-black text-slate-800">{value}</p>
    </div>
  );
}

function Feature({ emoji, title, text }) {
  return (
    <div className="card-hover rounded-[2rem] bg-white p-6 shadow-soft">
      <div className="text-4xl">{emoji}</div>
      <h3 className="mt-4 text-xl font-black text-slate-900">{title}</h3>
      <p className="mt-2 text-slate-600">{text}</p>
    </div>
  );
}