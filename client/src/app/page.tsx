"use client";

import { useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { ApiResponse } from "@/types/fraud";
import { downloadCsv } from "@/lib/csv";
import { SummaryCard } from "@/components/SummaryCard";
import { ChartCard } from "@/components/ChartCard";
import { TransactionTable } from "@/components/TransactionTable";


function objectToChartData(data: Record<string, number>) {
  return Object.entries(data).map(([name, value]) => ({
    name,
    value,
  }));
}


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

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-8">
              <ChartCard
                title="Risk Distribution"
                data={objectToChartData(data.analytics.risk_distribution)}
              />

              <ChartCard
                title="Average Risk by Category"
                data={objectToChartData(data.analytics.category_risk)}
              />

              <ChartCard
                title="Average Risk by Location"
                data={objectToChartData(data.analytics.location_risk)}
              />
            </div>

            <div className="flex justify-end mb-4">
              <button
                onClick={() => downloadCsv(data.transactions)}
                className="rounded-lg bg-slate-100 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-white"
              >
                Download CSV Report
              </button>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
          
              <TransactionTable transactions={data.transactions} />

            </div>
          </>
        )}
      </section>
    </main>
  );
}
