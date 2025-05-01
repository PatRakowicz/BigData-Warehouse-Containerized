# BigData Warehouse & Recession Classifier

This project is a Dockerized big data pipeline that:
- Fetches U.S. economic indicators from the Federal Reserve's FRED API
- Loads structured data into a MySQL data warehouse
- Trains a machine learning model to classify time periods as recession or not based on historical economic data

It consists of three main containers:
- `mysql` → stores the economic data
- `etl` → fetches and loads FRED data into the database
- `ml` → trains and evaluates a recession classification model

---

## Project Structure

```
fred_etl_project/
docker-compose.yml
.env                   # contains FRED_API_KEY
database/
    init.sql           # sets up the MySQL schema for fred_data
etl/
    Dockerfile
    etl_script.py      # fetches FRED indicators and inserts into MySQL
ml/
    Dockerfile
    ml_train.py        # loads data from MySQL and trains a RandomForest classifier that predicts recession
```

---

## What It Does

### ETL Container (`etl`)

- Uses the FRED API to download these indicators:
  - GDP
  - CPI (Inflation)
  - UNRATE (Unemployment)
  - FEDFUNDS (Interest Rate)
  - RSXFS (Retail Sales)
  - INDPRO (Industrial Production)
  - PI (Personal Income)
  - USRECM (Recession Indicator)
- Pushes clean, labeled data into the `fred_data` table in MySQL.

### ML Container (`ml`)

- Reads historical indicators from MySQL
- Pivots the data and creates lag features
- Trains a `RandomForestClassifier` to predict when or if there will be a recession in 3 months
- Outputs persentage of unemplyment and a value that displays 1 or 0, 1 being we will have a unenployment

---

## How to Use

### 1. Clone the project

```bash
git clone (this repository)
cd fred-etl-project
```

### 2. Set up your `.env` file

Create a `.env` file in the root of the project with your FRED API key:

```env
FRED_API_KEY=your_fred_api_key_here
```

### 3. Build and run everything

```bash
docker-compose up --build -d (if you want detached consol)
```

This will:

- Start MySQL and initialize the database
- Run the ETL container to fetch and store FRED data
- Run the ML container to train and evaluate the classifier

### 4. View ML Output

Run this to see the machine learning results:

```bash
docker-compose logs ml
```

You’ll see output like:

```
=== Confusion Matrix ===
[[32 0]
 [ 1 0]]

=== Classification Report ===
precision recall f1-score support
...
```

---

## Developer Commands

| Task                           | Command                         |
| ------------------------------ | ------------------------------- |
| Run only the ETL container     | `docker-compose up --build etl` |
| Run only the ML container      | `docker-compose up --build ml`  |
| Stop and remove all containers | `docker-compose down`           |
| Wipe database & volumes        | `docker-compose down -v`        |
| View logs for all containers   | `docker-compose logs`           |
