# Import necessary libraries
import requests
import pandas as pd

# Set default headers for the HTTP requests
defaultHeaders = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"}

# API URL for the scraping service
apiUrl = "https://app.scrapeak.com/v1/scrapers/zillow/listing"

# Replace "YOUR-API-KEY" with your actual API key
apiKey = "YOUR-API-KEY"

# The URL of the listing page with the 'searchQueryState' parameter for Zillow recently sold homes in Norfolk, VA
listingURL = "https://www.zillow.com/homes/recently_sold/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Norfolk%2C%20VA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-79.49477267730734%2C%22east%22%3A-73.16115451324484%2C%22south%22%3A35.07342513156661%2C%22north%22%3A38.752616100018315%7D%2C%22mapZoom%22%3A8%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22beds%22%3A%7B%22min%22%3A2%7D%2C%22baths%22%3A%7B%22min%22%3A1%7D%2C%22sqft%22%3A%7B%22max%22%3A2500%2C%22min%22%3A750%7D%2C%22built%22%3A%7B%22max%22%3A1990%7D%2C%22price%22%3A%7B%22max%22%3A1000000%7D%2C%22doz%22%3A%7B%22value%22%3A%2212m%22%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22att%22%3A%7B%22value%22%3A%22renovated%22%7D%2C%22mp%22%3A%7B%22max%22%3A5234%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22rs%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D" 

# Parameters for the API request
querystring = {
  "api_key": apiKey,
  "url": listingURL,
}

# Make a GET request to the API with the specified parameters
response = requests.request("GET", apiUrl, params=querystring, headers=defaultHeaders)

# Get the content of the response
responseContent = response.text

# Print the response content
print(responseContent)

# Convert the JSON response to a Pandas DataFrame and normalize it
df_listings = pd.json_normalize(response.json()["data"]["cat1"]["searchResults"]["listResults"])

# Save the DataFrame to a CSV file named "scraped_list.csv"
df_listings.to_csv("scraped_list.csv")
