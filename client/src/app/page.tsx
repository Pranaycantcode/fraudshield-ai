"use client";

import { useState } from "react";

type Summary = {
  total_transactions: number;
  high_risk_count: number;
  suspicious_count: number;
  safe_count: number;
  fraud_risk_percentage: number;
};

type Transaction = {
  transaction_id: string;
  user_id: string;
  timestamp: string;
  amount: number;
  merchant: string;
  category: string;
  location: string;
  risk_score: number;
  risk_label: string;
  explanation: string;
};

type ApiResponse = {
  summary: Summary;
  transactions: Transaction[];
};

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/predict`, {
      method: "POST",
      body: formData,
    });

    const result = await response.json();

    setData(result);
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-slate-950 text-white px-6 py-10">
      <section className="max-w-6xl mx-auto">
        <div className="mb-10">
          <p className="text-sm text-cyan-400 font-semibold mb-2">
            FraudShield AI
          </p>
          <h1 className="text-4xl font-bold mb-3">
            ML-powered transaction fraud detection
          </h1>
          <p className="text-slate-400 max-w-2xl">
            Upload transaction data and detect suspicious or high-risk activity
            using engineered fraud-risk signals.
          </p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 mb-8">
          <label className="block text-sm font-medium mb-3">
            Upload transaction CSV
          </label>

          <input
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="block w-full text-sm text-slate-300 file:mr-4 file:rounded-lg file:border-0 file:bg-cyan-500 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-slate-950 hover:file:bg-cyan-400"
          />

          <button
            onClick={handleUpload}
            disabled={!file || loading}
            className="mt-5 rounded-lg bg-cyan-500 px-5 py-2 font-semibold text-slate-950 disabled:opacity-50"
          >
            {loading ? "Analyzing..." : "Run Fraud Detection"}
          </button>
        </div>

        {data && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
              <SummaryCard
                title="Total Scanned"
                value={data.summary.total_transactions}
              />
              <SummaryCard
                title="High Risk"
                value={data.summary.high_risk_count}
              />
              <SummaryCard
                title="Suspicious"
                value={data.summary.suspicious_count}
              />
              <SummaryCard
                title="Risk %"
                value={`${data.summary.fraud_risk_percentage}%`}
              />
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
              <div className="p-5 border-b border-slate-800">
                <h2 className="text-xl font-semibold">Transaction Results</h2>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-slate-800 text-slate-300">
                    <tr>
                      <th className="px-4 py-3 text-left">Transaction</th>
                      <th className="px-4 py-3 text-left">User</th>
                      <th className="px-4 py-3 text-left">Amount</th>
                      <th className="px-4 py-3 text-left">Merchant</th>
                      <th className="px-4 py-3 text-left">Location</th>
                      <th className="px-4 py-3 text-left">Risk</th>
                      <th className="px-4 py-3 text-left">Explanation</th>
                    </tr>
                  </thead>

                  <tbody>
                    {data.transactions.map((txn) => (
                      <tr
                        key={txn.transaction_id}
                        className="border-t border-slate-800"
                      >
                        <td className="px-4 py-3">{txn.transaction_id}</td>
                        <td className="px-4 py-3">{txn.user_id}</td>
                        <td className="px-4 py-3">₹{txn.amount}</td>
                        <td className="px-4 py-3">{txn.merchant}</td>
                        <td className="px-4 py-3">{txn.location}</td>
                        <td className="px-4 py-3">
                          <RiskBadge label={txn.risk_label} />
                        </td>
                        <td className="px-4 py-3 text-slate-300 max-w-md">
                          {txn.explanation}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
      </section>
    </main>
  );
}

function SummaryCard({
  title,
  value,
}: {
  title: string;
  value: string | number;
}) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
      <p className="text-sm text-slate-400">{title}</p>
      <p className="text-3xl font-bold mt-2">{value}</p>
    </div>
  );
}

function RiskBadge({ label }: { label: string }) {
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