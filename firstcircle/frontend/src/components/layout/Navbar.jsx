import { Link, NavLink } from "react-router-dom";
import Button from "../common/Button.jsx";

export default function Navbar() {
  const navClass = ({ isActive }) =>
    `rounded-full px-4 py-2 text-sm font-bold transition ${
      isActive
        ? "bg-orange-100 text-orange-700"
        : "text-slate-600 hover:bg-white"
    }`;

  return (
    <header className="sticky top-0 z-40 border-b border-orange-100 bg-white/85 backdrop-blur-xl">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4">
        <Link to="/" className="flex items-center gap-3">
          <img
            src="/logo.png"
            alt="FirstCircle logo"
            className="h-12 w-12 rounded-2xl object-cover shadow-soft"
          />
          <div>
            <p className="text-xl font-black text-slate-900">FirstCircle</p>
            <p className="-mt-1 text-xs font-bold text-slate-400">
              Find your campus people
            </p>
          </div>
        </Link>

        <div className="hidden items-center gap-2 md:flex">
          <NavLink to="/dashboard" className={navClass}>
            Home
          </NavLink>
          <NavLink to="/drops" className={navClass}>
            Drops
          </NavLink>
          <NavLink to="/create-drop" className={navClass}>
            Create
          </NavLink>
          <NavLink to="/auto-place" className={navClass}>
            Auto-place
          </NavLink>
          <NavLink to="/history" className={navClass}>
            History
          </NavLink>
        </div>

        <Link to="/profile">
          <Button variant="purple" className="px-4 py-2">
            Profile
          </Button>
        </Link>
      </nav>
    </header>
  );
}