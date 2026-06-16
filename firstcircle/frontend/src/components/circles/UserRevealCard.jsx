export default function UserRevealCard({ user }) {
  return (
    <div className="rounded-[2rem] bg-white p-5 shadow-soft">
      <div className="grid h-16 w-16 place-items-center rounded-3xl bg-gradient-to-br from-yellow-300 via-pink-300 to-purple-400 text-2xl font-black text-white">
        {user.name[0]}
      </div>

      <h3 className="mt-4 text-xl font-black text-slate-900">{user.name}</h3>
      <p className="text-sm font-bold text-slate-500">
        {user.year}, {user.branch}
      </p>

      <div className="mt-4 flex flex-wrap gap-2">
        {user.interests.map((interest) => (
          <span
            key={interest}
            className="rounded-full bg-purple-100 px-3 py-1 text-xs font-bold text-purple-700"
          >
            {interest}
          </span>
        ))}
      </div>
    </div>
  );
}