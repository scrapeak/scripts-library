# Import necessary libraries
from urllib import parse
import pandas as pd
import requests, json
import time

# Comments for Steps in the process
"""
Steps:
1- Set the listing url
2- Run the createPriceChunks if you don't have price range list
3- Set priceChunkTaskId and Get price range list 
4- And then start the scraper
"""

# Set the desired settings for Pandas display
pd.set_option("display.max_columns", None)

# Replace "YOUR-API-KEY" with your actual API key
api_key = "YOUR-API-KEY"

# Set the URL for the listing page you want to scrape
listing_url = "https://www.zillow.com/homes/recently_sold/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Norfolk%2C%20VA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-79.49477267730734%2C%22east%22%3A-73.16115451324484%2C%22south%22%3A35.07342513156661%2C%22north%22%3A38.752616100018315%7D%2C%22mapZoom%22%3A8%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22beds%22%3A%7B%22min%22%3A2%7D%2C%22baths%22%3A%7B%22min%22%3A1%7D%2C%22sqft%22%3A%7B%22max%22%3A2500%2C%22min%22%3A750%7D%2C%22built%22%3A%7B%22max%22%3A1990%7D%2C%22price%22%3A%7B%22max%22%3A1000000%7D%2C%22doz%22%3A%7B%22value%22%3A%2212m%22%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22att%22%3A%7B%22value%22%3A%22renovated%22%7D%2C%22mp%22%3A%7B%22max%22%3A5234%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22rs%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

# Function to create price chunks for the specified listing URL
def createPriceChunks(api_key, listing_url):
    # API URL for creating price chunks
    url = "https://app.scrapeak.com/v1/scrapers/zillow/priceChunks"

    # Parameters for the API request
    querystring = {
        "api_key": api_key,
        "url": listing_url
    }

    # Make a GET request to create price chunks
    resp = requests.request("GET", url, params=querystring)

    # Return the JSON response
    return resp.json()

# Function to get the price chunk list for a given task ID
def getPriceChunkList(api_key, task_id):
    # API URL to get the price chunk list
    url = "https://app.scrapeak.com/api/task/result"

    # Parameters for the API request
    querystring = {
        "api_key": api_key,
        "task_id": task_id
    }

    # Make a GET request to get the price chunk list
    resp = requests.request("GET", url, params=querystring)

    # Return the JSON response
    return resp.json()

# Function to fetch listings for a given price range
def get_listings(api_key, listing_url):
    # API URL to fetch listings
    url = "https://app.scrapeak.com/v1/scrapers/zillow/listing"

    # Parameters for the API request
    querystring = {
        "api_key": api_key,
        "url": listing_url
    }

    # Introduce a delay to avoid overloading the server with requests
    time.sleep(2)

    # Make a GET request to fetch the listings
    return requests.request("GET", url, params=querystring)

# Wait for the price chunks task to finish.
def wait(api_key, task_id):
    while True:
        url = "https://app.scrapeak.com/api/task/status"

        # Parameters for the API request
        querystring = {
            "api_key": api_key,
            "task_id": task_id
        }
        
        resp = requests.request("GET", url, params=querystring)
        if resp.json()["data"]["status"] == "SUCCESS":
            break
        else:
            print("Waiting for the task to finish...")
            time.sleep(5)
            continue


taskInfo = createPriceChunks(api_key, listing_url)
print("The price chunks task has been created successfully. Details -> ", taskInfo)

wait(api_key, taskInfo["data"]["task_id"])
print("The price chunks task has been completed successfully.")

# Replace "TASK_ID" with the actual task ID obtained from createPriceChunks
priceChunkTaskId = taskInfo["data"]["task_id"]


priceChunkListResp = getPriceChunkList(api_key, priceChunkTaskId)
priceChunkList = priceChunkListResp["data"]["result"]["chunks"]

# Iterate through each price range and fetch listings
for priceRange in priceChunkList:
    # Display the price range being processed
    print("priceRange -> ", priceRange)
    # priceRange : {'chunkMinPrice': 0, 'chunkMaxPrice': 122070, 'chunkedlistSize': 429}
    
    # Parse and extract searchQueryStateData from the listing URL
    searchQueryStateData = {}
    for param_key, param_value in parse.parse_qs(parse.urlparse(listing_url).query).items():
        value = param_value[0]
        if value[0] == "{":
            value = json.loads(value)
        searchQueryStateData[param_key] = value
            
    # Start fetching listings for the given price range and pagination
    pageNumber = 1
    while True:
        # Update the searchQueryStateData with the current price range and page number
        searchQueryStateData["searchQueryState"]["pagination"] =  {"currentPage":pageNumber}
        searchQueryStateData["searchQueryState"]["filterState"]["price"] = {"min":priceRange["chunkMinPrice"], "max":priceRange["chunkMaxPrice"]}
        
        # Create a new listing URL with the updated searchQueryStateData
        listing_url = listing_url.split("searchQueryState=")[0]+parse.urlencode(searchQueryStateData)
        listing_url = listing_url.replace("%27", "%22").replace("True","true").replace("False", "false").replace("None","null")
        
        # Display the generated listing URL for debugging purposes
        print(listing_url)
        
        # Fetch the listings using the updated listing URL
        listing_response = get_listings(api_key, listing_url)
        
        # Display the response content for debugging purposes
        print(listing_response.text)

        # Check if the response was successful and process the listings
        if listing_response.status_code == 200:
            data = listing_response.json()["data"]
            if "cat1" in data:
                cat1_data = data["cat1"]
                print(data["categoryTotals"]["cat1"]["totalResultCount"])
                if data["categoryTotals"]["cat1"]["totalResultCount"] >= 1:
                    if "searchResults" in cat1_data:
                        search_results = cat1_data["searchResults"]
                        if "listResults" in search_results:
                            # Normalize and filter the JSON data to create a DataFrame
                            df_listings = pd.json_normalize(search_results["listResults"])

                            # Select only desired columns
                            selected_columns = ["hdpData.homeInfo.zpid", "hdpData.homeInfo.homeType", "hdpData.homeInfo.streetAddress", "hdpData.homeInfo.city", "hdpData.homeInfo.state", "hdpData.homeInfo.zipcode", "hdpData.homeInfo.livingArea", "hdpData.homeInfo.lotAreaValue", "hdpData.homeInfo.bedrooms", "hdpData.homeInfo.bathrooms", "detailUrl"]
                            df_selected = df_listings[selected_columns]

                            # Display the information about the DataFrame
                            print("Number of rows:", len(df_selected))
                            print("Number of columns:", len(df_selected.columns))
                            
                            # Save the DataFrame to a CSV file with price range and page number in the filename
                            df_selected.to_csv("listings_{}_to_{}_p{}.csv".format(priceRange["chunkMinPrice"], priceRange["chunkMaxPrice"], pageNumber), index=False)
                else:
                    # No more listings found, break the loop
                    break
        else:
            # Display the error response if fetching listings failed
            print(listing_response.text)
            print("Failed to fetch listings.")
            
        # Increment the page number for the next iteration
        pageNumber += 1


