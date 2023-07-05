import requests
import json
import locale
from collections import Counter


def json_parse(inn):
    url = f'https://api.damia.ru/spk/report?req={inn}&sections=fns,bals,checks,rels,isps,arbs,zakupki,scoring,rnp' \
          f'&format=json&key=515ef887d6b2f0008dc4a7e96d8158671a961f27'
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
        except:
            bankruptcy = "Нет данных"
        try:
            solvency = '{:.3}'.format(data["Скоринг"]["Риски"]["РискПроблемнКред"]["2021"]["РискЗнач"] * 100)
        except:
            solvency = "Нет данных"
        try:
            fz115 = '{:.3}'.format(data["Скоринг"]["Риски"]["Риск115ФЗ"]["2021"]["РискЗнач"] * 100)
        except:
            fz115 = "Нет данных"
        try:
            smsp = data["Закупки"]['ЕРУЗ']['СМСП']
            if smsp:
                smsp = '├✅ <em>СМСП:</em> <b>ДА</b>'
            else:
                smsp = '├❌ <em>СМСП:</em> <b>НЕТ</b>'
        except(KeyError, TypeError):
            smsp = '├❌ <em>СМСП:</em> <b>НЕТ</b>'
        try:
            eruz = data["Закупки"]['ЕРУЗ']['Исключен']
            if not eruz:
                eruz = '├✅ <em>ЕРУЗ:</em> <b>ДА</b>'
            else:
                eruz = '├❌ <em>ЕРУЗ:</em> <b>НЕТ</b>'
        except(KeyError, TypeError):
            eruz = '├✅ <em>ЕРУЗ:</em> <b>ДА</b>'
        try:
            rnp = data["РНП"]['Текст']
            if rnp == 'Найдены записи в РНП':
                rnp_str = f'├❌ <em>РНП:</em> <b>{rnp}</b>'
            else:
                rnp_str = f'├✅ <em>РНП:</em> <b>{rnp}</b>'
        except(KeyError, TypeError):
            rnp_str = '├<em>РНП:</em> <b>Нет данных</b>'
        return [short_name, inn, ogrn, director, contacts,
                authorized_capital, okved, date_open, address, balance_2021, balance_2020, balance_2019,
                income_2021, income_2020, income_2019, profit_2021, profit_2020, profit_2019, usn_osno, workers_amount,
                gos_zak, lic_org_str, fssp, account_block, data, arbitration_defendant_sum,
                arbitration_defendant_amount, arbitration_claimant_sum, arbitration_claimant_amount,
                bankruptcy, solvency, fz115, founders_str, smsp, eruz, rnp_str]
    elif str(data)[:25] == "{'ФНС': {'items': [{'ИП':":
        try:
            short_name = data["ФНС"]["items"][0]["ИП"]["ФИОПолн"]
        except (KeyError, TypeError):
            short_name = 'Нет данных'
        try:
            inn = data["ФНС"]["items"][0]["ИП"]["ИННФЛ"]
        except (KeyError, TypeError):
            inn = 'Нет данных'
        try:
            ogrn = data["ФНС"]["items"][0]["ИП"]["ОГРНИП"]
        except (KeyError, TypeError):
            ogrn = 'Нет данных'
        try:
            okved = 'Нет данных'
            for x in range(0, 4):
                try:
                    okved = data["ФНС"]["items"][x]["ИП"]['ОснВидДеят']['Текст']
                except (KeyError, TypeError, IndexError):
                    pass
        except (KeyError, TypeError):
            okved = 'Нет данных'
        try:
            contacts = data["ФНС"]["items"][0]["ИП"]["Контакты"]
        except (KeyError, TypeError):
            contacts = 'Нет данных'
        try:
            date_open = data["ФНС"]["items"][0]["ИП"]['ДатаРег']
        except (KeyError, TypeError):
            date_open = 'Нет данных'
        try:
            address = data["ФНС"]["items"][0]["ИП"]['Адрес']['АдресПолн']
        except (KeyError, TypeError):
            address = 'Нет данных'
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
                gos_zak = f"Участник - {total_sum} ({total_amount}) | Контракт заключен - " \
                          f"{format_number(contracts1_sum + contracts2_sum)} ({contracts1_amount + contracts2_amount})"
        except (KeyError, TypeError):
            gos_zak = "Нет госзакупок"
        lic_org_list = []
        try:
            for lic in data["ФНС"]["items"][0]["ИП"]["Лицензии"]:
                lic_org_list.append(lic["ЛицОрг"])
        except (KeyError, TypeError):
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
            arbitration_claimant_amount = 0
            for year in data["Арбитражи"]["Сводка"]["Истец"]:
                arbitration_claimant_amount += data["Арбитражи"]["Сводка"]["Истец"][year]["Итого"]["Количество"]
        except(KeyError, TypeError):
            arbitration_claimant_amount = "Нет данных"
        try:
            arbitration_claimant_sum = 0
            for year in data["Арбитражи"]["Сводка"]["Истец"]:
                arbitration_claimant_sum += data["Арбитражи"]["Сводка"]["Истец"][year]["Итого"]["Сумма"]
        except(KeyError, TypeError):
            arbitration_claimant_sum = "Нет данных"
        try:
            arbitration_defendant_amount = 0
            for year in data["Арбитражи"]["Сводка"]["Ответчик"]:
                arbitration_defendant_amount += data["Арбитражи"]["Сводка"]["Ответчик"][year]["Итого"]["Количество"]
        except(KeyError, TypeError):
            arbitration_defendant_amount = "Нет данных"
        try:
            arbitration_defendant_sum = 0
            for year in data["Арбитражи"]["Сводка"]["Ответчик"]:
                arbitration_defendant_sum += data["Арбитражи"]["Сводка"]["Ответчик"][year]["Итого"]["Сумма"]
        except(KeyError, TypeError):
            arbitration_defendant_sum = "Нет данных"
        try:
            account_block = data["ПроверкиФНС"]["items"][0]["ИП"]["Негатив"]["БлокСчета"]
            if 'Да' in account_block:
                account_block = 'Да'
        except(KeyError, TypeError):
            account_block = "Нет"
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
        except(KeyError, TypeError):
            fssp = "Нет данных"
        try:
            smsp = data["Закупки"]['ЕРУЗ']['СМСП']
            if smsp:
                smsp = '├✅ <em>СМСП:</em> <b>ДА</b>'
            else:
                smsp = '├❌ <em>СМСП:</em> <b>НЕТ</b>'
        except(KeyError, TypeError):
            smsp = '├❌ <em>СМСП:</em> <b>НЕТ</b>'
        try:
            eruz = data["Закупки"]['ЕРУЗ']['Исключен']
            if not eruz:
                eruz = '├✅ <em>ЕРУЗ:</em> <b>ДА</b>'
            else:
                eruz = '├❌ <em>ЕРУЗ:</em> <b>НЕТ</b>'
        except(KeyError, TypeError):
            eruz = '├✅ <em>ЕРУЗ:</em> <b>ДА</b>'
        try:
            rnp = data["РНП"]['Текст']
            if rnp == 'Найдены записи в РНП':
                rnp_str = f'├❌ <em>РНП:</em> <b>{rnp}</b>'
            else:
                rnp_str = f'├✅ <em>РНП:</em> <b>{rnp}</b>'
        except(KeyError, TypeError):
            rnp_str = '├<em>РНП:</em> <b>Нет данных</b>'
        return [data, short_name, inn, ogrn, contacts, okved, date_open, address, gos_zak, lic_org_str,
                arbitration_defendant_sum, arbitration_defendant_amount, arbitration_claimant_sum,
                arbitration_claimant_amount, account_block, fssp, smsp, eruz, rnp_str]


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


