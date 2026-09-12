import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";

import { API } from "@/utils/api";

/** A full page, injected via `manifest.routes`. Costs zero changes to core. */
export default function ExamplePage() {
  const { t } = useTranslation();
  const { data, isLoading } = useQuery({
    queryKey: ["care_nutrition", "config"],
    queryFn: () => API.config(),
  });

  return (
    <div className="p-6">
      <h1 className="text-xl font-semibold">{t("nutrition__page_title")}</h1>
      <p className="mt-2 text-sm text-gray-600">
        {isLoading
          ? t("nutrition__loading")
          : `enabled: ${String(data?.enabled)}`}
      </p>
    </div>
  );
}
