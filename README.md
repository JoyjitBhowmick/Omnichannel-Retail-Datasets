# Usage of This Data Sets
The data sets are intended for research purpose and can be used for any non-commercial purpose. We request you cite our work as follows - 

Joyjit Bhowmick and Jennifer Pazour. A Connected In-Store and Online Customer Data Set for Omnichannel Retail Logistics Research. In IIE Annual Conference. Proceedings, pages 1–6. Institute of Industrial and Systems Engineers (IISE), 2024. (Submitted)


## Introduction
We present four datasets and describe the methodology used to create these datasets along with supplementary source datasets and Python codes from which the four datasets were developed. The key idea behind the datasets is to connect them in terms of a group of products with similarities, which we denote as ’Product Families’. For instance, soy milk, almond milk, skim milk, whole milk, etc. are grouped into one product family named ’Milk.’ This allows us to organize data and make connections across in-store and online customer channels and among multiple data sources. Also, because individual products change frequently in grocery stores, but the product families tend to have similar characteristics, this allows for a more manageable data unit than gathering data at the individual item levels.Our datasets include -
(1) a mapping of product families between two different data sources 
(2) demand and shopping behavior for each product family for online and in-store customers; 
(3) product dimension, weight, and price for each product family; and lastly, 
(4) in-store customer and online order arrival rates on a granular level, specifically, per hour
and day of the week level.


## Description of Datasets
In what follows, we describe the datasets in detail with column definitions, insights, methods, and sources used to
generate these data sets.

### Mapping of Product Families
The first step of developing the connected datasets was to create a mapping between two data sources. One is the online
order datasets from instacart [13], which is an anonymized data set containing more than 200,000 users’ grocery orders
totaling over 3 million. Each order is connected to a user, a list of items, and the hour at which the order was placed
in the week. Additionally, it includes 49,688 product types, regardless of size, brand, and other specifications, that are
mapped into 134 product categories. The second is the in-store customer purchase and behavior dataset [12], which
defines 96 zones in a grocery store each covering several product types, which can be considered product groups, and
includes in-store customer purchase percentage and shopping behavior for each of these zones. Both of these data sets
provide demand profiles, which motivated us to develop a dataset named ’Product Family Mapping’ connecting the
attributes from these two sources with the column descriptions as follows -

• The column ’Aisle ID’ corresponds to the product categories defined in the instacart dataset [13] for online orders.
There are 134 such different product categories. We use these 134 categories as the central node in our dataset.
• ’Zone ID’ refers to the mapped product category used for in-store customer shopping behavior in a grocery store,
obtained in [12]. There are 96 such different zones.
• Since there was no clear one-to-one relationship among the product categories between the two sources, we also
provide alternative zones in the ’Zone ID Alternatives’ column, from the in-store dataset [12] which may be mapped
to the ’Aisle ID’ column, but may fall short to capture the majority of the defined product types compared to the
’Zone ID’ column. Empty values in this column mean there is no other alternative available.
• For each of the ’Aisle ID’ in the instacart dataset, there is an assigned ’Aisle’ name representing the product category
as a whole. For instance, all types of milk are included in the aisle name ’Milk’. We rename this ’Aisle’ column to
’Product Family’ which is more helpful to define a group of products more maybe?. For convenience, what product
types are grouped in a product family is made available in our repository under the name ’Aisle ID to Products’.

As the 96 zones are essentially discreet zones in a store layout described in [12], these mapped 134 product families
can also be mapped to the layout to achieve a transformed layout that can capture both in-store and online customers.



### Product Family Attribute Data
Next, for each of the 134 mapped Aisle ID in the previous section, we collect relevant attribute data. Based on the type of
attributes, we create two separate datasets: one based on customer demands and shopping behavior (both online and
in-store) named ’Demand of Product Families,’ and the second based on product information such as dimensions,
weight, and price, stored in the dataset named ’Product Information’. The first two columns of each of these two
datasets are named ’Aisle ID’ and ’Product Family’, which have been previously defined in Section 3.1.

