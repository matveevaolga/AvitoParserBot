from selenium.webdriver.common.by import By


class Parser:
    def __init__(self, driver, cursor):
        self.driver = driver
        self.cursor = cursor
        # словарь с порядковым номером последнего обработанного объявления на странице каждой из категорий
        self.current_number = {
            "gryzuny": 0,
            "koshki": 0,
            "kroliki": 0,
            "ptitsy": 0,
            "sobaki": 0
        }
        # словарь с соответствующими селекторами для каждого столбца таблицы
        self.selector_dict = {
            "_id": "...",
            "title": ".title-info-title-text",
            "photo": '[data-marker="item-view/gallery"] img',
            "description": "[itemprop=description]",
            "price": ".styles-module-size_xxxl-A2qfi",
            "location": "[itemprop=address]",
            "link": "..."
        }

    @staticmethod
    def form_dict(self, driver, category):
        formed_dict = {}
        link = ''
        # поиск объявления на странице выбранной категории под необходимым номером
        item = driver.find_element(By.CSS_SELECTOR, f"[data-marker=item]:nth-of-type({self.current_number[category]})")
        # парсинг страницы и заполнение словаря formed_dict
        for key in self.selector_dict.keys():
            try:
                if key == 'photo':
                    formed_dict[key] = driver.find_element(By.CSS_SELECTOR, self.selector_dict[key]).screenshot_as_base64
                elif key == '_id':
                    # объявление под category_id уже встречалось, парсинг останавливается
                    if self.cursor.execute(
                            f"SELECT id FROM {category} where {category}_id = '{item.get_attribute('id')}';"):
                        print("Has already been added", item.get_attribute('id'))
                        formed_dict = {}
                        break
                    # иначе продолжаем парсинг
                    formed_dict[f'{category}_id'] = item.get_attribute("id")
                    # найдено объявление => переход на его страницу
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

    def parse_data(self, numb, category):
        result = []
        # парсинг продолжается, пока в result не добавится необходимое кол-во объявлений выбранной категории
        while len(result) != numb:
            # переход на страницу сайта с выбранной категорией
            self.driver.get(f"https://avito.ru/moskva/{category}")
            # будет парсинг объявления под этим номером
            self.current_number[category] += 1
            cur = Parser.form_dict(self, self.driver, category)
            # объявление не встречалось => добавляем его в result
            if cur:
                result.append(cur)
                print(f"Successfully parsed {cur[f'{category}_id']}")
            # если объявление уже встречалось в таблице выбранной категории, переход
            # к парсингу следующего объявления
        return result
