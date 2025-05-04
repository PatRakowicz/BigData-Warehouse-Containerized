# BigData Warehouse & Recession Classifier
**Time Spent (h)**:
- **4**: General idea was a bit hard on how i could do this. Was a little stuck on getting the needed containers, attempted to do either visuals (time might be out of the question) or some sort of Machine Learning idea.
- **5**: Coding and applying the application was some what straight forward, got a little lost on the ML side of python. Honestly should have done visuals, something very simple, like web page with a table and just show the data from the SQL container. Docker was interesting to figure out, they have great documentation. I have experimented with docker-compose for a little while here. Did figure out that you can run multiple applications off one docker-compose file. Allowing for one file to handle all the containers and witch run at what moment. It will not always start correctly, you might have to run the SQL first and then ETL and then you can run your model off the data from the SQL container.

Dockerized big data pipeline:
- Fetches U.S. economic indicators from the Federal Reserve's FRED API.
- Loads structured data into a MySQL data warehouse.
- Trains a machine learning model to predict unenployment rates in a given span of 3 months.

It consists of three main containers:
- `mysql` → stores the economic data
- `etl` → fetches and loads FRED data into the database
- `ml` → trains and evaluates a classification model

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
    ml_train.py        # loads data from MySQL and trains a RandomForest classifier
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
- Trains a `RandomForestClassifier` to predict unenployment rates in a given span of 3 months.
- It will give two scores that will display what persentage we are at and a if 1 we are in a high unenployement 0 if not.
- IE. get something like 0.09 stating we are really low.

---

## How to Use
_Make sure you have some sort of docker applicaion installed and working on your machine. This can either be DockerDesktop or Docker CLI.
Run a hello wolrd container to test things._
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
Then it should display what the current application in the container is doing.
---

## Developer Commands

| Task                           | Command                         |
| ------------------------------ | ------------------------------- |
| Launch all containers          | `docker-compose up --build -d`  | 
| Run only the ETL container     | `docker-compose up --build etl` |
| Run only the ML container      | `docker-compose up --build ml`  |
| Stop and remove all containers | `docker-compose down`           |
| Wipe database & volumes        | `docker-compose down -v`        |
| View logs for all containers   | `docker-compose logs`           |
