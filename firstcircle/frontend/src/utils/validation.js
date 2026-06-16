export function isCollegeEmail(email) {
  return typeof email === "string" && email.includes("@") && email.includes(".");
}

export function required(value) {
  return value !== null && value !== undefined && String(value).trim() !== "";
}