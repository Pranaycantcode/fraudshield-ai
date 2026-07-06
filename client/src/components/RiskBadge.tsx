type RiskBadgeProps = {
  label: string;
};

export function RiskBadge({ label }: RiskBadgeProps) {
  const className =
    label === "High Risk"
      ? "bg-red-500/20 text-red-300"
      : label === "Suspicious"
      ? "bg-yellow-500/20 text-yellow-300"
      : "bg-green-500/20 text-green-300";

  return (
    <span className={`rounded-full px-3 py-1 text-xs font-semibold ${className}`}>
      {label}
    </span>
  );
}