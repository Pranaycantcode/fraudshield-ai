import { Transaction } from "@/types/fraud";
import { RiskBadge } from "./RiskBadge";

type TransactionTableProps = {
  transactions: Transaction[];
};

export function TransactionTable({ transactions }: TransactionTableProps) {
  return (
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
            {transactions.map((txn) => (
              <tr key={txn.transaction_id} className="border-t border-slate-800">
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
  );
}