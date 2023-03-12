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
    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get('https://www.okay.cz/')

    close_popup(driver)

    menu_element = driver.find_element(By.LINK_TEXT, 'Televize')
    menu_element.click()

    collection_items = driver.find_elements(By.CSS_SELECTOR, '.boost-pfs-filter-products .product__imageContainer')
    collection_items[0].click()

    add_to_cart = driver.find_element(By.CSS_SELECTOR, '.shopify-product-form .button--add-to-cart')
    add_to_cart.click()

    WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(By.CSS_SELECTOR, '.header-cart__count-number').text == '1'
    )

    driver.get('https://www.okay.cz/cart')

    checkout_button = WebDriverWait(driver, timeout=30).until(
        EC.element_to_be_clickable((By.ID, 'checkout'))
    )
    time.sleep(1)
    checkout_button.click()

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

    continue_button_element(driver).click()

    shipping_method = input_radio_element(driver, 'PI Bespoke Shipping-DASE')
    shipping_method.click()

    continue_button_element(driver).click()

    payment_method = input_radio_element(driver, '65295188010')
    payment_method.click()

    # continue_button_element(driver).click()

    time.sleep(10)
    driver.quit()


if __name__ == '__main__':
    main()
