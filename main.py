import requests
from bs4 import BeautifulSoup
import smtplib
import time

headers = {}  # enter your header here


def look_for_price(URL_func, price_desired_func, user_email_func):
    page = requests.get(URL_func, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    # custom made for amazon..

    title_prod = soup.find(id="productTitle").get_text()
    try:
        price_prod = soup.find(id='priceblock_ourprice').getText()
    except AttributeError:
        price_prod = soup.find(id="priceblock_dealprice").get_text()
    print(title_prod.strip(), price_prod.strip())

    price_without_rupee = price_prod[2:]
    price_formatted = float(price_without_rupee.replace(',', ''))

    print(price_formatted)
    if price_formatted < price_desired_func:
        send_price_alert(URL_func, user_email_func, price_prod)


def send_price_alert(URL_func, user_email_func, price_prod):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    print(user_email_func)
    server.login('yourmail', 'yourpassword')

    subject_mail = 'Hey there the price fell down'

    # ascii manipulations to manipulate string

    price_prod = price_prod.encode('ascii', errors="ignore").strip()
    priceOnMail = price_prod.decode('ascii')
    body_mail = f'hey there the price has dropped to: {priceOnMail} check out the link: {URL_func}\n'
    msg = f"Subject: {subject_mail}\n\n{body_mail}"

    server.sendmail('yourmail', user_email_func, msg)

    print('Hey the email has been sent')

    server.quit()


# code executing starts from here

print('Hey Welcome please enter the URL of the amazon product that you want to track')
URL = input(':')
price_desired = float(input('Enter the amount for an alert:'))
user_email = str(input('Please enter the mailId where you want the alert:'))

# check for price every hour

while True:
    look_for_price(URL, price_desired, user_email)
    time.sleep(3600)
