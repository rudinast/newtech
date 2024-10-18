from datetime import datetime


def get_data_by_date(data: dict, target_date: datetime) -> float:
    """
    Возвращает данные для указанной даты. Если данных для этой даты нет, возвращает None.

    :param data: Словарь, где ключ — это дата, а значение — данные.
    :param target_date: Дата, для которой нужно получить данные.
    :return: Данные для указанной даты или None, если данных нет.
    """
    # Преобразуем дату в строку в формате 'YYYY-MM-DD' для поиска в словаре
    target_date_str = target_date.strftime('%Y-%m-%d')
    # Возвращаем данные для указанной даты, если они есть, иначе None
    return data.get(target_date_str, None)
