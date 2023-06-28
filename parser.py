import undetected_chromedriver as uc

current_number = {
    "zhivotnye": 0
}


def get_data(category):
    current_number[category] += 1
    link = f"https://avito.ru/moskva/{category}"
    driver = uc.Chrome()
    driver.get(link)
    item = driver.find_element(uc.By.CSS_SELECTOR, f"[data-marker=item]:nth-of-type({current_number[category]}) a")
    link = item.get_attribute("href")
    driver.get(link)
    title = driver.find_element(uc.By.CSS_SELECTOR, ".title-info-title-text").text
    description = driver.find_element(uc.By.CSS_SELECTOR, "[itemprop=description]").text
    price = driver.find_element(uc.By.CSS_SELECTOR, ".styles-module-size_xxxl-A2qfi").text
    address_and_metro = driver.find_element(uc.By.CSS_SELECTOR, "[itemprop=address]").text.split('\n', maxsplit=1)
    address = address_and_metro[0]
    metro = address_and_metro[1]
    result = [title, description, price, address, metro, link]
    return result


