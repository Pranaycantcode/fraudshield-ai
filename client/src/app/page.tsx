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
import { FileUpload } from "@/components/FileUpload";
import { HighRiskTransactions } from "@/components/HighRiskTransactions";

function objectToChartData(data: Record<string, number>) {
  return Object.entries(data).map(([name, value]) => ({
    name,
    value,
  }));
}

export default function Home() {
  const [data, setData] = useState<ApiResponse | null>(null);

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

        <FileUpload onResult={setData} />

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

            <HighRiskTransactions transactions={data.high_risk_transactions} />

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
