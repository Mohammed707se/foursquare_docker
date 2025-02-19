from datetime import datetime
import requests
import csv
import sys
import os
import json

if len(sys.argv) < 2:
    print("Usage: python scraper.py <date in format DD-MM-YYYY>")
    sys.exit(1)

# استلام التاريخ وتحويله إلى الصيغة الصحيحة YYYYMMDD
try:
    input_date = sys.argv[1]
    formatted_date = datetime.strptime(input_date, "%d-%m-%Y").strftime("%Y%m%d")
except ValueError:
    print("Error: Incorrect date format. Use DD-MM-YYYY (e.g., 01-02-2024)")
    sys.exit(1)

API_URL = "https://api.foursquare.com/v2/search/recommendations"
params = {
    "locale": "en",
    "explicit-lang": "false",
    "v": formatted_date,  
    "m": "foursquare",
    "limit": 30,
    "offset": 30,
    "intent": "bestnearby",
    "sw": "24.733423426410056,46.64475202560425",
    "ne": "24.746909246928627,46.697280406951904",
    "wsid": "IAIBKEZPWFF3IOD4W31VVBCFTTSKV0",
    "oauth_token": "QEJ4AQPTMMNB413HGNZ5YDMJSHTOHZHMLZCAQCCLXIX41OMP",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.7",
    "Origin": "https://foursquare.com",
    "Referer": "https://foursquare.com/",
    "Sec-Ch-Ua": '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Sec-GPC": "1"
}

def fetch_foursquare_data():
    """ جلب البيانات من API فور سكوير """
    response = requests.get(API_URL, params=params, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Failed to fetch data. Status Code: {response.status_code}")
        return []

    try:
        data = response.json()
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON response.")
        return []

    places = data.get("response", {}).get("group", {}).get("results", [])

    return places

def save_to_csv(data, date):
    os.makedirs("data", exist_ok=True)

    file_path = f"data/foursquare_data_{date}.csv"

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["#", "Name", "Category", "Latitude", "Longitude", "Address", "Rating"])

        for idx, place in enumerate(data, start=1):
            venue = place.get("venue", {})
            name = venue.get("name", "N/A")
            category = venue.get("categories", [{}])[0].get("name", "N/A")
            lat = venue.get("location", {}).get("lat", "N/A")
            lng = venue.get("location", {}).get("lng", "N/A")
            address = " - ".join(venue.get("location", {}).get("formattedAddress", []))
            rating = venue.get("rating", "N/A")

            writer.writerow([idx, name, category, lat, lng, address, rating])

    print(f"✅ Data saved successfully to {file_path}")

if __name__ == "__main__":
    data = fetch_foursquare_data()
    if data:
        save_to_csv(data, formatted_date)
        print("✅ Scraping completed. Exiting...")
    else:
        print("⚠️ No data found. Exiting...")
    
    sys.exit(0)
