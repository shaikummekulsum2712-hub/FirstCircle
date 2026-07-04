import useLocalStorage from "./useLocalStorage.js";

const emptyProfile = {
  name: "",
  email: "",
  rollNumber: "",
  year: "",
  branch: "",
  studentType: "",
  bio: "",
  interests: [],
  comfort: [],
  freeSlots: []
};

export default function useProfile() {
  const [profile, setProfile] = useLocalStorage("firstcircle_profile", emptyProfile);

  return { profile, setProfile };
}