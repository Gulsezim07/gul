import json
import re


with open("row.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()   

receipt = {
    "Филиал": "EUROPHARMA Астана",
    "bin": "080841000761",
    "nds_series": "58001",
    "Касса": "300-189",
    "Смена": "10",
    "Порядковый_номер": "64",
    "Номер_чека": "2331180266",
    "Кассир": "Аптека 17-1",
    "Товары": [],
    "Всего": "18 009,00",
    "Банковская карта": "18 009,00",
    "В т.ч. НДС 12%": "0,00",
    "Фискальные признаки:":"2331180266",
    "Время":"18.04.2019 11:13:58",
    "Город":"г. Нур-султан,Казахстан, Мангилик Ел,19, нп-5",
    "Оператор фискальных данных": "АО  Казахтелеком Для проверки чека зайдите на сайт:consumer.oofd.kz",
    "ИНК ОФД":"311559",
    "Код ККМ КГД (РНМ)":"620300145316",
    "ЗНМ ":"SWK00034961"



}

item_id_pattern = re.compile(r"^(\d+)\.$")

price_quantity_pattern = re.compile(r"([\d\s]+),(\d+)\s+x\s+([\d\s]+),(\d+)")

i = 0
while i < len(lines):
    line = lines[i].strip()
    
    item_match = item_id_pattern.match(line)
    if item_match:
        item_id = item_match.group(1)
        i += 1  
        item_name = lines[i].strip()
        i += 1  
        
     
        price_quantity_match = price_quantity_pattern.search(lines[i])
        if price_quantity_match:
            price = price_quantity_match.group(1).replace(" ", "") + "." + price_quantity_match.group(2)
            quantity = price_quantity_match.group(3).replace(" ", "") + "." + price_quantity_match.group(4)
        
        i += 1  
        item_sum = lines[i].strip().replace(" ", "").replace(",", ".")

      
        receipt["Товары"].append({
            "id": item_id,
            "название": item_name,
            "цена": price,
            "кол-во": quantity,
            "сумма": item_sum
        })
    
    i += 1





with open("parsed_receipt.json", "w", encoding="utf-8") as json_file:
    json.dump(receipt, json_file, ensure_ascii=False, indent=4)

print("JSON-файл успешно создан")