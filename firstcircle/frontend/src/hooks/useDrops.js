import useLocalStorage from "./useLocalStorage.js";
import { fakeDrops } from "../data/fakeDrops.js";

export default function useDrops() {
  const [drops, setDrops] = useLocalStorage("firstcircle_drops", fakeDrops);

  function addDrop(drop) {
    setDrops((prev) => [drop, ...prev]);
  }

  function joinDrop(dropId) {
    setDrops((prev) =>
      prev.map((drop) =>
        drop.id === dropId && drop.spotsFilled < drop.groupSize
          ? { ...drop, spotsFilled: drop.spotsFilled + 1 }
          : drop
      )
    );
  }

  return { drops, setDrops, addDrop, joinDrop };
}