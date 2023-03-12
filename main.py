import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def close_popup(driver):
    try:
        popup_close_element = WebDriverWait(driver, timeout=10).until(
            lambda d: d.find_element(By.CSS_SELECTOR, '.exponea-close-cross')
        )
    except Exception as err:
        print('No popup here', err)
    else:
        popup_close_element.click()


def continue_button_element(driver):
    return driver.find_element(By.ID, 'continue_button')


def input_radio_element(driver, value):
    return WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(By.CSS_SELECTOR, f'.input-radio[value^="{value}"]')
    )


def main():
    # incializuj webdriver
    driver = webdriver.Chrome()
    driver.maximize_window()

    # otevri url okay.cz
    driver.get('https://www.okay.cz/')

    # zavři reklamní popup
    close_popup(driver)

    # klikni na kategorii televize
    menu_element = driver.find_element(By.LINK_TEXT, 'Televize')
    menu_element.click()

    # vyber 1. televizi a klikni na ní
    collection_items = driver.find_elements(By.CSS_SELECTOR, '.boost-pfs-filter-products .product__imageContainer')
    collection_items[0].click()

    # v detailu televizi vlož do košíku
    add_to_cart = driver.find_element(By.CSS_SELECTOR, '.shopify-product-form .button--add-to-cart')
    add_to_cart.click()

    # počkej než se produkt přidá do košíku
    WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(By.CSS_SELECTOR, '.header-cart__count-number').text == '1'
    )

    # přejdi do košíku
    driver.get('https://www.okay.cz/cart')

    # klikni na "k pokladně"
    checkout_button = WebDriverWait(driver, timeout=30).until(
        EC.element_to_be_clickable((By.ID, 'checkout'))
    )
    time.sleep(1)
    checkout_button.click()

    # zadej požadované doručovací údaje
    input_fields = {
        'checkout[email]': 'test.okay@okaycz.eu',
        'checkout[shipping_address][first_name]': 'test',
        'checkout[shipping_address][last_name]': 'test',
        'checkout[shipping_address][address1]': 'Testovaci 123',
        'checkout[shipping_address][zip]': '60200',
        'checkout[shipping_address][city]': 'Brno',
        'checkout[shipping_address][phone]': '+420123456789'
    }

    for key, value in input_fields.items():
        input_field = driver.find_element(By.NAME, key)
        input_field.send_keys(value)

    # klikni na "pokračovat v dopravě"
    continue_button_element(driver).click()

    # vyber způsob dopravy
    shipping_method = input_radio_element(driver, 'PI Bespoke Shipping-DASE')
    shipping_method.click()

    # klikni na "pokračovat k platbě"
    continue_button_element(driver).click()

    # vyber způsob platby
    payment_method = input_radio_element(driver, '65295188010')
    payment_method.click()

    # klikni na "odeslat objednávku"
    # continue_button_element(driver).click()

    # ukonči test
    time.sleep(10)
    driver.quit()



if __name__ == '__main__':
    main()