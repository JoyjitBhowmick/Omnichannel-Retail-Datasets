from bs4 import BeautifulSoup
import requests
import csv
import pandas
import re
import time






# Function to extract Product Title
def get_title(soup):
	try:
		# Outer Tag Object
		title = soup.find("span", attrs={"id":'productTitle'})
        ##Clean format
		title_value = title.string
		title_string = title_value.strip()
	except AttributeError:
		title_string = ""	
	return title_string


# Function to extract price
def get_price(soup):
    ##id type attribute
    price_id=['priceblock_ourprice','idpriceblock_dealprice','corePrice_desktop','sns-base-price']
    price1 = None
    for i in price_id:
        price1 = soup.find("span", attrs={'id':i})
        if price1 is not None:
            break
    else:
        ##class type attribute
        price_class = ['a-offscreen']
        price1 = None
        for i in price_class:
            price1 = soup.find("span", attrs={'class':i})
            if price1 is not None:
                break
        ##Clean format
    price1 = price1.get_text()
    price1 = price1.strip()
    return price1





# Function to extract weight
def get_weight(soup):
	weight = "Not Available"
	try:
        
        ##find specific attribute potential other attribute
		weight_element = soup.find("tr", attrs={'class':'a-spacing-small po-item_weight'})
		if weight_element is not None:
			td_element = weight_element.find("td", attrs={'class':'a-span9'})
			if td_element is not None:
				span_element = td_element.find("span")
				if span_element is not None:
					weight = span_element.string.strip()
	except AttributeError:
		pass
	return weight



# Function to extract dimension and else
def get_dimension(soup):
    dimension_element = soup.find(id='detailBullets_feature_div')
    if dimension_element is None:
        return {}

    data = {}
    for li in dimension_element.select('li'):
        key_element = li.select_one('.a-text-bold')
        value_element = li.select_one('span:nth-of-type(2)')
        if key_element and value_element:
            key = key_element.text.strip().encode('ascii','ignore').decode()
            value = value_element.text.strip()
            # Remove unwanted characters using regular expressions
            key = re.sub(r'\s*:\s*', '', key)
            value = re.sub(r'\s*[;,]\s*', '', value)
            data[key] = value

    return data


####web scrap and print
def scrap_data(URL, Cat):
    # HTTP Request
	webpage = requests.get(URL, headers=HEADERS)
	# Soup Object containing all data
	soup = BeautifulSoup(webpage.content, "lxml")
	# Fetch links as List of Tag Objects
	links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
	# Store the links
	links_list = []
	# Loop for extracting links from Tag Objects
	for link in links:
		links_list.append(link.get('href'))

	i = 0
	#total count
	TT=0
	# Loop for extracting product details from each link 
	for link in links_list:
		if i < 2000:
##delay 5 second
			##delay = 5
			##time.sleep(delay)
            ##scrap for each categorie 
			new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)
            #### decode from lxml
			new_soup = BeautifulSoup(new_webpage.content, "lxml")
			# Function calls to display all necessary product information
			print("Product Title =", get_title(new_soup))
			#print("Product Price =", get_price(new_soup))
			#print("Weight =", get_weight(new_soup))
			#print("Dimension =", get_dimension(new_soup))
            ###write to csv
			with open('AmazonData.csv', 'a+',newline='', encoding='UTF8') as f:
				writer = csv.writer(f)
				data = [Cat, get_title(new_soup), get_price(new_soup), get_weight(new_soup), get_dimension(new_soup)]
				writer.writerow(data)
			i =i+1
			TT =TT+1

if __name__ == '__main__':
    #Header = ['Category', 'Name','Price','Weight','Dimension']
    #with open('AmazonData.csv', 'w',newline='', encoding='UTF8') as f:
    #	writer = csv.writer(f)
    #	writer.writerow(Header)
    Header = ['Name','Price','Weight','Dimension']
        #read csv 
    df = pandas.read_csv('link.csv')
    ##category list
    link_list = df["Link"].tolist()
    ##category name list
    category_list = df["Cat"].tolist()
    
    # Headers for request
    ####user agent should repalce when blocked by the website /////// no need to change 'User-Agent'+'English-US'+'en-US'
    ###https://developers.whatismybrowser.com/useragents/parse/
    HEADERS = ({'User-Agent':
                #####///////////////////////////////////////////////down change below only
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
                ######//////////////////////////////////////////////up change above only
                'English-US': 'en-US'})
        
    # The webpage URL
    for link, c in zip(link_list, category_list):
        scrap_data(link, c)