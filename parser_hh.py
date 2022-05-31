import requests
import pprint
from collections import Counter
from operator import itemgetter
import json
DOMAIN = 'https://api.hh.ru/'
url_vacancies = f'{DOMAIN}vacancies'

# def hhparser(proff = 'Python developer'):



def parser_hh(proff, pages):
    f = open('result_top_10.txt', 'w')
    f.write('')
    f.close()
    f = open('top_10.txt', 'w')
    f.write('')
    f.close()
    f = open('city_top_10.txt', 'w')
    f.write('')
    f.close()
    f = open('city_head_10.txt', 'w')
    f.write('')
    f.close()


    my_skill_list = []
    my_city_list = []
    total_skill = []
    total_skill1 = {}
    total_city = []
    main_count = 0
    new_new = []
    # modify_my_city_list = []
    # modify_skill_list = []
    if int(pages)<20:
        pages = 20
    if int(pages)>2000:
        pages = 2000
    page = int(int(pages)/20) #int(input('Сколько страниц анализировать? (мах 100): '))

    #Перебор страниц

    for page_count in range(page):

        print(f'Парсинг страницы {page_count+1}')
        params = {
            'text': proff,
            'page': page_count
        }
        page_count += 1
        vacancy_count = 0
        # Перебор 20 вакансий на странице
        for k in range(20):
            try:
                main_count += 1
                vacancy_count += 1
                #Сколько ваканский спарсили на текущей странице
                print(vacancy_count)
                #Вытаскиваем нужный url (где есть skill) для дальнейшей обработки
                result = requests.get(url_vacancies, params=params).json()
                url_skill = result['items'][k]['url']
                my_result = requests.get(url_skill).json()
                #Записываем Skill в список
                my_skill = my_result['key_skills']
                lens = len(my_skill)

                if len(my_skill) != 0:
                    for counter in range(lens):
                        my_skill_list.append(my_skill[counter]['name'])
                else: pass

                my_name = my_result['name']
                my_address = my_result['area']
                if my_address == None:
                    my_city = 'Неизвестно'

                else:
                    my_city = my_address['name']

                my_city_list.append(my_city)
            except:
                pass

        total_result = result['found']
        print(f'Всего {total_result} вакансий найдено')
        print(f'{main_count} вакансий {proff} спарсено')


    lens_skill_list = len(my_skill_list)
    lens_my_city_list = len(my_city_list)


    modify_skill_list = Counter(my_skill_list)
    modify_my_city_list = Counter(my_city_list)

    lens_end_skill = len(modify_skill_list)
    lens_end_city = len(modify_my_city_list)


    for counter in range(lens_end_skill):
        name = list(modify_skill_list.keys())[counter]
        count = list(modify_skill_list.values())[counter]
        path = count / lens_skill_list
        percent = '{percent:.1%}'.format(percent=path)
        total_skill.append({'name': name, 'percent': percent, 'count': count})
        combain = f'{name} {percent} {count}'
        total_skill1 = {counter: combain}

    total_skill = (sorted(total_skill, key=itemgetter('count'), reverse=True))
    print(type(total_skill))


    for counter1 in total_skill:
        print(counter1['name'], counter1['percent'], counter1['count'])
        name = counter1['name']
        percent = counter1['percent']
        count = counter1['count']
        new = f'{name} {percent} {count}'
        new_new.append(new)

    print('*' * 200)
    print(total_skill1)
    print('!' * 200)

    print('*' * 200)
    print(new_new)
    print('!' * 200)

    result_skill = {
            'keywords': proff,
            'count': str(lens_end_skill),
            'requirements': total_skill
            }
    result_skill_json = json.dumps(result_skill, ensure_ascii=False, indent=4)

    print(result_skill['keywords'], result_skill['count'], result_skill['requirements'])

    print('*' * 200)
    print(type(result_skill['requirements']))
    print(result_skill['requirements'])
    print('*' * 200)


    for counter in range(lens_end_city):
        name = list(modify_my_city_list.keys())[counter]
        count = list(modify_my_city_list.values())[counter]
        path = count / lens_my_city_list
        percent = '{percent:.1%}'.format(percent=path)
        total_city.append({'name': name, 'percent': percent, 'count': count})

    total_city = (sorted(total_city, key=itemgetter('count'), reverse=True))

    result_city = {
            'keywords': proff,
            'dispersion': total_city
            }

    result_city_json = json.dumps(result_city, ensure_ascii=False, indent=4)

    f = open('city_head_10.txt', 'a')
    # f.write('Профессия: ')
    # f.write(result_skill['keywords'])
    # f.write('\n')
    f.write('Всего городов: ')
    f.write(str(lens_end_city))
    f.write('\n')


    f = open('city_top_10.txt', 'a')
    for counter in total_city:
        f.write(counter['name'])
        f.write(' ')
        f.write(str(counter['percent']))
        f.write(' ')
        f.write(str(counter['count']))
        f.write('\n')
    f.close()


    f = open('top_10.txt', 'a')
    f.write('Профессия: ')
    f.write(result_skill['keywords'])
    f.write('\n')
    f.write('Всего навыков: ')
    f.write(result_skill['count'])
    f.write('\n')
    # # f.write(str(result_skill['requirements']))
    # f.write('Скиллы: ')
    # f.write('\n')
    # f.write(str(new_new))
        # f.write('\n')
    f = open('result_top_10.txt', 'a')
    for counter in total_skill:
        f.write(counter['name'])
        f.write(' ')
        f.write(str(counter['percent']))
        f.write(' ')
        f.write(str(counter['count']))
        f.write('\n')
    f.close()

    f = open('result_10.json', 'w')
    f.write(result_skill_json)
    f.close()

    f = open('result.txt', 'w')
    f.write(str(result_skill))
    f.close()
    print('Успешно создан файл result.txt со списком необходимых навыков')

    f = open('result.json', 'w')
    f.write(result_skill_json)
    f.close()
    print('Успешно создан файл result.fson со списком необходимых навыков')

    f = open('city.txt', 'w')
    f.write(str(result_city))
    f.close()

    print('Успешно создан файл city.txt со списком городов')
    f = open('city.json', 'w')
    f.write(result_city_json)
    f.close()
    print('Успешно создан файл city.fson со списком городов')

