type SummaryCardProps = {
  title: string;
  value: string | number;
};

export function SummaryCard({ title, value }: SummaryCardProps) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
      <p className="text-sm text-slate-400">{title}</p>
      <p className="text-3xl font-bold mt-2">{value}</p>
    </div>
  );
}