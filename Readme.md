# BP Apple Checker

BP Apple Checker is a Python script that checks the availability of iPhone models in Apple stores and sends notifications using Pushover. It also provides a simple web UI to display the results of the last run and the frequency at which the script runs.

## Features

- Checks iPhone availability in specified Apple stores.
- Sends notifications using Pushover.
- Provides a web UI to display the results of the last run.
- Configurable frequency for running the script.

## Requirements

- Python 3.6+
- Docker

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/binuengoor/bp-apple-checker.git
   cd bp-apple-checker
   ```
## Installation

2. **Install Python dependencies**:
   `pip install -r requirements.txt`

3. **Set up environment variables**:
   Create a `.env` file in the project directory with the following content:
   ```sh
   FREQUENCY=5
   PUSHOVER_USER_KEY=your_user_key
   PUSHOVER_API_TOKEN=your_api_token
   ```

4. **Run the script**:
   `python main.py`

## Docker

You can also run the script using Docker.

1. **Build the Docker image**:
   `docker build -t iphone-checker .`

2. **Run the Docker container**:
   `docker run -e FREQUENCY=5 -e PUSHOVER_USER_KEY=your_user_key -e PUSHOVER_API_TOKEN=your_api_token -p 3767:3767 iphone-checker`

Replace `your_user_key` and `your_api_token` with your actual Pushover user key and API token. The `FREQUENCY` environment variable can be adjusted to change the interval at which the script runs.

## Docker Compose

You can also use Docker Compose to manage and run the application.

1. **Copy the `docker-compose.yml` file and update env variables.

2. **Build and run the services**:
   docker-compose up --build

3. **Access the web UI**:
   Open your browser and go to `http://localhost:3767` to see the results of the last run and the frequency at which the script runs. The page will refresh every 10 seconds.

## Usage

- Access the web UI at `http://localhost:3767` to see the results of the last run and the frequency at which the script runs. The page will refresh every 10 seconds.
- The notification message will be displayed at the top of the results. If no models are found, the message will be displayed in red; otherwise, it will be displayed in green.

## Configuration

- **COUNTRIES**: Update the COUNTRIES dictionary in main.py to add or modify the countries and their store paths and SKU codes.
- **SKUs and Favorites**: Update the `skus_for_country` and `favourites_for_country` functions in main.py to add or modify the SKUs and favorites for each country.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

