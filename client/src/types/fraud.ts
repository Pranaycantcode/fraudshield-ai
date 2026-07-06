export type Summary = {
  total_transactions: number;
  high_risk_count: number;
  suspicious_count: number;
  safe_count: number;
  fraud_risk_percentage: number;
};

export type Transaction = {
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

export type Analytics = {
  risk_distribution: Record<string, number>;
  category_risk: Record<string, number>;
  location_risk: Record<string, number>;
};

export type ApiResponse = {
  summary: Summary;
  analytics: Analytics;
  transactions: Transaction[];
};