#### Customer Demand and Shopping Behavior Data
• We map the 134 product families to in-store purchase rates from [12] with the column name "In-store Customers’
Purchase Percentage". This refers to the percent of arriving in-store customers buying an item from a product family.
We observe that over 50% in-store customers buy fresh fruits, vegetables, packaged produce, and herbs, whereas
less than 1% in-store customers buy spirits, prepared meals, canned meals, protein meal replacements, and cocoa
drink mixes.
• From the instacart dataset’s order history [13], we identify how many times a product family appeared in any order,
providing the percentage of online customers ordering an item from a product family. Thus, we created the column
’Online Customers’ Purchase Percentage’.
• The values of the column "In-store Customers’ Purchase Percentage" are extended into a discretized probability
distribution where we add all the values in "In-store Customers’ Purchase Percentage" and find the fraction of
the total for each product family, naming the column "Discrete Probability Distribution for In-store Customers."
This column helps to identify the probability of the next item being bought in the store. Further analysis of the
cumulative values of this column after ranking the product families from highest to lowest value shows that about
80% of in-store demand is fulfilled by about 40% of product families in the store.
• Similar to "Discrete Probability Distribution for In-store Customers", we transform the data from the column ’Online
Customers’ Purchase Percentage’ and create the column "Discrete Probability Distribution for Online Customers"
referring to the probability of an item being bought online from a product family. Similar cumulative demand
analysis shows about 40% of product families generate more than 80% of demand online. Moreover, fresh fruits
and vegetables are both the top demanded category in both channels; however, the in-store demand for these product
families are about 4% whereas online demand is about 11%.
• Impulse purchase refers to the purchase of a product by an in-store customer triggered by visual or other stimuli but
was actually unplanned upon entering the store [16]. We obtain the impulse purchase rates from [6] and manually
map them to the 134 product families. Thus, the column "Impulse Purchase Rate" thus captures the likelihood of an
item from a product family being bought impulsively when noticed by an in-store customer. For instance, Product
families such as chips, gum, candy, and chocolate are high-impulse purchase products which is why they are often
given larger shelf space [6] and duplicated around the checkout zone so that customers get enticed while they wait
[18].
• Emotional products are the ones that customers want to examine physically before they make a purchase decision
[29] (e.g., fresh produce). We manually made the distinction between whether a product family was categorized
as being emotional or unemotional based on the majority of the items in the product family and whether or not
that product family contained different versions of a single item. For instance, the product family ’Fruits’ contains
products that the customer may want to examine for ripeness and freshness, thus, marking it as emotional. This is in
contrast to unemotional products, which would be a product family that contains mostly packaged consumer goods,
like ’cereal’ that the customer would not need to spend time inspecting one box from another. Apart from such
clear distinctions, as each product families contain a lot of product types, some may fall under emotional and some
may fall under unemotional. In those cases, we categorized it as ’emotional’ if majority of the product types are
seemingly emotional and vice versa. This led to 33 products families categorized as emotional and the remaining
101 product families were categorized as unemotional and included, for example, coffee and cereal.
• Derived from the combination of average in-store customer arrivals from Section 3.3 and the column "In-store
Customers’ Purchase Percentage," we create the column "Average daily demand (in-store)" which refers to the
mean units of products expected to be sold daily for each product family by in-store customers. We take the average
customer arrivals of 3,265 [25, 30] to a store on a daily basis and multiply this number by the value of ’In-store
Customers’ Purchase Percentage’ to find the average daily demand in units.
• Similar to "Average daily demand (in-store)", we create the column "Average daily demand (Online)" calculated by
multiplying the average daily online orders of 128 estimated from [8, 19, 20], average basket size of 10.53 estimated
from [13], and the values from ’Discrete Probability Distribution for Online Customers’.
• The column ’Dwell Time (seconds)’ refers to the amount of time in seconds an in-store customer is expected to
dwell or walk around the shelves of the respective product family before leaving that area. We obtain the data from
[12] and follow the mapping described in Section 3.1 to generate this column.


#### Product Information Data
The dataset named ’Product Information’ was obtained by web scraping Amazon.com in January 2023 searching for
products with the same tag as the name mentioned in ’Product Family’ column followed by scrpaing the details of the
tagged products and storing them. This led us to collect details of 8,220 products in total, with each product family
having a different number of individual products scraped. For each of these products, we collected the product title
description as it appears on the website and attempted to collect three product attribute values: dimensions, weight, and
price. Similar to the dataset described in Section 3.2.1, the first column of the dataset named ’Product Information’
show the ’Aisle ID’ defined previously. However, the rest of this dataset differs in the method used to obtain the
attributes as we webscraped and summarized the data. The other columns of this dataset are described as follows:
• As for each product family, numerous items were scraped for information, we present the number of items considered
to come up with the summary statistics in the following columns. We labeled this column as ’Items Considered’.
• The dimensions of the products were captured by length, width, height. The following 12 columns represent the
average, standard deviation, maximum, and minimum dimensions in inches.
• We also captured the weight of the scraped products in pounds, which are similarly presented as the average,
standard deviation, maximum, and minimum.
• Lastly, the price of each scraped product was collected and summarized with the same four statistics in USD.
To provide researchers with further resources, we provide the web-scraped dataset named ’Web Scraped Product
Information’ with dimensions, weight, price, and the product description that appears on Amazon.com for each of the
8,220 products scraped. Additionally, the Python codes utilized to scrape the data as well as extract the needed data to
achieve the summary statistic are also made available under the names ’Webscrpaing Amazon’ and ’Data Extraction’,
respectively.



### In-store Customer and Online Order Arrivals
In the next dataset named ‘In-store Customer and Online Order Arrivals’, we estimate the customer arrivals for both
in-store and online channels on a granular level capturing arrivals each hour and day of the week. We estimated instore
customer arrival patterns using Google popular time data for a Walmart store (collected in September 2022),
considering average weekly customer arrival of 22,857 per store[25] across 10,500 Walmart retail units [30]. Next,
utilizing the data from Google Popular times as a proportional measurement and multiplying them by weekly in-store
customer arrivals per store of 22,857, we break down the arrivals by each hour of the day and each day of the week.
The first column named ’Day’ presents the seven days of the week. We present the data in 24-hour format and both
the columns ’From time’ and ’To time’ follow that format. The fourth column, ’Avg. In-store Customer Arrivals’,
represents the number of customers expected (rounded up) to enter the store within the specified one-hour period.
For instance, 25 customers on average enter the store between 6 am to 7 am on a Monday. Analysis into the dataset
suggests the most crowded store is found in the afternoon hours from 1 pm to 4 pm, and the least crowded is in the
morning times (6 am - 9 am) and late night hours (9 pm-11 pm). Additionally, Saturday is the most crowded followed
by Friday and Sunday. On the other hand, Monday and Tuesday are the least crowded day of the week. We also
estimate the online order arrival pattern based on the average weekly orders per store [8, 19, 20] and number of orders
per hour per day of the week from [13]. We present the data in the column ’Avg. Online Order Arrivals’. We find
similar patterns compared to in-store customer arrivals. Further analysis shows the most online orders are placed
between 10 am - 6 pm, and most online orders are placed on Fridays and weekends.


