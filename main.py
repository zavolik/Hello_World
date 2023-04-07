import re
import pandas as pd

# 1. Загрузите файл Russian_ds.tsv.
# Оба формата читаются с помощью команды .read_csv(), символ табуляции передается параметром sep (разделитель):

df = pd.read_csv('Russian_ds.tsv', sep='\t')
df.tail(40)


# 2. Создайте столбец с типом населенных пунктов.
def get_settlement_type(name):
    all_types = ['поселок городского типа', 'рабочий поселок', 'хутор', 'железнодорожная площадка',
                 'поселок железнодорожного разъезда',
                 'населенный пункт', 'слобода', 'железнодорожная будка', 'выселок', 'местечко', 'селище', 'заимка',
                 'блок-пост', 'участок', 'кордон', 'территория', 'аул', 'улус', 'кутан', 'станица', 'починок',
                 'остановочная платформа', 'обгонный пункт', 'железнодорожная платформа', 'обгонная платформа',
                 'железнодорожная казарма', 'остановочный пункт', 'аал', 'железнодорожный остановочный пункт',
                 'железнодорожный путевой пост', 'поселок при станции', 'арбан', 'высел', 'казарма', 'полустанок',
                 'экопоселение', 'поселение', 'остров', 'погост', 'слободка', 'железнодорожный блокпост',
                 'молочнотоварная ферма', 'місто', 'седо', 'переезд', 'мыс', 'отделение',
                 'станция', 'деревня', 'город', 'поселок', 'село', 'разъезд', 'проселок', 'городок', 'выселки']

    for key in all_types:
        if string_search(key, name.lower().replace('ё', 'е')):
            return key
    return 'отсутствует тип населенного пункта'  # высматриваем оставшиеся значения, для которых тип еще не определен


def string_search(string1, string2):  # до этого использовали in, работало через раз (поСЕЛОк)
    if re.search(r'\b' + re.escape(string1) + r'\b', string2):
        return True
    return False


df.insert(1, 'type', df['name'].apply(get_settlement_type))

print(df['type'].value_counts().tail(40))
df = df.drop(columns=['other_name'])  # удалили этот непонятный столбец, который не несет в себе смысла
df.tail(40)


# 3. Создайте столбец с названиями населенных пунктов, очищенный от типов. Созданные столбцы не должны содержать пропущенных значения, если невозможно установить тип населенного пункта, заполните пропуски. Допустимо заменить буквы ё на е для некоторых типов населенных пунктов.
def get_only_name(row):
    # проверка наличия типа населенного пункта
    if row['type'] == 'Отсутствует тип населенного пункта':
        return row['name']
    else:
        # вычитание типа населенного пункта из названия
        return row['name'].replace('ё', 'е').replace(row['type'], '')


df.insert(2, 'only_name', df.apply(get_only_name, 1))
print(df)

# 4. Получите список уникальных типов населенных пунктов, определите число уникальных типов населенных пунктов. Определите долю каждого типа населенного пункта. Для трех любых неизвестных для вас ранее типов населенных пунктов определите региональную принадлежность.

# Получение уникальных типов населенных пунктов
unique_types = df['type'].unique()

# Вывод списка уникальных типов населенных пунктов и их количество
print('Уникальные типы населенных пунктов: ', unique_types)
print('Количество уникальных типов населенных пунктов: ', len(unique_types))

# Определение доли каждого типа населенного пункта
for t in unique_types:
    count = df[df['type'] == t]['name'].count()
    fraction = count / len(df) * 100
    print('Доля типа "', t, '" :', round(fraction, 3), '%')

# Определение региональной принадлежности для трех неизвестных типов населенных пунктов
unknown_types = ['арбан', 'аал', 'кутан']
for t in unknown_types:
    regions = df[df['type'] == t]['region_name'].unique()
    print('Тип', t, 'входит в состав регионов: ', regions)

# 5. Посчитайте сумму населения по типам населенных пунктов в абсолютных и относительных значениях.
# Сгруппировать данные по типу населенного пункта и вычислить сумму населения
grouped = df.groupby('type')['population'].sum()