def format_lights(info: float):
    if info <= 33:
        info = f'🟢 {info}%'
    elif info >= 66:
        info = f'🔴 {info}%'
    else:
        info = f'🟡 {info}%'
    return info


def get_api_data(name):
    url = f'http://89.108.118.100:8000/api/v2/complaints/?complaint_id=&date_after=&date_before=&region=' \
          f'&customer_name=&customer_inn=&complainant_name={name}&complainant_inn=' \
          f'&numb_purchase=&docs_complaints=&docs_solutions=&docs_prescriptions=&docs_complaints_2=' \
          f'&docs_solutions_2=&docs_prescriptions_2='
    response = requests.get(url)
    data = json.loads(response.text)
    count = data['count']
    try:
        complaint_id = data['results'][0]['complaint_id']
        phone_number = data['results'][0]['json_data'][f'{complaint_id}']['section_card_common_dict'][
            'Данные участника контрактной системы в сфере закупок, подавшего жалобу']['Номер телефона']
    except (IndexError, KeyError):
        phone_number = None
    try:
        complaint_id = data['results'][0]['complaint_id']
        email = data['results'][0]['json_data'][f'{complaint_id}']['section_card_common_dict'][
            'Данные участника контрактной системы в сфере закупок, подавшего жалобу']['Адрес электронной почты']
    except (IndexError, KeyError):
        email = None
    return phone_number, email, count


