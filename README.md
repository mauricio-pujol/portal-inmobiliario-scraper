# Portal Inmobiliario Web Scraper
## Description
[Portal Inmobiliario](https://www.portalinmobiliario.com/) is the main website in Chile to publish real estate for sale online. 
**The purpose of this project is to implement and ETL process to extract properties from this website periodically in a certain city or area.**

Required steps to achieve this are:
- Retrieve semi-structured html.
- Clean and transform it into a tabular data structure.
- Store it for further analysis. <span style="color:red;">(to do: Store on cloud.)</span>

Future ideas to be developed include estimating if a specific property for sale is under or over its market value, according to its attributes, neighbor properties attributes and prices, city and historic market trends as well.

<span style="color:red;">(to do: Dockerize.)</span>

## Requirements
Ensure to have the following libraries. Version used is specified as well:
- pandas = 2.1.1
- beautifulsoup4 = 4.12.2
- urllib3 = 2.0.6
- numpy = 1.26.1
- openpyxl = 3.1.2

<span style="color:red;">(to do: Migrate to a requirements.txt)</span>


## Usage
This section explains what every .py file does for every stage of the ETL process.

### **Extraction stage**

- `dictionary_location.py`: Fixed dictonary that pairs the city to the URL of Portal Inmobiliario. It’s called in `main_extraction.py`

- `function_scrape_property.py`: This file defines a major function that deals with most of the extraction in `main_extraction.py`. In simple, the function:
    1. Given a property URL as an input, retrieves its html and scrapes it using `Beautiful Soup`.
    2. From the this html, extract relevant attributes of the scanned property such as: title, description, price, maintenance_cost, size, number of bedrooms and bathrooms, coordinates, broker and other secondary attributes.
    3. Returns a 1-row dataframe containing this property scraped data.
<span style="color:red;">(to do: optimize waiting time while requesting html.)</span>

- `main_extraction.py`: This is the main script that runs the **Extraction Stage**. These are, in general terms, the steps:
    1. Starts by defining a city to scan properties. For example, set `location` to “Reñaca”, a coastal city in Chile. The city must be predefined in the fixed dictionary locations_url, which is called from `dictionary_locations.py` file.
    2. Sets the browser to show real estate properties within selected location. Unless the selected city or area is extremely small, these properties will be shown on multiple pages. The script iterates every page (1, 2, …, n) and saves the specific URL of each property indexed within the page. These URLs are temporary stored on `set_urls`.
    3. Generates an empty dataframe named `df_raw_data`. Later it will be used to store semi-structured data scanned from each property.
    4. Iterates over every URL in `set_urls` calling the function `extract_property_raw_data`. For every property requests the html, and extract the key attributes of the property. These atributes are saved into `df_raw_data` as they are.
    5. Once the iteration is over, the resulting `df_raw_data` is saved as .csv file locally in the directory /extracted_data. Note that the .csv file contains some metadata, like city and date time. For example, `/extracted_data/venta-departamento-Reñaca_2024-02-12 07.51.51.021097.csv` means that the script was set to scan apartments for sale in Reñaca and that the scraping was done on 2024-02-12 at 07.51.51 local time.

**This concludes the extraction stage.**

### **Transformation stage**

- `main_transformation.py`:  This is the main script that runs the Tranformation Stage. There are some cleaning functions defined in this file as well. These are, in general terms, the steps:
    1. Iterate and merge every .csv file within /extracted_data into a single dataframe. Add the datetime metadata found in the .csv file name to a column named `load_date`.
    2. Apply cleaning function to each column. For example:
        - Standarize price from CLP to UF.
        - Transform to integer text fields such as '2 baños' (2 bathrooms).
        - Transform orientation to a bool column. The input for North orientation may come as 'N', 'Nor', 'NO', and so on. Transform into a boolean column named `orientation_north`.

<span style="color:red;">(to do: migrate to a new functions_clean.py)</span>

<span style="color:red;">(to do: Complete Transformation process by saving the clean data dataframe resulting)</span>
## Configuration
Explain any configuration option or settings in the .py files