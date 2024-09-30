import os
import requests
import json
import schedule
import time
from datetime import datetime
from urllib.parse import quote
import sys
from flask import Flask, render_template_string
import pytz
from datetime import datetime

app = Flask(__name__)

COUNTRIES = {
    "US": {
        "storePath": "",
        "skuCode": "LL"
    }
}

def skus_for_country(country_sku_code):
    return {
        "MYW63LL/A": "iPhone 16 Pro Max 256GB Natural Titanium",
        "MYW33LL/A": "iPhone 16 Pro Max 256GB Black Titanium",
        #"MYAQ3LL/A": "iPhone 16 128GB White", 
        # "MTMN3VC/A": "Testingggg",
    }

def favourites_for_country(country_sku_code):
    return [
        "MYW63LL/A",
        "MYW33LL/A",
    ]

last_run_results = ""
notification_message = ""
frequency = int(os.getenv("FREQUENCY", 5))  # Default to 5 minutes if not set


def check_inventory():
    global last_run_results, notification_message
    control = "MYW63LL/A"
    store_number = os.getenv('STORE_NUMBER',"R102")
    search_nearby = os.getenv("SEARCH_NEARBY", "false")
    country = "US"

    args = sys.argv[1:]

    if args:
        passed_store = args[0]
        country = (args[1] if len(args) > 1 else "US").upper()
        if passed_store.startswith("R"):
            store_number = passed_store

    country_config = COUNTRIES[country]
    store_path = country_config["storePath"]
    sku_list = skus_for_country(country_config["skuCode"])
    favorites = favourites_for_country(country_config["skuCode"])

    query = "&".join([f'parts.{i}={quote(k)}' for i, k in enumerate(sku_list.keys())]) + f"&searchNearby={search_nearby}&store={store_number}"

    url = f"https://www.apple.com{store_path}/shop/fulfillment-messages?{query}"

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error: Received status code {response.status_code}")

    body = response.json()
    stores_array = body['body']['content']['pickupMessage']['stores']
    sku_counter = {}
    has_store_search_error = False

    results = []
    status_array = []

    for store in stores_array:
        name = store['storeName']
        product_status = []

        for key, value in sku_list.items():
            product = store['partsAvailability'][key]

            has_store_search_error = product.get('storeSearchEnabled', False) != True

            if key == control and not has_store_search_error:
                has_store_search_error = product.get('pickupDisplay', 'unavailable') != "available"
            else:
                product_status.append(f"{value}: {product.get('pickupDisplay', 'unavailable')}")

                if product.get('pickupDisplay', 'unavailable') == "available":
                    results.append(f"{value} in stock at {store['storeName']}")
                    count = sku_counter.get(key, 0)
                    count += 1
                    sku_counter[key] = count

        status_array.append({
            "name": name,
            "products": product_status,
        })

    has_error = has_store_search_error

    inventory = " | ".join([f"{sku_list[key]}: {value}" for key, value in sku_counter.items()])

    results.append('\nInventory counts')
    results.append('----------------')
    results.append(inventory.replace(" | ", "\n"))

    results.append('Status Array')
    results.append('------------')
    for store in status_array:
        results.append(f"<b>Store: {store['name']}</b>")
        for product in store['products']:
            results.append(f"  {product}")

    notification_message = "No models found."
    if inventory:
        has_ultimate = any(r in favorites for r in sku_counter.keys())
        notification_message = f"{'FOUND iPhone! ' if has_ultimate else ''}Some models found: {inventory}"

    color = "red" if notification_message == "No models found." else "green"
    results.insert(0, f"<h3 style='color: {color};'>{notification_message}</h3>")

    message = notification_message

    if message != "No models found.":
        # Pushover notification
        user_key = os.getenv("PUSHOVER_USER_KEY")
        api_token = os.getenv("PUSHOVER_API_TOKEN")
        pushover_url = "https://api.pushover.net/1/messages.json"
        pushover_data = {
            "token": api_token,
            "user": user_key,
            "message": message,
            "title": "iPhone Availability",
            "sound": "pushover",
        }
        response = requests.post(pushover_url, data=pushover_data)
        if response.status_code == 200:
            results.append("Pushover notification sent successfully.")
        else:
            results.append(f"Failed to send Pushover notification: {response.status_code}")

    eastern = pytz.timezone('US/Eastern')
    current_time = datetime.now(eastern).astimezone(eastern).strftime('%Y-%m-%d %H:%M:%S %Z%z')
    results.append(f"\nGenerated: {current_time}")

    last_run_results = "\n".join(results)

# Schedule the job
schedule.every(frequency).minutes.do(check_inventory)

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
            <meta http-equiv="refresh" content="10">
            <title>iPhone Inventory Checker</title>
        </head>
        <body>
            <h1>iPhone Inventory Checker</h1>
            <p>This script runs every {{ frequency }} minutes.</p>
            <h2>Last Run Results</h2>
            <pre>{{ last_run_results|safe }}</pre>
        </body>
        </html>
    ''', frequency=frequency, last_run_results=last_run_results)

if __name__ == '__main__':
    # Run the inventory check once before starting the Flask server
    check_inventory()

    # Start the Flask web server in a separate thread
    from threading import Thread
    def run_flask():
        app.run(host='0.0.0.0', port=3767)

    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Run the scheduled job
    while True:
        schedule.run_pending()
        time.sleep(1)