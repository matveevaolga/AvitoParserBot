from selenium.webdriver.common.by import By


class Parser:
    def __init__(self, category, driver):
        self.driver = driver
        self.category = category
        self.current_number = {
            "zhivotnye": 0
        }
        self.selector_dict = {
            f"{category}_id": "...",
            "title": ".title-info-title-text",
            "photo": '[data-marker="item-view/gallery"] img',
            "description": "[itemprop=description]",
            "price": ".styles-module-size_xxxl-A2qfi",
            "location": "[itemprop=address]",
            "link": "..."
        }

    def _form_dict(self, driver, category):
        formed_dict = {}
        link = ''
        item = driver.find_element(By.CSS_SELECTOR, f"[data-marker=item]:nth-of-type({self.current_number[category]})")
        for key in self.selector_dict.keys():
            try:
                if key == 'photo':
                    formed_dict[key] = driver.find_element(By.CSS_SELECTOR, self.selector_dict[key]).screenshot_as_base64
                elif key == f'{category}_id':
                    formed_dict[key] = item.get_attribute("id")
                    item = item.find_element(By.CSS_SELECTOR, ".iva-item-title-py3i_ a[itemprop='url']")
                    link = item.get_attribute("href")
                    driver.get(link)
                elif key == 'link':
                    formed_dict[key] = link
                elif key == 'location':
                    formed_dict[key] = driver.find_element(By.CSS_SELECTOR, self.selector_dict[key]).text.split('\n', maxsplit=1)[0].strip()
                else:
                    formed_dict[key] = driver.find_element(By.CSS_SELECTOR, self.selector_dict[key]).text
            except Exception as ex:
                print(key, ': ')
                print(ex)
                formed_dict[key] = None
        return formed_dict

    def parse_data(self):
        self.current_number[self.category] += 1
        result = self._form_dict(self.driver, self.category)
        print("Successfully parsed", end=" ")
        return result
