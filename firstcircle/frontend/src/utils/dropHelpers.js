export function getDropProgress(drop) {
  if (!drop?.groupSize) return 0;
  return Math.min(100, Math.round((drop.spotsFilled / drop.groupSize) * 100));
}

export function isDropAlmostFull(drop) {
  return drop.groupSize - drop.spotsFilled <= 1;
}

export function scoreDropForAutoPlace(drop, preferences) {
  let score = 0;

  if (preferences.category === "anything" || preferences.category === drop.type) score += 40;

  if (preferences.time === "today" && drop.date.toLowerCase() === "today") score += 25;
  if (preferences.time === "tomorrow" && drop.date.toLowerCase() === "tomorrow") score += 25;
  if (preferences.time === "week") score += 15;

  if (drop.groupSize - drop.spotsFilled === 1) score += 20;
  if (drop.spotsFilled > 0) score += 10;

  return score;
}