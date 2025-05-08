# cis6930sp25(Data Engineering)-project3

## Name:
Abhinava Sai Tirunagari

## Project Description
This project implements a Python package that consumes UFO sighting messages from a RabbitMQ broker, classifies each sighting using a RandomForest machine learning model, and visualizes the classified sightings live on a Streamlit dashboard.

The project supports:
- Local execution using UV
- Containerized execution using Apptainer
- Message publishing via a test script (`send_message.py`) to RabbitMQ

The RabbitMQ server is set up locally using Docker.

---

## How to Install (UV Installation)

## Demo Video

You can view the walkthrough video [here](https://drive.google.com/file/d/1daLyBjTobclPJ1Z85rHLMbd6u9T7dnVL/view?usp=sharing).

### 1. Install UV
If you don't have UV installed:
```
pip install uv
```
## How to Run Locally Using UV
### 1. Install Dependencies

Inside the project root directory (where pyproject.toml exists), run:
```
uv pip install .
```
This will install:

- pika (for RabbitMQ)

- pandas (for data handling)

- scikit-learn (for machine learning classification)

- streamlit (for dashboard visualization)

- loguru (for structured logging)

### 2. Set Up a Local RabbitMQ Server Using Docker
Run the following command to start RabbitMQ with management UI:
```
docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

### 3. Create the ufo Exchange
- Go to http://localhost:15672

- Login with:

    - Username: guest

    - Password: guest

- Navigate to Exchanges → Add a New Exchange:

    - Name: ufo

    - Type: fanout

    - Durable: checked

- Click Add Exchange

### 4. Run the Streamlit Dashboard Locally
```
python main.py
```
The dashboard will be available at:
```
http://localhost:8501
```
### 5. Send Test UFO Messages Using send_message.py
In a second terminal, run:
```
python send_message.py
```
This will publish 10 randomly generated UFO sighting messages to the ufo exchange.

You should immediately see the classified messages appear on the dashboard!

## How to Build and Run Using Apptainer

### 1. Build the Apptainer Container
Inside the project root (output/ folder), run:
```
apptainer build edad.sif apptainer.def
```

### 2. Run the Containerized Dashboard
Make sure your RabbitMQ server is running (via Docker, as shown above).  
Then run:
```
apptainer run --env COMMAND=localhost --env PORT=5672 edad.sif
```
- `COMMAND=localhost` → RabbitMQ server address

- `PORT=5672` → RabbitMQ server port
The dashboard will again be available at:
```
http://localhost:8501
```
You can still send messages by:
```
python send_message.py
```

## Features and Functions

### main.py
- Parses RabbitMQ host and port from environment variables.
- Launches Streamlit dashboard.

### src/classifier.py
- Trains a RandomForestClassifier on synthetic UFO sighting data.
- Predicts whether a sighting is alien communication.

### src/consumer.py
- Connects to RabbitMQ.
- Subscribes to `ufo` fanout exchange.
- Consumes, classifies, and stores messages for visualization.

### src/dashboard.py
- Streamlit app that:
  - Displays classified sightings in a table.
  - Maps sightings based on latitude and longitude.
  - Visualizes prediction and shape distributions.

### send_message.py
- Publishes random UFO sightings to RabbitMQ for testing.

## How to Run Test Cases

### Running Tests Locally Using UV

Install pytest:

```bash
uv pip install pytest
```

Then run:

```bash
pytest tests/
```

This will discover and execute all unit tests inside the `tests/` folder.

---

## Running Tests Inside the Apptainer Container

Open an interactive shell inside the container:

```bash
apptainer shell edad.sif
```

Inside the container, run:

```bash
pytest /app/tests/
```
This will run all tests inside `/app/tests/`.

Exit the container:

```bash
exit
```

## Test Cases - Functionalities

### tests/test_classifier.py
- Tests that `SightingClassifier.predict()` returns only 0 or 1 for a valid sighting message.

### tests/test_consumer.py
- Tests that `SightingConsumer.parse_message()` parses valid JSON correctly.
- Tests that it safely handles invalid (non-JSON) input.

### tests/test_classifier_edge_cases.py
- Tests classifier behavior when required fields are missing.
- Tests behavior when input is completely empty.


## Bugs and Assumptions

- **RabbitMQ Real-time Behavior**: Fanout exchange requires the consumer to be active when publishing messages; otherwise, messages are lost.
- **Simple Machine Learning Model**: The RandomForest model is trained on a small synthetic dataset and is not meant for production.
- **Apptainer Limitations**: Ensure that ports (like 8501) are accessible if running containers in restricted environments.
- **Hardcoded Exchange**: The system listens specifically for the `ufo` exchange and expects sighting messages in a defined JSON format.
