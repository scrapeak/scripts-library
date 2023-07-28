# Import necessary libraries
import requests
import pandas as pd

# Set default headers for the HTTP requests
defaultHeaders = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"}

# API URL for the scraping service
apiUrl = "https://app.scrapeak.com/v1/scrapers/zillow/property"

# Replace "YOUR-API-KEY" with your actual API key
apiKey = "YOUR-API-KEY" # CHANGE WITH YOUR API KEY

# Zillow Property ZPID (Zillow Property ID) to scrape data for
propertyZPID = "66288024"

# Parameters for the API request
querystring = {
  "api_key": apiKey,
  "zpid": propertyZPID,
}

# Make a GET request to the API with the specified parameters
response = requests.request("GET", apiUrl, params=querystring, headers=defaultHeaders)

# Get the content of the response
responseContent = response.text

# Print the response content
print(responseContent)

# Convert the JSON response to a Pandas DataFrame and normalize it
df_listings = pd.json_normalize(response.json()["data"])

# Save the DataFrame to a CSV file named "scrapeak_property.csv"
df_listings.to_csv("scrapeak_property.csv")
