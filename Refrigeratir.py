from datetime import datetime, date, timedelta
from decimal import Decimal

DATE_FORMAT = "%Y-%m-%d"
# goods = {}

goods = {
    "Яйца": [
        {"amount": Decimal("16"), "expiration_date": date(2024, 2, 29)},
        {"amount": Decimal("4"), "expiration_date": date(2024, 3, 29)},
    ],
    "Яйца гусиные": [
        {"amount": Decimal("1"), "expiration_date": date(2024, 2, 29)},
        {"amount": Decimal("4"), "expiration_date": date(2024, 2, 29)},
    ],
    "Морковь": [
        {"amount": Decimal("1.7"), "expiration_date": date(2024, 2, 29)},
        {"amount": Decimal("0.3"), "expiration_date": date(2023, 8, 6)},
    ],
}


def add(items, title, amount, expiration_date=None):
    if expiration_date is not None:
        date_as_datetime = datetime.strptime(expiration_date, DATE_FORMAT)
        expiration_date = datetime.date(date_as_datetime)
    if title not in items:
        items[title] = [{"amount": amount, "expiration_date": expiration_date}]
    else:
        batch_list = dict.pop(items, title)  # Список партий продуктов
        batch_list.append({
            "amount": amount, "expiration_date": expiration_date
            })
        items[title] = batch_list


def add_by_note(items, note):
    list_from_str = note.split()  # Split строки по разделмтелю пробел.
    last_element_value = list_from_str[-1]
    last_value = last_element_value.split(
        "-"
    )  # Сплитуем последний элемент, проверяем на дату по '-'.
    if len(last_value) == 3:  # Если после сплита 3 элемента, значит это дата.
        expiration_date = list_from_str[-1]  # Последний == дата
        amount = Decimal(list_from_str[-2])  # Предпоследний == amount
        title = " ".join(
            list_from_str[:-2]
        )  # Собираем название (:-2 значит что -2 не включено в диапазон)
    else:
        expiration_date = None  # Date == None
        amount = Decimal(list_from_str[-1])  # amount is last element.
        title = " ".join(
            list_from_str[:-1]
        )  # Собираем название (:-1 значит что -1 не включено в диапазон)
    add(items, title, amount, expiration_date)


def find(items, needle):  # Поиск по названию продукта.
    needle_lower = needle.lower()  # Нижний регистр для запроса
    found_products = []
    for title in items:
        title_lower = title.lower()  # Нижний регистр для проверяющей строки
        if (
            title_lower.find(needle_lower) > -1
        ):  # Поиск подстроки в title если зн-е > 0, то True
            found_products.append(title)
    return found_products


def amount(items, needle):
    count = Decimal("0")
    product_list = find(items, needle)  # Получаем список продуктов
    for needle_product in product_list:
        # items_value = items[needle_product]  # Получаем список партий закупок
        for batch in items[needle_product]:  # Прогоняем партии закупок
            count += batch["amount"]  # Количество продукта в Decimal
    return count


def expire(items, in_advance_days=0):
    result = []
    today = date.today()
    print(today)
    expiration_date = timedelta(days=in_advance_days) + today
    for name_of_product in items:
        count = Decimal("0")
        for batches_of_products in items[name_of_product]:
            if (
                batches_of_products["expiration_date"] is not None
                and expiration_date >= batches_of_products["expiration_date"]
            ):
                count += batches_of_products["amount"]
        if count > 0:
            result.append((name_of_product, count))
    return result


# print(expire(goods))
# print(expire(goods, 100))
# print(expire(goods, 2))

# print(amount(goods, 'яйца'))
# print(amount(goods, 'морковь'))
# print(amount(goods, 'МоРкоВь'))
# print(amount(goods, 'Яйца'))
# print(amount(goods, 'Яйца гусиные'))

# print(find(goods, 'ЯйЦа'))

# add_by_note(goods, ' Пельмени Сибирская Коллекция 10  1000-10-10')
# add_by_note(goods, 'Яйца гусиные 4 2023-07-15')
# add_by_note(goods, 'Яйца гусиные 4')

# add(goods, 'Яйца', Decimal('10'), '2024-2-25')
# add(goods, 'Яйца', Decimal('3'), '2023-10-15')
# add(goods, 'Вода', Decimal('2.5'))
