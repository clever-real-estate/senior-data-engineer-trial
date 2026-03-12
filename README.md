# Senior Data Architecture Engineer — Take-Home Assignment

## Quick Start

```bash
# 1. Clone and enter the repo
git clone <repo-url> && cd senior-da-engineer-trial

# 2. Copy the environment file
cp .env.example .env

# 3. Start the local Airflow environment
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

You're joining a data engineering team that uses **Apache Airflow** for orchestration and **Databricks** for compute and transformations. Your first project is to build a small but production-quality data pipeline for the company's e-commerce analytics platform.

**The data:**

| File | Location | Description |
|---|---|---|
| `orders.csv` | `data/raw/` | 5,000 e-commerce orders spanning 90 days with order ID, customer, product, quantity, price, date, status, and country |
| `products.json` | `data/raw/` | Product catalog with 15 products across 2 categories and 6 subcategories, including cost price and weight |

**The business goal:** Produce a daily summary of order activity that the analytics team can query. Specifically:

1. **Ingest** the raw order and product data from the landing zone (`data/raw/`).
2. **Transform** the data — join orders with products, compute line-item totals and profit margins, and filter to only completed orders.
3. **Aggregate** into a daily summary: revenue, cost, profit, and order count per product per day.
4. **Land** the results in `data/output/` as Parquet (preferred) or CSV.

---

## What We're Asking You to Build

Complete as much as you can in **2–3 hours**. We value quality and thoughtfulness over completeness — a well-designed partial solution is better than a rushed end-to-end one.

### 1. Airflow DAG(s) — *Required*

Design and implement one or more DAGs in the `dags/` directory that orchestrate the pipeline described above.

**Expectations:**
- Model task dependencies cleanly (don't put everything in one giant task).
- Make the pipeline **idempotent** — re-running for the same date shouldn't produce duplicates or corrupt data.
- Use **parameterization** (e.g., execution date) so the pipeline could support backfills.
- Implement reasonable **error handling and retries**.
- Use the provided `MockDatabricksSubmitRunOperator` (in `plugins/operators/mock_databricks.py`) for at least one task to show how you'd integrate with Databricks in production. You can also use `PythonOperator`, `BashOperator`, or any other standard operator.

**What about the actual transformation logic?** Write it as local Python scripts (in `scripts/` or inline). No real Databricks cluster is needed. The mock operator will run your script locally. If you prefer, you can use PySpark locally — PySpark is included in `requirements.txt`.

### 2. Infrastructure-as-Code / Deployment — *Required*

In the `infra/` directory, provide configuration that shows how you'd deploy this pipeline beyond local dev. Choose at least one:

- **Terraform** config for provisioning Airflow and/or Databricks resources (can be a realistic skeleton — it doesn't need to `apply`).
- **Docker / Kubernetes** manifests for running Airflow in a more production-like setup.
- **CI/CD pipeline** config (GitHub Actions, GitLab CI, etc.) that would lint, test, and deploy the DAGs.

This doesn't need to be runnable — we want to see that you understand what production deployment looks like.

### 3. Design Document — *Required*

Write a 1–2 page design doc in `docs/` (Markdown is fine) that includes:

- An **architecture diagram** (ASCII art, Mermaid, or an image) showing how data flows through the pipeline.
- **Key design decisions** and the trade-offs you considered.
- How you'd handle **late-arriving data** or schema changes.
- What you'd do differently with **real Databricks access** and a production workload.

### 4. Tests — *Encouraged*

Add tests in `tests/`. At minimum, a couple of unit tests for your transformation logic. We've included `pytest` in the requirements.

### 5. README Updates — *Required*

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
│   │   ├── orders.csv
│   │   └── products.json
│   └── output/               ← Your pipeline writes results here
├── scripts/
│   └── generate_data.py      ← Optional: generate more test data
├── tests/
│   └── test_example.py       ← Example test (provided)
├── infra/                    ← Your IaC / deployment config goes here
├── docs/                     ← Your design doc goes here
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

- **Scope it right.** We'd rather see a clean, well-tested pipeline for the core scenario than a sprawling implementation. If you're running out of time, prioritize the DAG design and design doc.
- **Show your thinking.** Comments, docstrings, and the design doc are where you can demonstrate senior-level judgment.
- **Use the mock operator.** Even if it's just for one task, it shows you understand the Databricks integration pattern.
- **Idempotency matters.** Think about what happens when the DAG is re-triggered for the same logical date.
- **Don't over-engineer** the IaC — a realistic skeleton with comments explaining what each resource does is sufficient.

---

## Submission

1. Push your work to a private GitHub repo and invite Jimmy Lien (@jlien) and Trent Seigfried (@trents).
2. Make sure `docker-compose up --build` still works with your changes.
3. Ensure we can trigger your DAG(s) from the Airflow UI and see results in `data/output/`.

Good luck — we're looking forward to seeing your approach!
