# care_nutrition project brief

## Identity

- Backend repository/package: `care_nutrition`
- Frontend repository/federation remote: `care_nutrition_fe`
- Human-readable title: Care Nutrition
- Settings prefix: `NUTRITION`
- i18n prefix: `nutrition__`
- Frontend preview port: `4173`

## Product scope

Care Nutrition manages nutrition programmes with two longitudinal record types:

1. Growth monitoring measurements attached to a patient, including measurement date,
   anthropometric values, and the recording staff member.
2. Supplementation plans and events attached to a patient, with the lifecycle
   `planned → dispensed → completed`.

The plugin owns dedicated Django tables, migrations, serializers, viewsets, and permissions.
It references CARE patients and staff but does not add fields or foreign keys to core models.

## UI surfaces

- A staff-only nutrition programme route and navigation entry for reviewing and recording
  patient growth and supplementation history.
- Patient profile and encounter actions using existing CARE extension points to open the
  nutrition workflow for the relevant patient.
- No patient-portal page or OTP-authenticated API is in scope.

## Workflow and access

- Staff users can view and record growth measurements for patients they are authorized to access.
- Staff users can create supplementation plans and move them from planned to dispensed to
  completed; invalid transitions are rejected.
- No third-party services, reminders, or asynchronous integrations are required for the first
  vertical slice.

## Architecture decisions

- Keep the core diff at zero unless an existing extension point cannot support the required
  patient/encounter actions; any necessary core addition must be generic and documented.
- Mount the backend under `/api/care_nutrition/`.
- Use the CARE design system palette and scope all frontend CSS under
  `.care-nutrition-container`.
- Prefix all frontend translation keys with `nutrition__`.

## Cold-start workspace assumptions

- CARE backend checkout: `./care` if available, otherwise clone to the workspace.
- CARE frontend checkout: `./care_fe` if available, otherwise clone to the workspace.
- Plugin repositories are materialized alongside those checkouts.