def check_text(info):
    emoji = "❌" if info[21] == 'Нет лицензий' else "✅"
    license_str = f'├<em>{emoji} Лицензии:</em> <b>{info[21]}</b>\n'
    emoji = "✅" if info[23] == "Нет" else "❌"
    accounts_str = f'├<em>{emoji} Блокировка счетов:</em> <b>{info[23]}</b>\n'
    emoji = "❌" if info[20] == 'Нет госзакупок' else "✅"
    gos_zak_str = f'├<em>{emoji} Госзакупки:</em> <b>{info[20]} </b>\n'
    emoji = "✅" if info[22] == 'К взысканию - 0 руб. (0)' else "❌"
    fssp_str = f'├<em>{emoji} ФССП:</em> <b>{info[22]}</b>\n'
    emoji = "❌" if info[8] == 'Нет данных' else "✅"
    address_str = f'├<em>{emoji} Юридический адрес:</em> <b> {info[8]}</b>\n'
    emoji = "❌" if info[19] == 'Нет данных' else "✅"
    workers_amount_str = f'├<em>{emoji} Количество сотрудников:</em> <b>{info[19]}</b>\n'
    count = get_api_data(info[0].replace('"', "'"))[2]
    emoji = "❌" if info[9] == 'Нет данных' or info[12] == 'Нет данных' or info[15] == 'Нет данных' else "✅"
    balance_2021_str = f'├<b>{emoji} 2021 (тыс.руб)</b>:\n'
    emoji = "❌" if info[10] == 'Нет данных' or info[13] == 'Нет данных' or info[16] == 'Нет данных' else "✅"
    balance_2020_str = f'├<b>{emoji} 2020 (тыс.руб)</b>:\n'
    emoji = "❌" if info[11] == 'Нет данных' or info[14] == 'Нет данных' or info[17] == 'Нет данных' else "✅"
    balance_2019_str = f'├<b>{emoji} 2019 (тыс.руб)</b>:\n'
    for index in [25, 27, 29, 30, 31]:
        if info[index] != "Нет данных":
            if index in [25, 27]:
                info[index] = format_number(info[index])
            else:
                info[index] = format_lights(float(info[index]))
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
                f'{address_str}'
                f'{balance_2021_str}'
                f'├<em>Баланс</em>: <b>{info[9]}</b>\n'
                f'├<em>Выручка:</em> <b>{info[12]}</b>\n'
                f'├<em>Чистая прибыль</em>: <b>{info[15]}</b>\n'
                f'{balance_2020_str}'
                f'├<em>Баланс</em>: <b>{info[10]}</b>\n'
                f'├<em>Выручка:</em> <b>{info[13]}</b>\n'
                f'├<em>Чистая прибыль</em>: <b>{info[16]}</b>\n'
                f'{balance_2019_str}'
                f'├<em>Баланс</em>: <b>{info[11]}</b>\n'
                f'├<em>Выручка:</em> <b>{info[14]}</b>\n'
                f'├<em>Чистая прибыль</em>: <b>{info[17]}</b>\n'
                f'├<em>Налоговый режим:</em> <b>{info[18]}</b>\n'
                f'{workers_amount_str}'
                f'{gos_zak_str}'
                f'{license_str}'
                f'├<em>Арбитражи:</em> <b>Ответчик - {info[25]} ({info[26]}) | Истец - {info[27]} ({info[28]})</b>\n'
                f'{accounts_str}'
                f'{fssp_str}'
                f'{info[33]}\n'
                f'{info[35]}\n'
                f'{info[34]}\n'
                f'├<em>Жалобы:</em> <b>{count}</b>\n'
                f'├<b>Скоринг:</b>\n'
                f'├<em>Банкротство:</em> <b>{info[29]}</b>\n'
                f'├<em>Платежеспособность:</em> <b>{info[30]}</b>\n'
                f'├<em>ФЗ-115:</em> <b>{info[31]}</b>\n'
                f'├<b><a href="https://svoya-proverka.ru/scoring/?ogrn={info[1]}">'
                f'Здесь </a>ссылка на полную версию на сайте</b>')
        return text


