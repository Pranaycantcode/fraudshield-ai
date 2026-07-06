import { Transaction } from "@/types/fraud";
import { RiskBadge } from "./RiskBadge";

type HighRiskTransactionsProps = {
  transactions: Transaction[];
};

export function HighRiskTransactions({
  transactions,
}: HighRiskTransactionsProps) {
  if (transactions.length === 0) {
    return null;
  }

  return (
    <div className="bg-slate-900 border border-red-500/20 rounded-2xl p-5 mb-8">
      <div className="mb-4">
        <h2 className="text-xl font-semibold">High-Risk Transactions</h2>
        <p className="text-sm text-slate-400">
          Transactions requiring immediate review.
        </p>
      </div>

      <div className="space-y-3">
        {transactions.map((txn) => (
          <div
            key={txn.transaction_id}
            className="border border-slate-800 rounded-xl p-4"
          >
            <div className="flex flex-wrap items-center justify-between gap-3 mb-2">
              <div>
                <p className="font-semibold">{txn.transaction_id}</p>
                <p className="text-sm text-slate-400">
                  {txn.user_id} • {txn.merchant} • {txn.location}
                </p>
              </div>

              <RiskBadge label={txn.risk_label} />
            </div>

            <p className="text-sm text-slate-300">{txn.explanation}</p>
          </div>
        ))}
      </div>
    </div>
  );
}