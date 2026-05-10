import { format, parseISO, differenceInDays, isValid } from "date-fns";

export function formatDate(dateStr: string | null | undefined, fmt = "MMM d, yyyy"): string {
  if (!dateStr) return "—";
  const parsed = parseISO(dateStr);
  return isValid(parsed) ? format(parsed, fmt) : "—";
}

export function formatShortDate(dateStr: string | null | undefined): string {
  return formatDate(dateStr, "MMM d");
}

export function daysBetween(start: string | null, end: string | null): number {
  if (!start || !end) return 0;
  return Math.max(0, differenceInDays(parseISO(end), parseISO(start)));
}

export function toISODateString(date: Date): string {
  return format(date, "yyyy-MM-dd");
}
