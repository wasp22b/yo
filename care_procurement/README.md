# Care Procurement

Tender, purchase order, vendor, and receipt management for CARE

A [CARE](https://github.com/ohcnetwork/care) backend plugin. It is an ordinary Django app,
pip-installed into core and registered through `plug_config.py`. Core contains no reference
to this package.

## Install (local development)

Place the plugin inside the backend checkout as a **real directory**. A symlink breaks
`docker build`, which cannot follow links out of the build context.

```bash
mv /path/to/care_procurement $CARE_BE/care_procurement
```

`care/plug_config.py`:

```python
care_procurement = Plug(
    name="care_procurement",
    package_name="care_procurement",
    version="",
    configs={
        "PROCUREMENT_ENABLED": True,
    },
)

plugs = [care_procurement, ...]
```

Plugins are pip-installed at **image build time**, so a newly registered plug needs a rebuild:

```bash
cd $CARE_BE
make down      # safe stop. NOT `make teardown` — that deletes the database volume.
make build     # re-runs install_plugins.py
make up
make makemigrations && make migrate
```

`backend` and `celery` share one image, so a single rebuild covers both.

## API

Mounted automatically at `/api/care_procurement/` by core's `config/urls.py`.

| Method | Path | Description |
| --- | --- | --- |
| GET | `/api/care_procurement/config/` | Client-safe configuration |
| GET/POST | `/api/care_procurement/vendors/` | List or create vendors (`?facility=<uuid>` required for listing) |
| GET/PATCH/DELETE | `/api/care_procurement/vendors/{external_id}/` | Manage one vendor |
| GET/POST | `/api/care_procurement/tenders/` | List or create tenders (`?facility=<uuid>` required for listing) |
| POST | `/api/care_procurement/tenders/{external_id}/transition/` | Move a tender through its lifecycle |
| GET/POST | `/api/care_procurement/purchase-orders/` | List or create purchase orders |
| POST | `/api/care_procurement/purchase-orders/{external_id}/transition/` | Approve, receive, or cancel an order |
| GET/POST | `/api/care_procurement/receipts/` | List or create goods receipts |
| POST | `/api/care_procurement/receipts/{external_id}/transition/` | Accept or reject a receipt |

## Settings

Resolution order: `PLUGIN_CONFIGS["care_procurement"][key]` → environment variable → default.
See `care_procurement/settings.py`.
