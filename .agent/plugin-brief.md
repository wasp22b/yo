# care_procurement plugin brief

## Identity

- Backend package: `care_procurement`
- Frontend package: `care_procurement_fe`
- Human title: Care Procurement
- Settings prefix: `PROCUREMENT_`
- i18n prefix: `procurement__`
- Frontend preview port: `4174`

## Purpose

Care Procurement gives facility staff a focused purchasing workspace for managing vendor
relationships and the purchasing lifecycle: publish and award tenders, create and approve
purchase orders, record received goods, and track receipt acceptance or rejection.

## Data ownership

The plugin owns its domain tables for vendors, tenders, purchase orders, and receipts. Records
are staff-facing and should use CARE base model conventions, external IDs, soft-delete filtering,
and facility-scoped access. No patient portal flow is required.

## Lifecycle and roles

- Tender: `draft` -> `published` -> `awarded` -> `closed`
- Purchase order: `draft` -> `approved` -> `received` -> `cancelled`
- Receipt: `pending` -> `accepted` or `rejected`
- Facility procurement staff may create and manage procurement records within their facility.
- Approval and awarding actions require the existing facility-management capability where the
  host permission model exposes it; the implementation must not invent a new core role.

## UI

Use a dedicated plugin route and navigation entry for the procurement workspace. Existing host
extension points are not needed for the first vertical slice; do not modify `care_fe`.

## Integrations

No third-party service is required. Configuration should remain environment/Plug supplied, with
no committed credentials.

## Core overlap

Keep core changes at zero unless registration is required by the local CARE checkout. The plugin
must own its models, migrations, API, UI, and i18n namespace.