# Сгруппировать данные по типу населенного пункта и вычислить сумму населения
grouped_approx = df.groupby('type')['approx'].sum()

print("Абсолютные значения:")
print(grouped)
print("\nОтносительные значения:")
print(grouped_approx)

# 6. Определите топ-10 самых популярных названий населенных пунктов. Определите число уникальных названий населенных пунктов.
# Подсчет топ-10 самых популярных названий населенных пунктов
top_10 = df['only_name'].value_counts().nlargest(10)
print("Топ-10 самых популярных названий населенных пунктов:", top_10)

# Подсчет числа уникальных названий населенных пунктов
unique_names_count = df['only_name'].nunique()
print("Число уникальных названий населенных пунктов:", unique_names_count)

# 7. Определите населенные пункты с самыми короткими названиями. Получите список населенных пунктов с длиной в два символа, найдите наиболее популярные названия из найденного списка. Определите региональную принадлежность. Повторите исследование для населенных пунктов с тремя символами.
short_names_2 = df[df['only_name'].str.len() == 2]['only_name']
print(df[df['only_name'].isin(short_names_2)][['only_name', 'region_name']].head(20))

short_names_3 = df[df['only_name'].str.len() == 3]['only_name']
print(df[df['only_name'].isin(short_names_3)][['only_name', 'region_name']].head(20))


# 8. Найдите населенный пункт с самым длинным названием из одного слова без пробелов и дефисов.
def find_starting_letter(df, column_name):
    maxLength = 0
    maxName = ""
    for index, row in df.iterrows():
        name_words = row[column_name].lower().replace('-', '').split()

        for word in name_words:
            if (len(word) > 0):
                nameCount = len(word)
                if nameCount > maxLength:
                    maxLength = nameCount
                    maxName = word

    print(maxName)


find_starting_letter(df, "only_name")

# 9. Определите число населенных пунктов на букву "Ы". На какую букву чаще всего начинаются названия населенных пунктов?
df['first_letter'] = df['only_name'].str[0]
count = (df['first_letter'] == 'Ы').sum()
print(count)


# 9. Определите число населенных пунктов на букву "Ы". На какую букву чаще всего начинаются названия населенных пунктов?
def find_starting_letter(df, column_name):
    counter = {}
    for index, row in df.iterrows():
        name = row[column_name].lower()

        if (len(name) > 0):
            first_letter = name[0].lower()
            if first_letter not in counter:
                counter[first_letter] = 1
            else:
                counter[first_letter] += 1

            # Ищем букву, с которой начинается название населенного пункта чаще всего.
    max_count = 0
    max_letter = ''
    for letter, count in counter.items():
        if count > max_count:
            max_count = count
            max_letter = letter
    print(max_letter)


find_starting_letter(df, 'only_name')

# 10. Определите сколько раз встречаются в названиях населенных пунктов прилагательные: большой, малый, красный, новый. #они могут встречаться и внутри названий (Прекрасный)
counts = {'большой': 0, 'малый': 0, 'красный': 0,
          'новый': 0}  # как делали в первом уроке, ключи словаря - 4 наших прилагательных
for adj in counts:
    counts[adj] = df['only_name'].str.contains(adj, case=False).sum()
# параметр case=False указывает методу str.contains() не учитывать регистр при поиске совпадений в строках
print(
    counts)  # считает только прилагательные в конкретной записи(муж. род), если слово записано с большой буквы то его принимает тоже


# 11. Найдите несколько примеров необычных названий населенных пунктов, связанных с одной из тематик (одной или нескольких, можно в разных). Допустимо предложить свою тематику.
def find_animals(df):
    # список с животными
    animals = ["волк", "кото", "котё", "тигр", "лиси"]
    # итерируемся по строкам DataFrame
    for index, row in df.iterrows():
        # берем только столбец "name" и разбиваем его на отдельные слова
        name_words = row["name"].split()
        # проверяем каждое слово из столбца "name"
        for word in name_words:
            # если первые 4 символа слова совпадают с элементом списка animals,
            # то выводим название пункта и переходим к следующей строке
            if word[:4].lower() in animals:
                print(row["name"])


find_animals(df)