import { useState } from "react";
import { useNavigate } from "react-router-dom";
import PageWrapper from "../components/layout/PageWrapper.jsx";
import Input from "../components/common/Input.jsx";
import Select from "../components/common/Select.jsx";
import Button from "../components/common/Button.jsx";
import InterestChip from "../components/profile/InterestChip.jsx";
import ComfortChip from "../components/profile/ComfortChip.jsx";
import FreeSlotForm from "../components/profile/FreeSlotForm.jsx";
import ProfileSummaryCard from "../components/profile/ProfileSummaryCard.jsx";
import useProfile from "../hooks/useProfile.js";
import { comfortOptions, interests } from "../data/constants.js";
import { userService } from "../services/userService.js";
import { profileService } from "../services/profileService.js";

export default function ProfileSetup() {
  const navigate = useNavigate();
  const { profile, setProfile } = useProfile();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  function updateField(field, value) {
    setProfile({ ...profile, [field]: value });
  }

  function toggleArray(field, value) {
    const current = profile[field] || [];
    const exists = current.includes(value);
    updateField(field, exists ? current.filter((item) => item !== value) : [...current, value]);
  }

  function addSlot(slot) {
    updateField("freeSlots", [...(profile.freeSlots || []), slot]);
  }

  function removeSlot(index) {
    updateField("freeSlots", profile.freeSlots.filter((_, i) => i !== index));
  }

  async function submitProfile(e) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (!profile.name.trim() || !profile.email.trim() || !profile.rollNumber.trim()) {
        throw new Error("Name, email, and roll number are required.");
      }

      // Create user first
      const user = await userService.createUser(profile.email, profile.name, profile.rollNumber);
      
      // Create profile next
      await profileService.createProfile(user.id, {
        year: profile.year,
        branch: profile.branch,
        studentType: profile.studentType,
        bio: profile.bio,
        interests: profile.interests,
        comfort: profile.comfort
      });

      // Save slots
      if (profile.freeSlots && profile.freeSlots.length > 0) {
        await profileService.saveFreeSlots(user.id, profile.freeSlots);
      }

      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      setError(err.message || "Failed to save profile. Running in fallback offline mode.");
      if (err.message.includes("Failed to fetch") || err.message.includes("offline")) {
        alert("Server is offline. Profile saved locally.");
        navigate("/dashboard");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <PageWrapper>
      <div className="grid gap-6 lg:grid-cols-[1.5fr_0.8fr]">
        <form onSubmit={submitProfile} className="space-y-6">
          <section className="rounded-[2rem] bg-white p-6 shadow-soft">
            <p className="font-black text-pink-600">Profile setup</p>
            <h1 className="mt-1 text-4xl font-black text-slate-950">Tell FirstCircle about you</h1>
            <p className="mt-2 text-slate-600">This helps us place you in better campus Circles.</p>

            {error && (
              <div className="mt-4 rounded-2xl bg-red-50 p-4 border border-red-200 text-sm font-bold text-red-700">
                ⚠️ {error}
              </div>
            )}

            <div className="mt-6 grid gap-4 md:grid-cols-2">
              <Input label="Name" value={profile.name} onChange={(e) => updateField("name", e.target.value)} />
              <Input label="College email" value={profile.email} onChange={(e) => updateField("email", e.target.value)} />
              <Input label="Roll number" value={profile.rollNumber || ""} placeholder="e.g. 2026-CS-01" onChange={(e) => updateField("rollNumber", e.target.value)} />

              <Select label="Year" value={profile.year} onChange={(e) => updateField("year", e.target.value)}>
                <option value="">Select year</option>
                <option>1st Year</option>
                <option>2nd Year</option>
                <option>3rd Year</option>
                <option>4th Year</option>
              </Select>

              <Input label="Branch / Major" value={profile.branch} onChange={(e) => updateField("branch", e.target.value)} />

              <Select label="Student type" value={profile.studentType} onChange={(e) => updateField("studentType", e.target.value)}>
                <option value="">Select type</option>
                <option>Hosteller</option>
                <option>Day scholar</option>
              </Select>
            </div>

            <label className="mt-4 block">
              <span className="mb-2 block text-sm font-bold text-slate-700">Short bio</span>
              <textarea
                rows="4"
                value={profile.bio}
                onChange={(e) => updateField("bio", e.target.value)}
                placeholder="I like coding, Valorant, football, and building small apps..."
                className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 outline-none focus:border-orange-400 focus:ring-4 focus:ring-orange-100"
              />
            </label>
          </section>

          <section className="rounded-[2rem] bg-white p-6 shadow-soft">
            <h2 className="text-2xl font-black text-slate-900">Pick your interests</h2>
            <div className="mt-4 flex flex-wrap gap-2">
              {interests.map((interest) => (
                <InterestChip
                  key={interest}
                  label={interest}
                  selected={profile.interests.includes(interest)}
                  onClick={() => toggleArray("interests", interest)}
                />
              ))}
            </div>
          </section>

          <section className="rounded-[2rem] bg-white p-6 shadow-soft">
            <h2 className="text-2xl font-black text-slate-900">Comfort preferences</h2>
            <div className="mt-4 grid gap-2 sm:grid-cols-2 md:grid-cols-3">
              {comfortOptions.map((option) => (
                <ComfortChip
                  key={option}
                  label={option}
                  selected={profile.comfort.includes(option)}
                  onClick={() => toggleArray("comfort", option)}
                />
              ))}
            </div>
          </section>

          <FreeSlotForm slots={profile.freeSlots || []} onAdd={addSlot} onRemove={removeSlot} />

          <Button type="submit" variant="purple" className="w-full" disabled={loading}>
            {loading ? "Saving Profile..." : "Save Profile & Continue"}
          </Button>
        </form>

        <div className="lg:sticky lg:top-24 lg:self-start">
          <ProfileSummaryCard profile={profile} />
        </div>
      </div>
    </PageWrapper>
  );
}