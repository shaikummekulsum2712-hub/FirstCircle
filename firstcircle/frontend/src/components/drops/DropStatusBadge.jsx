import Badge from "../common/Badge.jsx";

export default function DropStatusBadge({ status }) {
  const styles = {
    open: "bg-green-100 text-green-700",
    "almost-full": "bg-orange-100 text-orange-700",
    confirmed: "bg-purple-100 text-purple-700",
    expired: "bg-slate-100 text-slate-600"
  };

  return (
    <Badge className={styles[status] || styles.open}>
      {status || "open"}
    </Badge>
  );
}