import requests
import json
import locale
from collections import Counter


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
        founders = []
        for item in data.get("ФНС", {}).get("items", []):
            for founder in item.get("ЮЛ", {}).get("Учредители", []):
                if "УчрФЛ" in founder:
                    founders.append(founder["УчрФЛ"].get("ФИОПолн"))
                elif "УчрЮЛ" in founder:
                    founders.append(founder["УчрЮЛ"].get("НаимСокрЮЛ"))

        founders = [founder for founder in founders if founder is not None]
        if not founders:
            founders_str = "Нет данных"
        else:
            founders_str = ", ".join(founders)
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
            balance_2021 = format(data["Отчетность"]['2021']['1600'], ',').replace(',', ' ')
        except:
            balance_2021 = 'Нет данных'
        try:
            balance_2020 = format(data["Отчетность"]['2020']['1600'], ',').replace(',', ' ')
        except:
            balance_2020 = 'Нет данных'
        try:
            balance_2019 = format(data["Отчетность"]['2019']['1600'], ',').replace(',', ' ')
        except:
            balance_2019 = 'Нет данных'
        try:
            income_2021 = format(data["Отчетность"]['2021']['2110'], ',').replace(',', ' ')
        except:
            income_2021 = 'Нет данных'
        try:
            income_2020 = format(data["Отчетность"]['2020']['2110'], ',').replace(',', ' ')
        except:
            income_2020 = 'Нет данных'
        try:
            income_2019 = format(data["Отчетность"]['2019']['2110'], ',').replace(',', ' ')
        except:
            income_2019 = 'Нет данных'
        try:
            profit_2021 = format(data["Отчетность"]['2021']['2400'], ',').replace(',', ' ')
        except:
            profit_2021 = 'Нет данных'
        try:
            profit_2020 = format(data["Отчетность"]['2020']['2400'], ',').replace(',', ' ')
        except:
            profit_2020 = 'Нет данных'
        try:
            profit_2019 = format(data["Отчетность"]['2019']['2400'], ',').replace(',', ' ')
        except:
            profit_2019 = 'Нет данных'
        try:
            usn_osno = data["ФНС"]["items"][0]["ЮЛ"]["ОткрСведения"]["СведСНР"]
            if usn_osno == "Нет":
                usn_osno = "ОСНО"
        except:
            usn_osno = "ОСНО"
        try:
            workers_amount = data["ФНС"]["items"][0]["ЮЛ"]["ОткрСведения"]["КолРаб"]
        except:
            workers_amount = "Нет данных"
        try:
            purchase_sum = 0
            for year in data["Закупки"]["Сводка"]["44_223"]["Закупки"]:
                if "Закупка завершена" in data["Закупки"]["Сводка"]["44_223"]["Закупки"][year]:
                    for item in data["Закупки"]["Сводка"]["44_223"]["Закупки"][year]["Закупка завершена"]["Цена"]:
                        purchase_sum += item["Сумма"]
            purchase_amount = 0
            for year in data["Закупки"]["Сводка"]["44_223"]["Закупки"]:
                if "Закупка завершена" in data["Закупки"]["Сводка"]["44_223"]["Закупки"][year]:
                    for item in data["Закупки"]["Сводка"]["44_223"]["Закупки"][year]["Закупка завершена"]["Цена"]:
                        purchase_amount += item["Количество"]
            contracts1_sum = 0
            for year in data["Закупки"]["Сводка"]["44_223"]["Контракты"]:
                if "Исполнение завершено" in data["Закупки"]["Сводка"]["44_223"]["Контракты"][year]:
                    for item in data["Закупки"]["Сводка"]["44_223"]["Контракты"][year]["Исполнение завершено"]["Цена"]:
                        contracts1_sum += item["Сумма"]
            contracts1_amount = 0
            for year in data["Закупки"]["Сводка"]["44_223"]["Контракты"]:
                if "Исполнение завершено" in data["Закупки"]["Сводка"]["44_223"]["Контракты"][year]:
                    for item in data["Закупки"]["Сводка"]["44_223"]["Контракты"][year]["Исполнение завершено"]["Цена"]:
                        contracts1_amount += item["Количество"]
            contracts2_sum = 0
            for year in data["Закупки"]["Сводка"]["44_223"]["Контракты"]:
                if "Исполнение прекращено" in data["Закупки"]["Сводка"]["44_223"]["Контракты"][year]:
                    for item in data["Закупки"]["Сводка"]["44_223"]["Контракты"][year]["Исполнение прекращено"]["Цена"]:
                        contracts2_sum += item["Сумма"]
            contracts2_amount = 0
            for year in data["Закупки"]["Сводка"]["44_223"]["Контракты"]:
                if "Исполнение прекращено" in data["Закупки"]["Сводка"]["44_223"]["Контракты"][year]:
                    for item in data["Закупки"]["Сводка"]["44_223"]["Контракты"][year]["Исполнение прекращено"]["Цена"]:
                        contracts2_amount += item["Количество"]

            total_sum = format_number(purchase_sum + contracts1_sum + contracts2_sum)
            total_amount = purchase_amount + contracts1_amount + contracts2_amount
            if total_sum and total_amount == 0:
                gos_zak = "Нет госзакупок"
            else:
                gos_zak = f"Участник - {total_sum} ({total_amount}) | Контракт заключен - {format_number(contracts1_sum + contracts2_sum)} ({contracts1_amount + contracts2_amount})"
        except:
            gos_zak = "Нет госзакупок"
        lic_org_list = []
        try:
            for lic in data["ФНС"]["items"][0]["ЮЛ"]["Лицензии"]:
                lic_org_list.append(lic["ЛицОрг"])
        except:
            lic_org_list = ['Нет лицензий']

        lic_org_counter = Counter(lic_org_list)
        lic_org_str = ""
        for key, value in lic_org_counter.items():
            if value > 1:
                lic_org_str += f"{key} ({value}),\n"
            else:
                lic_org_str += f"{key},\n"
        lic_org_str = lic_org_str.rstrip(",\n")
        try:
            fssp_sum = 0
            for year in data["ФССП"]["Сводка"]:
                for category in data["ФССП"]["Сводка"][year]["Не завершено"]:
                    if "Сумма" in data["ФССП"]["Сводка"][year]["Не завершено"][category]:
                        fssp_sum += data["ФССП"]["Сводка"][year]["Не завершено"][category]["Сумма"]
            fssp_amount = 0
            for year in data["ФССП"]["Сводка"]:
                for category in data["ФССП"]["Сводка"][year]["Не завершено"]:
                    if "Количество" in data["ФССП"]["Сводка"][year]["Не завершено"][category]:
                        fssp_amount += data["ФССП"]["Сводка"][year]["Не завершено"][category]["Количество"]
            if fssp_sum and fssp_amount == 0:
                fssp = "Нет данных"
            else:
                fssp = f"К взысканию - {format_number(fssp_sum)} ({fssp_amount})"
        except:
            fssp = "Нет данных"
        try:
            account_block = data["ПроверкиФНС"]["items"][0]["ЮЛ"]["Негатив"]["БлокСчета"]
            if 'Да' in account_block:
                account_block = 'Да'
        except:
            account_block = "Нет"
        try:
            arbitration_claimant_amount = 0
            for year in data["Арбитражи"]["Сводка"]["Истец"]:
                arbitration_claimant_amount += data["Арбитражи"]["Сводка"]["Истец"][year]["Итого"]["Количество"]
        except:
            arbitration_claimant_amount = "Нет данных"
        try:
            arbitration_claimant_sum = 0
            for year in data["Арбитражи"]["Сводка"]["Истец"]:
                arbitration_claimant_sum += data["Арбитражи"]["Сводка"]["Истец"][year]["Итого"]["Сумма"]
        except:
            arbitration_claimant_sum = "Нет данных"
        try:
            arbitration_defendant_amount = 0
            for year in data["Арбитражи"]["Сводка"]["Ответчик"]:
                arbitration_defendant_amount += data["Арбитражи"]["Сводка"]["Ответчик"][year]["Итого"]["Количество"]
        except:
            arbitration_defendant_amount = "Нет данных"
        try:
            arbitration_defendant_sum = 0
            for year in data["Арбитражи"]["Сводка"]["Ответчик"]:
                arbitration_defendant_sum += data["Арбитражи"]["Сводка"]["Ответчик"][year]["Итого"]["Сумма"]
        except:
            arbitration_defendant_sum = "Нет данных"
        try:
            bankruptcy = '{:.3}'.format(data["Скоринг"]["Риски"]["РискБанкр"]["2021"]["РискЗнач"] * 100)
            solvency = '{:.3}'.format(data["Скоринг"]["Риски"]["РискПроблемнКред"]["2021"]["РискЗнач"] * 100)
            fz115 = '{:.3}'.format(data["Скоринг"]["Риски"]["Риск115ФЗ"]["2021"]["РискЗнач"] * 100)

        except:
            bankruptcy = "Нет данных"
            solvency = "Нет данных"
            fz115 = "Нет данных"

        return [short_name, inn, ogrn, director, contacts,
                authorized_capital, okved, date_open, address, balance_2021, balance_2020, balance_2019,
                income_2021, income_2020, income_2019, profit_2021, profit_2020, profit_2019, usn_osno, workers_amount,
                gos_zak, lic_org_str, fssp, account_block, data, format_number(arbitration_defendant_sum),
                arbitration_defendant_amount, format_number(arbitration_claimant_sum), arbitration_claimant_amount,
                bankruptcy, solvency, fz115, founders_str]


