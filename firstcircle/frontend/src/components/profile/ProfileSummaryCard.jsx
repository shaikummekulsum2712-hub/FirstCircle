export default function ProfileSummaryCard({ profile }) {
  return (
    <div className="rounded-[2rem] bg-white p-6 shadow-soft">
      <h3 className="text-xl font-black text-slate-900">Your profile preview</h3>
      <div className="mt-4 space-y-2 text-sm text-slate-600">
        <p><b>Name:</b> {profile.name || "Not added"}</p>
        <p><b>Year:</b> {profile.year || "Not added"}</p>
        <p><b>Branch:</b> {profile.branch || "Not added"}</p>
        <p><b>Bio:</b> {profile.bio || "Not added"}</p>
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        {profile.interests?.map((interest) => (
          <span key={interest} className="rounded-full bg-purple-100 px-3 py-1 text-xs font-bold text-purple-700">
            {interest}
          </span>
        ))}
      </div>
    </div>
  );
}