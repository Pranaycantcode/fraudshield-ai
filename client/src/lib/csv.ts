import { Transaction } from "@/types/fraud";

export function downloadCsv(transactions: Transaction[]) {
  const headers = [
    "transaction_id",
    "user_id",
    "timestamp",
    "amount",
    "merchant",
    "category",
    "location",
    "risk_score",
    "risk_label",
    "explanation",
  ];

  const rows = transactions.map((txn) =>
    headers.map((header) => {
      const value = txn[header as keyof Transaction];
      return `"${String(value).replace(/"/g, '""')}"`;
    })
  );

  const csvContent = [
    headers.join(","),
    ...rows.map((row) => row.join(",")),
  ].join("\n");

  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = "fraudshield-report.csv";
  link.click();

  URL.revokeObjectURL(url);
}