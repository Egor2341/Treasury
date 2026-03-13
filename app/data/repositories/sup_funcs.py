def month_to_int(month: str):
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
              "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

    months_dict = {month: i + 1 for i, month in enumerate(months)}
    return months_dict[month]