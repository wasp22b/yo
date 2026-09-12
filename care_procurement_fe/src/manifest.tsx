import { lazy } from "react";

import Page from "./components/Page";

// Keep heavy imports out of this module — it loads on every care_fe page load, for every user.
const ProcurementPage = lazy(() => import("./pages/ProcurementPage"));

/**
 * Structural mirrors of the host's prop types.
 *
 * Plugins are separate builds, so `care_fe` types cannot be imported. Declare only the
 * fields actually used. Verify names/props against `care_fe/src/pluginTypes.ts`.
 */
interface NavigationLink {
  url: string;
  name: string;
  icon?: React.ReactNode;
  children?: NavigationLink[];
}

interface Manifest {
  plugin: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  routes: Record<string, (...args: any) => React.ReactNode>;
  extends: string[];
  components: {
    // Replace with the extension points this plugin actually implements.
    FacilityHomeActions: React.LazyExoticComponent<
      React.FC<{ facility: { id: string }; className?: string }>
    >;
  };
  navItems?: NavigationLink[];
  userNavItems?: NavigationLink[];
  adminNavItems?: NavigationLink[];
}

const manifest: Manifest = {
  plugin: "care_procurement_fe",
  routes: {
    "/procurement": () => (
      <Page>
        <ProcurementPage />
      </Page>
    ),
  },
  extends: [],
  components: {
    FacilityHomeActions: lazy(
      () => import("./components/FacilityHomeActions"),
    ),
  },
  navItems: [
    {
      url: "/procurement",
      name: "procurement__nav_label",
    },
  ],
  userNavItems: [],
  adminNavItems: [],
};

export default manifest;
