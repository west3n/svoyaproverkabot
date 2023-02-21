import requests
import json


def json_parse(inn):
    url = f'https://api.damia.ru/spk/report?req={inn}&sections=fns,bals,checks,rels,isps,arbs,zakupki,scoring&format=' \
          'json&key=515ef887d6b2f0008dc4a7e96d8158671a961f27'
    response = requests.get(url)
    data = json.loads(response.text)
    if str(data)[:25] == "{'ФНС': {'items': [{'ЮЛ':":
        try:
            short_name = data["ФНС"]["items"][0]["ЮЛ"]["НаимСокрЮЛ"]
        except:
            short_name = 'Нет данных'
        try:
            inn = data["ФНС"]["items"][0]["ЮЛ"]["ИНН"]
        except:
            inn = 'Нет данных'
        try:
            ogrn = data["ФНС"]["items"][0]["ЮЛ"]["ОГРН"]
        except:
            ogrn = 'Нет данных'
        try:
            director = data["ФНС"]["items"][0]["ЮЛ"]["Руководитель"]["ФИОПолн"]
        except:
            director = 'Нет данных'
        try:
            contacts = data["ФНС"]["items"][0]["ЮЛ"]["Контакты"]
        except:
            contacts = 'Нет данных'
        try:
            authorized_capital = data["ФНС"]["items"][0]["ЮЛ"]["Капитал"]["СумКап"]
        except:
            authorized_capital = 'Нет данных'
        try:
            okved = data["ФНС"]["items"][0]["ЮЛ"]["ОснВидДеят"]["Текст"]
        except:
            okved = 'Нет данных'
        try:
            date_open = data["ФНС"]["items"][0]["ЮЛ"]["ДатаРег"]
        except:
            date_open = 'Нет данных'
        try:
            address = data["ФНС"]["items"][0]["ЮЛ"]["Адрес"]["АдресПолн"]
        except:
            address = 'Нет данных'
        try:
            balance = str(data["Отчетность"]['2021']['1600']) + " руб."
        except:
            balance = 'Нет данных'
        try:
            income = str(data["Отчетность"]['2021']['2110']) + " руб."
        except:
            income = 'Нет данных'
        try:
            profit = str(data["Отчетность"]['2021']['2400']) + " руб."
        except:
            profit = 'Нет данных'
        try:
            usn_osno = data["ФНС"]["items"][0]["ЮЛ"]["ОткрСведения"]["СведСНР"]
        except:
            usn_osno = "Нет данных"
        try:
            workers_amount = data["ФНС"]["items"][0]["ЮЛ"]["ОткрСведения"]["КолРаб"]
        except:
            workers_amount = "Нет данных"

        lic_org_list = []
        try:
            for lic in data["ФНС"]["items"][0]["ЮЛ"]["Лицензии"]:
                lic_org_list.append(lic["ЛицОрг"])
        except:
            lic_org_list = ['Нет лицензий']

        lic_org_str = "\n".join(lic_org_list)

        return [short_name, inn, ogrn, director, contacts,
                authorized_capital, okved, date_open, address, balance,
                income, profit, usn_osno, workers_amount, lic_org_str, data]

    elif str(data)[:25] == "{'ФНС': {'items': [{'ИП':":
        try:
            short_name = data["ФНС"]["items"][0]["ИП"]["ФИОПолн"]
        except:
            short_name = 'Нет данных'
        try:
            status = data["ФНС"]["items"][0]["ИП"]["СтатусИП"]
        except:
            status = 'Нет данных'
        try:
            inn = data["ФНС"]["items"][0]["ИП"]["ИННФЛ"]
        except:
            inn = 'Нет данных'
        try:
            ogrn = data["ФНС"]["items"][0]["ИП"]["ОГРНИП"]
        except:
            ogrn = 'Нет данных'
        try:
            okved = data["ФНС"]["items"][0]["ИП"]["ОснВидДеят"]["Текст"]
        except:
            okved = 'Нет данных'
        try:
            date_open = data["ФНС"]["items"][0]["ИП"]["ДатаРег"]
        except:
            date_open = 'Нет данных'
        return short_name, status, inn, ogrn, okved, date_open, data


def format_number(num):
    if num >= 10 ** 9:
        return f"{num / 10 ** 9:.2f} млрд."
    elif num >= 10 ** 6:
        return f"{num / 10 ** 6:.2f} млн."
    elif num >= 10 ** 3:
        return f"{num / 10 ** 3:.2f} тыс."
    else:
        return str(num)


def check_text(info):
    if info[9]:
        try:
            capital = format_number(float(info[5]))
        except:
            capital = 'Нет данных'
        if str(info[4]) != "[]":

            output = ""
            for contact in info[4]:
                output += f"<em>{contact}:</em> <b>{','.join(info[4][contact])}</b>\n"

        else:
            output = '<em>Контакты:</em><b> Нет данных</b>\n'
        text = (f'<em>Краткое наименование:</em> <b> {info[0]} </b> \n'
                f'<em>ИНН:</em> <b>{info[1]}</b>\n'
                f'<em>ОГРН:</em><b> {info[2]}</b>\n'
                f'<em>Руководитель организации:</em> <b>{info[3]}</b>\n'
                f'{output}'
                f'<em>Уставной капитал:</em> <b>{capital}</b>\n'
                f'<em>Основной вид деятельности:</em> <b>{info[6]}</b>\n'
                f'<em>Дата регистрации:</em> <b>{info[7]}</b>\n'
                f'<em>Юридический адрес:</em> <b> {info[8]}</b>\n'
                f'<em>Баланс</em>: <b>{info[9]}</b>\n'
                f'<em>Выручка:</em> <b>{info[10]}</b>\n'
                f'<em>Чистая прибыль</em>: <b>{info[11]}</b>\n'
                f'<em>УСН/ОСНО:</em> <b>{info[12]}</b>\n'
                f'<em>Количество сотрудников:</em> <b>{info[13]}</b>\n'
                f'<em>Госзакупки: </em>\n'
                f'<em>Лицензии:</em> <b>{info[14]}</b>\n'
                f'<em>Арбитраж: </em>\n'
                f'<em>ФССП: </em>')
        return text
    else:
        text = (f'<em>ФИО:</em> <b> {info[0]} </b> \n\n'
                f'<em>Статус:</em> <b> {info[1]} </b> \n\n'
                f'<em>ИНН:</em> <b>{info[2]}</b>\n\n'
                f'<em>ОГРН:</em><b> {info[3]}</b>\n\n'
                f'<em>Основной вид деятельности:</em> <b>{info[4]}</b>\n\n'
                f'<em>Дата регистрации:</em> <b>{info[5]}</b>')
        return text
