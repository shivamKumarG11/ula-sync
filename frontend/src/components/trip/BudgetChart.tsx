import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { formatCurrency } from "@/utils/formatters";
import type { BudgetSummary } from "@/types/budget";

const COLORS = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"];

interface BudgetChartProps {
  budget: BudgetSummary;
}

export function BudgetChart({ budget }: BudgetChartProps) {
  const data = budget.by_category.map((c) => ({
    name: c.category,
    value: c.total_usd,
  }));

  return (
    <div className="flex flex-col gap-4">
      <div className="grid grid-cols-2 gap-4 text-center">
        <div>
          <p className="text-xs text-muted-foreground">Estimated</p>
          <p className="text-xl font-bold">{formatCurrency(budget.estimated_total_usd)}</p>
        </div>
        {budget.budget_total_usd && (
          <div>
            <p className="text-xs text-muted-foreground">Budget</p>
            <p className="text-xl font-bold">{formatCurrency(budget.budget_total_usd)}</p>
          </div>
        )}
      </div>
      {data.length > 0 && (
        <ResponsiveContainer width="100%" height={220}>
          <PieChart>
            <Pie data={data} cx="50%" cy="50%" outerRadius={80} dataKey="value">
              {data.map((_entry, index) => (
                <Cell key={index} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip formatter={(v: number) => formatCurrency(v)} />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}
