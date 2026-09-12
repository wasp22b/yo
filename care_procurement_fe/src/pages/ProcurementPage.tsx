import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";

import { API } from "@/utils/api";

const resourceCards = [
  ["procurement__vendors", "vendors"],
  ["procurement__tenders", "tenders"],
  ["procurement__purchase_orders", "purchase-orders"],
  ["procurement__receipts", "receipts"],
] as const;

export default function ProcurementPage() {
  const { t } = useTranslation();
  const { data: config, isLoading } = useQuery({
    queryKey: ["care_procurement", "config"],
    queryFn: () => API.config(),
  });

  return (
    <section className="mx-auto max-w-5xl p-6">
      <div className="rounded-lg border border-secondary-300 bg-white p-6 shadow-sm">
        <p className="text-sm font-medium text-primary-700">
          {t("procurement__facility_operations")}
        </p>
        <h1 className="mt-1 text-2xl font-bold">{t("procurement__page_title")}</h1>
        <p className="mt-2 max-w-2xl text-sm text-secondary-700">
          {t("procurement__page_description")}
        </p>
        <p className="mt-4 text-xs text-secondary-600">
          {isLoading
            ? t("procurement__loading")
            : config?.enabled
              ? t("procurement__enabled")
              : t("procurement__disabled")}
        </p>
      </div>
      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {resourceCards.map(([label, resource]) => (
          <div key={resource} className="rounded-lg border border-secondary-300 bg-white p-5">
            <p className="text-sm text-secondary-700">{t(label)}</p>
            <p className="mt-2 text-2xl font-bold text-primary-700">—</p>
            <p className="mt-1 text-xs text-secondary-600">
              {t("procurement__resource_path", { resource })}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}
