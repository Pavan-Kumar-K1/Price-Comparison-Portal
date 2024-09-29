from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Set up ChromeDriver
service = Service('C:/Users/k.udayasagar/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe')

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (without opening a browser window)
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Create WebDriver instance
driver = webdriver.Chrome(service=service, options=chrome_options)

app = Flask(__name__)

# Function to scrape Amazon products
def scrape_amazon(product_name):
    details = []
    amazon_url = f'https://www.amazon.in/s?k={product_name.replace(" ", "+")}'
    
    # Using the existing driver
    driver.get(amazon_url)
    time.sleep(5)  # Wait for the page to load
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    Products = soup.find_all("div", class_="sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16")
    
    for product in Products:
        try:
            name = product.find("span", class_="a-size-medium a-color-base a-text-normal").text.strip()
        except:
            name = ''
        try:
            price = product.find("span", class_="a-price-whole").text.strip()
        except:
            price = ""
        details.append((name, price))
    
    # Filter products based on the search keyword
    details = [i for i in details if product_name.lower() in i[0].lower()]
    
    return details

# Function to scrape Flipkart products
def scrape_flipkart(product_name):
    name_price = []
    url = f'https://www.flipkart.com/search?q={product_name.replace(" ", "+")}'
    
    # Using the existing driver
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    soup = BeautifulSoup(driver.page_source, "lxml")
  
    container = soup.find("div", class_="DOjaWF gdgoEp")

    if container:
        Products = container.find_all("div", class_="cPHDOP col-12-12")
        for Product in Products:
            try:
                name = Product.find("div", class_="KzDlHZ").text.strip()
            except:
                name = " "
            try:
                price = Product.find("div", class_="Nx9bqj _4b5DiR").text.strip()
            except:
                price = " "
            try:
                ram = Product.find("li", class_="J+igdf").text.strip()
            except:
                ram = " "
            name_price.append((name, price, ram))
    
    return name_price

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        if product_name:
            flipkart_products = scrape_flipkart(product_name)
            print(flipkart_products)
            amazon_products = scrape_amazon(product_name)
            
            return render_template('index.html', flipkart_products=flipkart_products, amazon_products=amazon_products)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
