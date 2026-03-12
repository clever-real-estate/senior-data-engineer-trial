# Senior Data Architecture Engineer — Take-Home Assignment

## Quick Start

```bash
# 1. Clone and enter the repo
git clone <repo-url> && cd senior-data-engineer-trial

# 2. Copy the environment file
cp .env.example .env

# 3. Start the local Airflow environment
#    (use "docker compose" if "docker-compose" is not found on your system)
docker-compose up --build -d

# 4. Open the Airflow UI
#    http://localhost:8080  (admin / admin)

# 5. Verify: trigger the "example_hello_world" DAG from the UI — it should succeed.
```

Tear down when finished:

```bash
docker-compose down -v
```

---

## The Scenario

You're joining a data engineering team that uses **Apache Airflow** for orchestration and **Databricks** for compute. The company's e-commerce analytics pipeline has been running for a few months, but a recent data audit surfaced quality issues in the source systems. On top of that, the upstream engineering team is rolling out a **schema change** to the orders feed, and the analytics team just submitted a request for a **second analytical view**.

Your task is to build a production-quality pipeline that handles these real-world challenges — messy data, evolving schemas, and multiple stakeholders with different analytical needs.

### The Data

| File | Location | Description |
|---|---|---|
| `orders.csv` | `data/raw/` | ~5,000 e-commerce orders spanning Jan–Mar 2024. **This data comes from production and may contain quality issues. Explore before you build.** |
| `orders_v2_sample.csv` | `data/raw/` | 200 orders in a **new schema format** the engineering team is rolling out. Your pipeline must handle both file formats. |
| `products.json` | `data/raw/` | Product catalog — 15 products across 2 categories and 6 subcategories, including cost price and weight. |

### Business Requirements

1. **Ingest** raw order data from both file formats and the product catalog from `data/raw/`.
2. **Clean and validate** the data — handle any quality issues you discover. Document what you find and how you address each issue.
3. **Standardize** both order schemas into a single unified model so the pipeline works the same regardless of which file format arrives.
4. **Enrich** by joining with the product catalog, computing line-item totals and profit margins, and filtering to completed orders.
5. **Produce two analytical outputs** in `data/output/`:
   - **Daily Product Summary** — revenue, cost, profit, and order count per product per day.
   - **Monthly Country Summary** — total revenue, total orders, average order value, and unique customers per country per month.
6. **Document your data lineage** — provide a data catalog or manifest that describes your tables, their schemas, upstream sources, and any freshness or quality expectations.

---

## What We're Asking You to Build

Target **2–3 hours**; up to 4 hours is acceptable given the scope. We value quality and architectural reasoning over completeness — a well-designed partial solution beats a rushed end-to-end one.

**If you're running short on time, prioritize in this order:**
1. DAG design with layered architecture
2. Data quality handling
3. Both gold-layer analytical outputs
4. Data catalog / lineage manifest

### 1. Airflow DAG(s) — *Required*

Design and implement one or more DAGs in the `dags/` directory that orchestrate the full pipeline.

**Expectations:**
- Your DAG design should reflect a **layered data architecture** (e.g., raw/cleaned/analytical) with shared transformation stages feeding multiple analytical outputs.
- Model task dependencies cleanly — show the diamond/fan-out pattern where shared work feeds different downstream views.
- Make the pipeline **idempotent** — re-running for the same date shouldn't produce duplicates.
- Use **parameterization** (e.g., `logical_date`) so the pipeline could support backfills.
- Implement reasonable **error handling and retries**.
- Use the provided `MockDatabricksSubmitRunOperator` (in `plugins/operators/mock_databricks.py`) for at least one task. You can also use `PythonOperator`, `BashOperator`, or any other standard operator.

**Transformation logic:** Write it as local Python scripts (in `scripts/` or inline). No real Databricks cluster is needed — the mock operator runs your script locally. PySpark is available in `requirements.txt` if you prefer it.

### 2. Infrastructure-as-Code / Deployment — *Required*

In the `infra/` directory, provide configuration that shows how you'd deploy this pipeline beyond local dev. Choose at least one:

