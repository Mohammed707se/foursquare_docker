🚀 How to Run with Docker
1️⃣ Build the Docker Image:
```
docker build -t foursquare-scraper .
```

2️⃣ Run the Scraper:
```
docker run --rm -v $(pwd)/data:/app/data foursquare-scraper "01-02-2024"
```
📌 Replace "01-02-2024" with your desired date (DD-MM-YYYY).

📂 Output
The scraped data will be saved as a CSV file inside the data/ folder.
Example file:

data/foursquare_data_20240201.csv