def format_number(num: float):
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    if num >= 10 ** 9:
        result = f"{locale.format_string('%.1f', num / 10 ** 9, grouping=True).rstrip('0').rstrip('.')} млрд. руб."
        return result.replace(', ', ' ')
    elif num >= 10 ** 6:
        result = f"{locale.format_string('%.1f', num / 10 ** 6, grouping=True).rstrip('0').rstrip('.')} млн. руб."
        return result.replace(', ', ' ')
    elif num >= 10 ** 3:
        result = f"{locale.format_string('%.1f', num / 10 ** 3, grouping=True).rstrip('0').rstrip('.')} тыс. руб."
        return result.replace(', ', ' ')
    else:
        result = f"{locale.format_string('%.0f', num, grouping=True)} руб."
        return result.replace(', ', ' ')


def format_number_2(num: float):
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    if num >= 10 ** 6:
        result = f"{locale.format_string('%.1f', num / 10 ** 6, grouping=True).rstrip('0').rstrip('.')} млрд. руб."
        return result.replace(', ', ' ')
    elif num >= 10 ** 3:
        result = f"{locale.format_string('%.1f', num / 10 ** 3, grouping=True).rstrip('0').rstrip('.')} млн. руб."
        return result.replace(', ', ' ')
    else:
        result = f"{locale.format_string('%.1f', num, grouping=True).rstrip('0').rstrip('.')} тыс. руб."
        return result.replace(', ', ' ')


