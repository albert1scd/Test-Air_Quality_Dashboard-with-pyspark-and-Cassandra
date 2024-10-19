# Test-Air_Quality_Dashboard-with-pyspark-and-Cassandra


This project demonstrates the integration of FastAPI and PySpark to create a simple API that processes data using Spark.

## Features

- FastAPI web server
- PySpark data processing
- Simple API endpoint to calculate average age by city

## Prerequisites

- Python 3.7+
- pip
- Java 8+ (required for PySpark)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/fastapi-pyspark-project.git
   cd fastapi-pyspark-project
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the application

1. Start the FastAPI server:
   ```
   uvicorn app.main:app --reload
   ```

2. Open your browser and go to `http://localhost:8000/docs` to see the Swagger UI documentation and test the API.

## API Endpoints

- `GET /`: Welcome message
- `GET /average-age/{city}`: Get the average age for a specific city

## Running tests

To run tests, use the following command:
```
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
