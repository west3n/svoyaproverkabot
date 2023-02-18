import requests
import json


def json_parse(inn):
    url = f'https://api.damia.ru/spk/report?req={inn}&sections=fns,bals,checks,rels,isps,arbs,zakupki,scoring&format=' \
          'json&key=515ef887d6b2f0008dc4a7e96d8158671a961f27'
    response = requests.get(url)
    data = json.loads(response.text)
    short_name = data["ФНС"]["items"][0]["ЮЛ"]["НаимСокрЮЛ"]
    inn = data["ФНС"]["items"][0]["ЮЛ"]["ИНН"]
    ogrn = data["ФНС"]["items"][0]["ЮЛ"]["ОГРН"]
    director = data["ФНС"]["items"][0]["ЮЛ"]["Руководитель"]["ФИОПолн"]
    contacts = data["ФНС"]["items"][0]["ЮЛ"]["Контакты"]
    authorized_capital = data["ФНС"]["items"][0]["ЮЛ"]["Капитал"]["СумКап"]
    okved = data["ФНС"]["items"][0]["ЮЛ"]["ОснВидДеят"]["Текст"]
    date_open = data["ФНС"]["items"][0]["ЮЛ"]["ДатаРег"]
    address = data["ФНС"]["items"][0]["ЮЛ"]["Адрес"]["АдресПолн"]
    return short_name, inn, ogrn, director, contacts, authorized_capital, okved, date_open, address, data


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
    output = ""
    for contact in info[4]:
        output += f"<em>{contact}:</em> <b>{','.join(info[4][contact])}</b>\n\n"

    text = (f'<em>Краткое наименование:</em> <b> {info[0]} </b> \n\n'
            f'<em>ИНН:</em> <b>{info[1]}</b>\n\n'
            f'<em>ОГРН:</em><b> {info[2]}</b>\n\n'
            f'<em>Руководитель организации:</em> <b>{info[3]}</b>\n\n'
            f'{output}'
            f'<em>Уставной капитал:</em> <b>{format_number(float(info[5]))}</b>\n\n'
            f'<em>Основной вид деятельности:</em> <b>{info[6]}</b>\n\n'
            f'<em>Дата регистрации:</em> <b>{info[7]}</b>\n\n'
            f'<em>Юридический адрес:</em> <b> {info[8]}</b>')
    return text
