import undetected_chromedriver as uc
from selenium import webdriver

current_number = {
    "zhivotnye": 0
}

selector_dict = {
    "animal_id": "...",
    "title": ".title-info-title-text",
    "photo": '[data-marker="item-view/gallery"] img',
    "description": "[itemprop=description]",
    "price": ".styles-module-size_xxxl-A2qfi",
    "location": "[itemprop=address]",
    "link": "..."
}


def form_dict(driver, category):
    formed_dict = {}
    link = ''
    item = driver.find_element(uc.By.CSS_SELECTOR, f"[data-marker=item]:nth-of-type({current_number[category]})")
    for key in selector_dict.keys():
        try:
            if key == 'photo':
                formed_dict[key] = driver.find_element(uc.By.CSS_SELECTOR, selector_dict[key]).screenshot_as_base64
            elif key == 'animal_id':
                formed_dict[key] = item.get_attribute("id")
                item = item.find_element(uc.By.CSS_SELECTOR, ".iva-item-title-py3i_ a[itemprop='url']")
                link = item.get_attribute("href")
                driver.get(link)
            elif key == 'link':
                formed_dict[key] = link
            elif key == 'location':
                formed_dict[key] = driver.find_element(uc.By.CSS_SELECTOR, selector_dict[key]).text.split('\n', maxsplit=1)[0].strip()
            else:
                formed_dict[key] = driver.find_element(uc.By.CSS_SELECTOR, selector_dict[key]).text
        except Exception as ex:
            print(key, ': ')
            print(ex)
            formed_dict[key] = None
    return formed_dict


def parse_data(category):
    current_number[category] += 1
    link = f"https://avito.ru/moskva/{category}"
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = uc.Chrome(version_main=114, options=options)
    driver.get(link)
    result = form_dict(driver, category)
    print("Successfully parsed", end=" ")
    driver.close()
    return result