- **Terraform** config for provisioning Airflow and/or Databricks resources (can be a realistic skeleton — it doesn't need to `apply`).
- **Docker / Kubernetes** manifests for running Airflow in a more production-like setup.
- **CI/CD pipeline** config (GitHub Actions, GitLab CI, etc.) that would lint, test, and deploy the DAGs.

This doesn't need to be runnable — we want to see that you understand what production deployment looks like.

### 3. Design Document — *Required*

Write a 1–2 page design doc in `docs/` (Markdown is fine) that includes:

- An **architecture diagram** (ASCII art, Mermaid, or an image) showing how data flows through the layers of your pipeline.
- **Key design decisions** and the trade-offs you considered.
- Your **data quality strategy** — what checks run, where in the pipeline, and what happens when they fail.
- How you handle **schema evolution** — both the v1/v2 reconciliation and your approach to future schema changes.
- What you'd do differently with **real Databricks access** and a production workload.
- How you'd add **monitoring and alerting** — if this pipeline fails at 3 AM, how would the team know and how would they recover?

### 4. Data Catalog / Lineage Manifest — *Required*

Provide a data catalog or lineage manifest in `docs/` (YAML, JSON, or Markdown) that documents each table or dataset in your pipeline:

- Schema (column names and types)
- Upstream source(s)
- Transformation logic summary
- Freshness SLA or update frequency
- Data quality rules applied

This could be a simple hand-crafted YAML file, or you could propose integration with tools like Great Expectations, dbt docs, or OpenMetadata. We care more about the thinking than the tool choice.

### 5. Tests — *Encouraged*

Add tests in `tests/`. At minimum, a couple of unit tests for your transformation logic. We've included `pytest` in the requirements.

### 6. README Updates — *Required*

Update this README (or add a separate one) with:
- How to run your pipeline locally.
- Any assumptions you made.
- What you'd improve with more time.

---

## Repo Structure

```
.
├── README.md                 ← You are here
├── docker-compose.yml        ← Local Airflow environment (provided)
├── Dockerfile                ← Custom Airflow image (provided)
├── requirements.txt          ← Python dependencies (provided)
├── .env.example              ← Environment variable template
├── dags/
│   └── example_dag.py        ← Smoke-test DAG (provided, do not modify)
├── plugins/
│   └── operators/
│       └── mock_databricks.py  ← Mock Databricks operator (provided)
├── data/
│   ├── raw/                  ← Seed data (provided)
│   │   ├── orders.csv           (v1 schema — may contain quality issues)
│   │   ├── orders_v2_sample.csv (v2 schema — new format being rolled out)
│   │   └── products.json
│   └── output/               ← Your pipeline writes results here
├── scripts/                  ← Place your transformation scripts here
├── tests/
│   └── test_example.py       ← Example test (provided)
├── infra/                    ← Your IaC / deployment config goes here
├── docs/                     ← Your design doc + data catalog go here
└── config/                   ← Any additional config files
```

---

## Environment Details

| Component | Version / Detail |
|---|---|
| Airflow | 3.0.1 |
| Python | 3.12 |
| Executor | LocalExecutor (Postgres backend) |
| PySpark | 3.5.4 (available but optional) |
| Airflow UI | http://localhost:8080 (admin / admin) |
| Postgres | 15 on port 5432 |

**Airflow 3.0 notes:** This repo uses Airflow 3.0, which has architectural differences from 2.x. The webserver is now the `api-server`, DAG processing runs as a separate `dag-processor` service, and the standard operators (e.g., `PythonOperator`) live in `airflow.providers.standard`. Custom operators should extend `airflow.sdk.BaseOperator`. Context variables like `execution_date` have been removed — use `logical_date` or `data_interval_start`/`data_interval_end` instead.

**Environment variables** available inside the Airflow containers:

| Variable | Value |
|---|---|
| `RAW_DATA_PATH` | `/opt/airflow/data/raw` |
| `OUTPUT_DATA_PATH` | `/opt/airflow/data/output` |
| `DATABRICKS_HOST` | `http://mock-databricks:9999` |
| `DATABRICKS_TOKEN` | `mock-token-for-local-dev` |

---

## Hints & Guidelines

- **Explore the data before building.** Don't assume it's clean. Part of this exercise is discovering what's wrong and deciding how to handle it.
- **Think in layers.** Good data architectures separate ingestion, cleaning, and analytical concerns. Show us that separation in your DAG design and code structure.
- **The schema change is intentional.** Show us how you'd handle it as a recurring operational reality, not a one-off hack. What happens when v3 arrives next month?
- **For the data catalog**, we value clarity and completeness over tooling sophistication. A well-thought-out YAML file is better than a half-implemented framework integration.
- **Use the mock operator** for at least one task — it shows you understand the Databricks integration pattern.
- **Idempotency matters.** Think about what happens when the DAG is re-triggered for the same logical date.
- **Don't over-engineer** the IaC — a realistic skeleton with comments explaining what each resource does is sufficient.
- **Scope it right.** A clean, well-tested pipeline with a thoughtful design doc beats a sprawling implementation. See the prioritization guidance above.

---

## Submission

1. Push your work to a private GitHub repo and invite Jimmy Lien (@jlien) and Trent Seigfried (@trents).
2. Make sure `docker-compose up --build` still works with your changes.
3. Ensure we can trigger your DAG(s) from the Airflow UI and see results in `data/output/`.

Good luck — we're looking forward to seeing your approach!
