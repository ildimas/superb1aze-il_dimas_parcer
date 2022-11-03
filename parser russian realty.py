import requests
from bs4 import BeautifulSoup
import time
import random


starter = 1
end = 5
all_appartments_dict = {}
pages = 10
def parcer(starter, end, all_appartments_dict, pages):
    if end >= pages:
        return all_appartments_dict
    else:
        persent = (end / pages) * 100
        for i in range(starter, end):
            # запрос на сайт
            url = f'https://www.russianrealty.ru/%D0%9F%D1%80%D0%BE%D0%B4%D0%B0%D0%B6%D0%B0-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80/{i}/'
            headers = {
                "Accept": 
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
            }

            req = requests.get(url, headers=headers)
            src = req.text

            # запись в файл
            with open("index.html", "w", encoding="utf-8") as file:
                file.write(src)

            with open("index.html", "r", encoding="utf-8") as file:
                src = file.read()

            # парс данных
            soup = BeautifulSoup(src, "lxml")
            all_appartments_hrefs = soup.find_all("div", {"class": "hproduct"})

            for div in all_appartments_hrefs:
                # имя, ссылка, количество комнат
                item_name = div.find('a').text
                item_name = item_name.replace("&sup2", "2")
                item_href = "https:" + div.find('a').get('href')
                item_rooms_number = int(item_name[0])

                # цена и адрес
                item_price = int(div.find('span').text)
                item_adress_details = div.find('p', class_ = "adr").text

                in_point_item_adress_details = item_adress_details.index("«")
                item_adress = item_adress_details[0 : in_point_item_adress_details]

                # количество минут до метро
                try:
                    in_point_item_adress_details_ending = item_adress_details[::-1].index(",")
                    in_point_item_adress_details_ending2 = item_adress_details[::-1].index(" ")
                    item_minutes_for_subway = item_adress_details[len(item_adress_details) - in_point_item_adress_details_ending + 1 : len(item_adress_details) - 1]
                    in_point_item_minutes_for_subway = item_minutes_for_subway.index(" ")
                    item_minutes_for_subway = int(item_minutes_for_subway[: in_point_item_minutes_for_subway])
                except ValueError:
                    item_minutes_for_subway = 'not stated'

                # площадь квартиры и кухни
                in_point_item_name_beginning = item_name.index(" ")
                in_point_item_name_ending = item_name[::-1].index(" ")
                squares = item_name[in_point_item_name_beginning + 1 : len(item_name) - (in_point_item_name_ending + 1)]

                in_point_squares_beginning = squares.index("/")
                appartment_square = float(squares[0 : in_point_squares_beginning])
                in_point_squares_ending = squares[::-1].index("/")
                appartment_kitchen_square = float(squares[len(squares) - in_point_squares_ending :])

                appartment_info = div.find_all('li') # список li элементов, через которые берётся информация ниже

                # этаж квартиры и дома
                appartment_floors_info = appartment_info[0].text

                in_point_appartment_floors_info_sliced = appartment_floors_info.index("-")
                appartment_floors_info = appartment_floors_info[: in_point_appartment_floors_info_sliced]

                in_point_appartment_floors_info_beginning = appartment_floors_info.index(" ")
                appartment_floor = int(appartment_floors_info[0 : in_point_appartment_floors_info_beginning])
                in_point_appartment_floors_info_ending = appartment_floors_info[::-1].index(" ")
                appartment_floors_in_building = int(appartment_floors_info[len(appartment_floors_info) - in_point_appartment_floors_info_ending :])

                # наличие балкона или лоджии
                appartment_balcony_lodge = appartment_info[1].text
                if appartment_balcony_lodge.find("балкон") != -1 or appartment_balcony_lodge.find("лоджия") != -1:
                    appartment_balcony_lodge = True
                else:
                    appartment_balcony_lodge = False

                # тип ремонта
                if appartment_balcony_lodge:
                    appartment_renovation_type = appartment_info[2].text
                else:
                    appartment_renovation_type = appartment_info[1].text
                in_point_appartment_renovation_type = appartment_renovation_type.index(" ")
                appartment_renovation_type = appartment_renovation_type[in_point_appartment_renovation_type + 1 : ]

                if appartment_renovation_type == "требуется ремонт" or appartment_renovation_type == "без отделки":
                    appartment_renovation_type = "нет ремонта"
                elif appartment_renovation_type == "косметический" or appartment_renovation_type == "под чистовую":
                    appartment_renovation_type = "эконом"
                else:
                    appartment_renovation_type = "улучшенный"

                file.close()

                # словарь с ключом в виде названия квартиры и значением в виде списка переменных
                all_appartments_dict[item_name] = [ item_href,                              # ссылка / string
                                                    item_price,                             # цена / int
                                                    item_adress,                            # адрес / string
                                                    item_minutes_for_subway,                # кол-во минут до метро / int
                                                    item_rooms_number,                      # количество комнат / int
                                                    appartment_square,                      # общая площадь квартиры / float
                                                    appartment_kitchen_square,              # площадь кухни / float
                                                    appartment_floor,                       # этаж квартиры / int
                                                    appartment_floors_in_building,          # этажность дома / int
                                                    appartment_balcony_lodge,               # наличие балкона или лоджии / bool
                                                    appartment_renovation_type,             # тип ремонта / string
                                                    ]
            
            time.sleep(random.randrange(4, 6))
        time.sleep(random.randrange(10, 20))
        end += 5; starter += 5
        print(f"процент выполениния: {persent}%")
        return parcer(starter, end, all_appartments_dict, pages)


# for i in (all_appartments_dict):
#     list_of_values = all_appartments_dict[i]
#     print(list_of_values)
    
# print(f'Всего квартир пропарсено: {len(all_appartments_dict)}')
# print(type(all_appartments_dict))
x = parcer(starter, end, all_appartments_dict, pages)
print(x)
print('кол-во пропаршеных квартир:', len(x))