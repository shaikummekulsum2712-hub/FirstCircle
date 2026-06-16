import useProfile from "./useProfile.js";

export default function useAuth() {
  const { profile } = useProfile();

  return {
    isLoggedIn: Boolean(profile?.email),
    user: profile
  };
}