def check_text(info):
    if info[9]:
        try:
            capital = format_number(float(info[5]))
        except:
            capital = 'Нет данных'
        if str(info[4]) != "[]":

            output = ""
            for contact in info[4]:
                output += f"├<em>{contact}:</em> <b>{', '.join(info[4][contact])}</b>\n"

        else:
            output = '<em>Контакты:</em><b> Нет данных</b>\n'
        text = (f'🟢<em>Краткое наименование:</em> <b> {info[0]} </b> \n'
                f'├<em>ИНН:</em> <b>{info[1]}</b>\n'
                f'├<em>ОГРН:</em><b> {info[2]}</b>\n'
                f'├<em>Руководитель организации:</em> <b>{info[3]}</b>\n'
                f'├<em>Учредители: </em><b>{info[32]}</b>\n'
                f'{output}'
                f'├<em>Уставной капитал:</em> <b>{capital}</b>\n'
                f'├<em>Основной вид деятельности:</em> <b>{info[6]}</b>\n'
                f'├<em>Дата регистрации:</em> <b>{info[7]}</b>\n'
                f'├<em>Юридический адрес:</em> <b> {info[8]}</b>\n'
                f'├<b>2021 (тыс.руб)</b>:\n'
                f'├<em>Баланс</em>: <b>{info[9]}</b>\n'
                f'├<em>Выручка:</em> <b>{info[12]}</b>\n'
                f'├<em>Чистая прибыль</em>: <b>{info[15]}</b>\n'
                f'├<b>2020 (тыс.руб)</b>:\n'
                f'├<em>Баланс</em>: <b>{info[10]}</b>\n'
                f'├<em>Выручка:</em> <b>{info[13]}</b>\n'
                f'├<em>Чистая прибыль</em>: <b>{info[16]}</b>\n'
                f'├<b>2019 (тыс.руб)</b>:\n'
                f'├<em>Баланс</em>: <b>{info[11]}</b>\n'
                f'├<em>Выручка:</em> <b>{info[14]}</b>\n'
                f'├<em>Чистая прибыль</em>: <b>{info[17]}</b>\n'
                f'├<em>Налоговый режим:</em> <b>{info[18]}</b>\n'
                f'├<em>Количество сотрудников:</em> <b>{info[19]}</b>\n'
                f'├<em>Госзакупки:</em> <b>{info[20]} </b>\n'
                f'├<em>Лицензии:</em> <b>{info[21]}</b>\n'
                f'├<em>Арбитражи:</em> <b>Ответчик - {info[25]} ({info[26]}) | Истец - {info[27]} ({info[28]})</b>\n'
                f'├<em>Блокировка счетов:</em> <b>{info[23]}</b>\n'
                f'├<em>ФССП:</em> <b>{info[22]}</b>\n'
                f'├<b>Скоринг:</b>\n'
                f'├<em>Банкротство:</em> <b>{format_lights(float(info[29]))}</b>\n'
                f'├<em>Платежеспособность:</em> <b>{format_lights(float(info[30]))}</b>\n'
                f'├<em>ФЗ-115:</em> <b>{format_lights(float(info[31]))}</b>\n'
                f'├<b><a href="https://svoya-proverka.ru/scoring/?ogrn={info[1]}">Здесь </a>ссылка на полную версию на сайте</b>')
        return text