def check_text_2(info):
    emoji = "❌" if info[9] == 'Нет лицензий' else "✅"
    license_str = f'├<em>{emoji} Лицензии:</em> <b>{info[9]}</b>\n'
    emoji = "✅" if info[14] == "Нет" else "❌"
    accounts_str = f'├<em>{emoji} Блокировка счетов:</em> <b>{info[14]}</b>\n'
    emoji = "❌" if info[8] == 'Нет госзакупок' else "✅"
    gos_zak_str = f'├<em>{emoji} Госзакупки:</em> <b>{info[8]} </b>\n'
    emoji = "✅" if info[15] == 'К взысканию - 0 руб. (0)' else "❌"
    fssp_str = f'├<em>{emoji} ФССП:</em> <b>{info[15]}</b>\n'
    emoji = "❌" if info[7] == 'Нет данных' else "✅"
    address_str = f'├<em>{emoji} Адрес:</em> <b> {info[7]}</b>\n'
    for index in [10, 12]:
        if info[index] != "Нет данных":
            info[index] = format_number(info[index])
    count = get_api_data(info[1])[2]
    if info[4]:
        email_list = []
        try:
            email_1 = info[4]['e-mail'][0]
        except KeyError:
            email_1 = 'Нет данных'
        except TypeError:
            email_1 = 'Нет данных'
        email_list.append(email_1)
        email_2 = get_api_data(info[1])[1]
        if email_2:
            email_list.append(email_2)
        phone_number = get_api_data(info[1])[0] if get_api_data(info[1])[0] else 'Нет данных'
        output = f"<em>Контакты:</em>\n" \
                 f"├<em>Email:</em><b> {', '.join(email_list)}</b>\n" \
                 f"├<em>Номер телефона:</em><b> {phone_number}</b>\n"
    else:
        output = '<em>Контакты:</em><b> Нет данных</b>\n'
    text = (f'🟢<em>ИП:</em> <b> {info[1]} </b> \n'
            f'├<em>ИНН:</em> <b>{info[2]}</b>\n'
            f'├<em>ОГРН:</em><b> {info[3]}</b>\n'
            f'{output}'
            f'├<em>Основной вид деятельности:</em> <b>{info[5]}</b>\n'
            f'├<em>Дата регистрации:</em> <b>{info[6] if info[6] else "Нет данных"}</b>\n'
            f'{address_str}'
            f'{gos_zak_str}'
            f'{license_str}'
            f'├<em>Арбитражи:</em> <b>Ответчик - {info[10]} ({info[11]}) | Истец - {info[12]} ({info[13]})</b>\n'
            f'{accounts_str}'
            f'{fssp_str}'
            f'{info[16]}\n'
            f'{info[18]}\n'
            f'{info[17]}\n'
            f'├Жалобы: {count}\n'
            f'├<b><a href="https://svoya-proverka.ru/scoring/?ogrn={info[3]}">'
            f'Здесь </a>ссылка на полную версию на сайте</b>')
    return text
