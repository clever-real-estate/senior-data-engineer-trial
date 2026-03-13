# Senior Data Architecture Engineer — Take-Home Assignment

## Quick Start

```bash
cp .env.example .env
docker-compose up --build -d
# Airflow UI: http://localhost:8080  (admin / admin)
# Verify: trigger the "example_hello_world" DAG — it should succeed.
```

Tear down: `docker-compose down -v`

---

## The Scenario

You're joining a data engineering team that uses **Apache Airflow** for orchestration and **Databricks** for compute. The company's e-commerce analytics pipeline has been running for a few months, but a recent data audit surfaced quality issues in the source systems. On top of that, the upstream engineering team is rolling out a **schema change** to the orders feed, and the analytics team just submitted a request for a **second analytical view**.

Your task is to build a production-quality pipeline that handles these real-world challenges — messy data, evolving schemas, and multiple stakeholders with different analytical needs.

### The Data

| File | Location | Description |
|---|---|---|
| `orders.csv` | `data/raw/` | ~5,000 e-commerce orders spanning Jan–Mar 2024. |
| `orders_v2_sample.csv` | `data/raw/` | 200 orders in a **new schema format** the engineering team is rolling out. Your pipeline must handle both file formats. |
| `products.json` | `data/raw/` | Product catalog — 15 products across 2 categories and 6 subcategories, including cost price and weight. |

### Business Requirements

1. **Ingest** raw order data from both file formats and the product catalog from `data/raw/`.
2. **Produce two analytical outputs** in `data/output/`:
   - **Daily Product Summary** — revenue, cost, profit, and order count per product per day.
   - **Monthly Country Summary** — total revenue, total orders, average order value, and unique customers per country per month.

---

## Deliverables

Target **2–3 hours**; up to 4 hours is acceptable. We value quality and architectural reasoning over completeness — a well-designed partial solution beats a rushed end-to-end one.

| Deliverable | Location | Notes |
|---|---|---|
| Airflow DAG(s) | `dags/` | Orchestrate the full pipeline. Use the `MockDatabricksSubmitRunOperator` in `plugins/operators/mock_databricks.py` for at least one task. |
| Transformation logic | `scripts/` or inline | Local Python. PySpark is available via `requirements.txt` if you prefer it. No real Databricks cluster needed. |
| Infrastructure-as-Code | `infra/` | Show how you'd deploy this beyond local dev (Terraform, K8s manifests, CI/CD — pick what makes sense). Doesn't need to be runnable. |
| Design document | `docs/` | 1–2 pages covering architecture and key design decisions. |
| Tests | `tests/` | Encouraged. `pytest` is available. |
| README updates | This file or a new one | How to run it, assumptions, what you'd improve. |

---

## Environment

| Component | Detail |
|---|---|
| Airflow | 3.0.1 (LocalExecutor, Postgres 15 backend) |
| Python | 3.12 |
| PySpark | 3.5.4 (optional) |

**Airflow 3.0 note:** Standard operators live in `airflow.providers.standard`. Custom operators should extend `airflow.sdk.BaseOperator`. Use `logical_date` / `data_interval_start` / `data_interval_end` — `execution_date` has been removed.

Environment variables available in containers: `RAW_DATA_PATH`, `OUTPUT_DATA_PATH`, `DATABRICKS_HOST`, `DATABRICKS_TOKEN`.

---

## Submission

1. Push your work to a private GitHub repo and invite Jimmy Lien (@jlien) and Trent Seigfried (@trents).
2. Make sure `docker-compose up --build` still works with your changes.
3. Ensure we can trigger your DAG(s) from the Airflow UI and see results in `data/output/`.
