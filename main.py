from bs4 import BeautifulSoup
import requests
import pandas as pd


# Function to extract Product Title

def get_ProductName(soup):
    try:
        # Extracting Product's Name
        title_string = soup.find("span", attrs={"id": 'productTitle'}).string.strip()
    except AttributeError:
        title_string = "N/A"

    return title_string


# Function to extract Product Price

def get_ProductPrice(soup):
    try:
        # Extracting Product's Price
        price = soup.find("span", attrs={'class': 'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'}).find("span", attrs={'class':"a-offscreen"}).string.strip()
    except AttributeError:
        try:
            # If there is some deal price
            price = soup.find("span", attrs={'class': 'a-offscreen'}).string.strip()
        except:
            price = "N/A"

    return price


# Function to extract Product Rating

def get_ProductRating(soup):
    try:
        # Extracting Product's Ratings
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = "New To Amazon"

    return rating


# Function to extract Availability Status

def get_SellerName(soup):
    try:
        # Checking if the product is in Stock or not
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip()

        if available == "In stock":
            # If product is in stock we extract the seller's name
            available = soup.find("div", attrs={'id':"merchant-info"}).find("a", attrs={'class':"a-link-normal"}).find("span").string.strip()
    except AttributeError:
        # If product is out of stock we return "Out Of Stock"
        available = "Out Of Stock"

    return available



if __name__ == '__main__':

    # add your user agent
    HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})

    # The webpage URL
    URL = "https://www.amazon.in/s?k=mobile+portable+power+banks&ref=nb_sb_noss"

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")
    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
        links_list.append(link.get('href'))

    # Dictionary for storing all details and then creating a CSV file
    d = {"Product Name": [], "Price": [], "Ratings (OUT OF 5)": [], "Seller Name": []} 
    i = 0

    # Loop for extracting product details from each link
    for link in links_list:
        print("Running for product "+str(i+1))

        new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        i += 1

        # Function calls to display all necessary product information
        d["Product Name"].append(get_ProductName(new_soup))
        d["Price"].append(get_ProductPrice(new_soup))
        d["Ratings (OUT OF 5)"].append(get_ProductRating(new_soup))
        d["Seller Name"].append(get_SellerName(new_soup))

    # Converting the dictionary into a CSV file using pandas
    amazon_df = pd.DataFrame(d)
    amazon_df.to_csv("Data.csv", index=False)