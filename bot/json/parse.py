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

        return short_name, inn, ogrn, director, contacts, authorized_capital, okved, date_open, address, data

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
        output = ""
        for contact in info[4]:
            try:
                output += f"<em>{contact}:</em> <b>{','.join(info[4][contact])}</b>\n\n"
            except:
                output = 'Нет данных'

            text = (f'<em>Краткое наименование:</em> <b> {info[0]} </b> \n\n'
                    f'<em>ИНН:</em> <b>{info[1]}</b>\n\n'
                    f'<em>ОГРН:</em><b> {info[2]}</b>\n\n'
                    f'<em>Руководитель организации:</em> <b>{info[3]}</b>\n\n'
                    f'{output}'
                    f'<em>Уставной капитал:</em> <b>{capital}</b>\n\n'
                    f'<em>Основной вид деятельности:</em> <b>{info[6]}</b>\n\n'
                    f'<em>Дата регистрации:</em> <b>{info[7]}</b>\n\n'
                    f'<em>Юридический адрес:</em> <b> {info[8]}</b>')

            return text
    else:
        text = (f'<em>ФИО:</em> <b> {info[0]} </b> \n\n'
                f'<em>Статус:</em> <b> {info[1]} </b> \n\n'
                f'<em>ИНН:</em> <b>{info[2]}</b>\n\n'
                f'<em>ОГРН:</em><b> {info[3]}</b>\n\n'
                f'<em>Основной вид деятельности:</em> <b>{info[4]}</b>\n\n'
                f'<em>Дата регистрации:</em> <b>{info[5]}</b>')
        return text
