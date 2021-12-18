import requests
from bs4 import BeautifulSoup
from flask import request
from flask import Flask
from waitress import serve

# Step 1 : inserting the links to webscrap
# in case of any changes in the links we only have to change the link in this list, every function is connected with this list regarding the changment in links
url_array = ['https://action.jo/ar/offers',
             'https://smartbuy-me.com/smartbuystore/ar/%D8%A7%D9%84%D8%B9%D8%B1%D9%88%D8%B6/c/DEALS?q=%3AnewestDate%3Abrand%3AAPPLE']

name = ""
discount = ""
price = ""
urlName = ""
newName = ""
newPrice = ""
newDiscount = ""
productSite = ""


# step 5:  extrating the data from the links
def init(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    items = ""
    if url == url_array[0]:
        items = soup.find_all("div", attrs={"class": "col-6 col-sm-4 col-md-3 p-2 align-items-stretch"})
    elif url == url_array[1]:
        items = soup.find_all("div", attrs={"class": "mainproduct_div itembox"})
    return items


# step 4 part 2: here to extract only from action mobile
def action_mobile(url):
    global name, discount, price, urlName
    for item in init(url):
        name = name + item.find("div", class_="card-title flex-grow-1").text + "~"
        discount = discount + item.find("div", class_="discount").text + "~"
        price = price + item.find("span", class_="integer").text + item.find("span", class_="decimal").text + "~"
        urlName = urlName + "Action Mobile" + "~"


# step 4 part 1: here to extract only from smartbuy
def smartbuy(url):
    global name, discount, price, urlName
    for item in init(url):
        name = name + item.find("a", class_="name view-grid hidden-xs").text + "~"
        discount = discount + item.find("span", class_="percentagePrice-list").text + "~"
        price = price + item.find("span", class_="orignalPrice list-style").text + "~"
        urlName = urlName + "Smart buy" + "~"


# step 3: here to identify the website
def website(url):
    if url == url_array[0]:
        action_mobile(url)
    elif url == url_array[1]:
        smartbuy(url)


# step 2:  this for taking the link from the list
for j in url_array:
    access = requests.get(j)
    if access.status_code == 200:
        website(j)
    else:
        print(j + " Error with this link")

app = Flask(__name__)


# for flask purpose what data we are presenting
@app.route('/mobiles/productName')
def product_Name():
    global newName, newPrice, newDiscount, productSite
    newName = ""
    newPrice = ""
    newDiscount = ""
    productSite = ""
    i = 0
    isOneplusSelected = request.args.get('oneplus')
    isIphoneSelected = request.args.get('apple')

    nameList = name.split("~")
    priceList = price.split("~")
    discountList = discount.split("~")
    productSiteList = urlName.split("~")

    for onename in nameList:
        if onename.lower().find("apple") != -1 and isIphoneSelected == "true" or onename.lower().find("iphone") != -1:
            newName = newName + onename + "~"
            newPrice = newPrice + priceList[i] + "~"
            newDiscount = newDiscount + discountList[i] + "~"
            productSite = productSite + productSiteList[i] + "~"
        i = i + 1

    i = 0

    for onename1 in nameList:
        if onename1.lower().find("one plus") != -1 and isOneplusSelected == "true":
            newName = newName + onename1 + "~"
            newPrice = newPrice + priceList[i] + "~"
            newDiscount = newDiscount + discountList[i] + "~"
            productSite = productSite + productSiteList[i] + "~"

        i = i + 1
    return newName


@app.route('/mobiles/productPrice')
def product_Price():
    return newPrice


@app.route('/mobiles/productDiscount')
def product_Discount():
    return newDiscount


@app.route('/mobiles/productSite')
def product_Site():
    return productSite


@app.route('/', methods=['GET'])
def home():
    print("rrr")
    return "hello"


if __name__ == '__main__':
    try:
        serve(app, host="0.0.0.0", port="5000")
    except:
        print("unexcepted error")



