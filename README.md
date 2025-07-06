# 🛠️ Cost-Efficient ETL Pipeline with CI/CD, Validation & Monitoring

A production-style ETL pipeline that ingests, cleans, validates, and loads **Brazil E-Commerce** data using **Python, Airflow, PostgreSQL, Great Expectations, Docker, and GitHub Actions** — all without relying on paid tools or bloated stacks.

## 📦 Project Stack

| Layer         | Tech Used                            |
|---------------|--------------------------------------|
| Orchestration | Apache Airflow (via Docker)          |
| Processing    | Python (Pandas, SQLAlchemy)          |
| Validation    | Great Expectations                   |
| Storage       | PostgreSQL (Dockerized)              |
| Monitoring    | Logging + Airflow DAG alerting       |
| CI/CD         | GitHub Actions + Pytest              |
| Config Mgmt   | YAML (`config/config.yml`) for dataset ↔ table mapping |

## 📈 Key Features

✅ **ETL Pipeline**  
- Modular and reusable cleaners for each CSV dataset  
- Loads data into PostgreSQL using SQLAlchemy  
- Config-driven with `.env` + YAML support  
- Logs row counts and execution time  

✅ **Data Validation with Great Expectations**  
- Expectations configured per dataset  
- Validated automatically via Airflow  
- Dynamic Postgres datasource setup  
- Fails loudly if expectations aren’t met  

✅ **Monitoring (No Grafana Needed)**  
- ETL writes structured logs (`logs/etl.log`)  
- Airflow DAG scans logs daily for failures or zero rows  
- Optional Grafana/Prometheus config available in `monitoring/`  

✅ **CI/CD with GitHub Actions**  
- Runs `pytest` for unit tests  
- Executes Great Expectations validations  
- Easy to extend for deployment or DAG sync  

## 🧪 Sample Unit Test

```python
def test_customers_schema():
    df = pd.read_csv("data/raw/olist_customers_dataset.csv")
    df_clean = clean_customers(df)
    assert "customer_id" in df_clean.columns
    assert not df_clean.isnull().any().any()
```

> Tests for schema, nulls, row counts, and cleaner coverage are all included in `tests/`

## 🐳 Docker Customisations

- `docker/dockerfile.airflow` extends the base Airflow image to include:
  - `dbt-core==1.7.9`
  - `dbt-postgres==1.7.9`
- Keeps orchestration, transformation, and validation unified inside the Airflow container

## 📁 Folder Structure

```
.
├── config/                      ← Global YAML configs + dbt profiles
│   └── config.yml
├── dags/                        ← Airflow DAGs
├── data/                        ← Raw CSVs (not committed)
├── dbt_project/                 ← dbt models & project files
├── docker/                      ← Custom Dockerfiles
├── gx/                          ← Great Expectations suite
├── logs/                        ← ETL & validation logs
├── monitoring/                  ← (Optional) Prometheus & Grafana configs
├── src/                         ← Pipeline code
│   └── etl/                     ← ETL runners & cleaners
│   └── validation/              ← GE checkpoint runner
├── tests/                       ← Pytest unit tests
├── .github/workflows/ci.yml     ← CI pipeline
├── docker-compose.yml           ← Dev stack launcher
└── requirements.txt
```

## 📊 Data Source

This project uses the [Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), which includes customer, order, product, seller, and geolocation data.

## 🚀 How to Run Locally

```bash
# Clone the repo
git clone https://github.com/your-username/cost-efficient-etl-pipeline.git
cd cost-efficient-etl-pipeline

# Launch all services
docker-compose up --build

# Open Airflow at: http://localhost:8080
```

## 🧪 Run Tests Locally

```bash
# In your local environment (not container)
pip install -r requirements.txt
pytest tests/
```

## ✅ CI/CD via GitHub Actions

The [`.github/workflows/ci.yml`](.github/workflows/ci.yml) file automatically runs on every `push` and `pull_request` to `main`:

- ✅ **Code Quality** — Linting with [`ruff`](https://github.com/astral-sh/ruff), a fast Python linter  
- ✅ **Unit Tests** — Runs `pytest` with coverage on the ETL pipeline  
- ✅ **Validation** — Executes Great Expectations checkpoints on actual datasets  
- ✅ **Isolated Environment** — Uses a service container for PostgreSQL  
- ✅ **Fail Fast** — Pipeline fails early on data/schema/test issues  





