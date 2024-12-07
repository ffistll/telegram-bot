# reinsulation_replacement.py

import math
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Константные переменные
a = 1
b = 2
c = 3
h = 100
c1 = 0.2
c2 = 0.31
c5 = 0.9

# Константы модуля упругости и коэффициента Пуассона
E = 206000  # МПа
v = 0.3

# Создание клавиатур
defect_character_keyboard = ReplyKeyboardMarkup(row_width=1,
                                                resize_keyboard=True)
defect_character_keyboard.add(
    KeyboardButton('Поверхностные дефекты'), KeyboardButton('Гофры'),
    KeyboardButton('Дефекты сварных соединений'), KeyboardButton('Вмятины'),
    KeyboardButton('Дефекты овализации поперечного сечения'))

defect_reason_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
defect_reason_keyboard.add(
    KeyboardButton('Коррозионные дефекты, единичные трещины и дефекты КРН'),
    KeyboardButton(
        'Механические повреждения (риска, царапина, продир, плена закат)'))

defect_answer_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
defect_answer_keyboard.add(KeyboardButton('Да'), KeyboardButton('Нет'))

# Клавиатура для выбора категории трубопровода
category_keyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
category_keyboard.add(KeyboardButton('B'), KeyboardButton('1'),
                      KeyboardButton('2'), KeyboardButton('3'),
                      KeyboardButton('4'))

# Клавиатура для выбора k1
k1_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
k1_keyboard.add(KeyboardButton('1) 1,34'), KeyboardButton('2) 1,40'),
                KeyboardButton('3) 1,47'), KeyboardButton('4) 1,55'))

# Глобальный словарь для хранения данных пользователей
user_data_global = {}


def parse_float(value):
    try:
        value = value.replace(',', '.')
        return float(value)
    except (ValueError, AttributeError):
        return None


def handle_back_command(bot, message, user_data):
    if 'previous_state' in user_data and user_data['previous_state']:
        user_data['state'] = user_data['previous_state'].pop()
        bot.send_message(message.chat.id, 'Хорошо, давайте вернёмся назад.')
        message.text = ''
        handle_state(bot, message, user_data)
    else:
        bot.send_message(message.chat.id,
                         'Невозможно вернуться назад.',
                         reply_markup=ReplyKeyboardRemove())


def start_reinsulation_replacement(bot, message, user_data):
    user_data['state'] = 'defect_character_selection'
    user_data['previous_state'] = []
    bot.send_message(message.chat.id,
                     'Выберите характер дефекта:',
                     reply_markup=defect_character_keyboard)


def handle_state(bot, message, user_data):
    state = user_data.get('state')
    if state is None:
        bot.send_message(
            message.chat.id,
            'Пожалуйста, начните сначала, введя команду /start или напишите "Старт".'
        )
        return

    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return

    if state == 'defect_character_selection':
        handle_defect_character(bot, message, user_data)
    elif state == 'defect_reason_selection':
        handle_defect_reason(bot, message, user_data)
    elif state == 'defect_length_300mm':
        handle_defect_length_300mm(bot, message, user_data)
    elif state == 'defect_length':
        handle_defect_length(bot, message, user_data)
    elif state == 'defect_width':
        handle_defect_width(bot, message, user_data)
    elif state == 'dmax':
        handle_dmax(bot, message, user_data)
    elif state == 'p':
        handle_p(bot, message, user_data)
    elif state == 'Dn':
        handle_Dn(bot, message, user_data)
    elif state == 'tf':
        handle_tf(bot, message, user_data)
    elif state == 'k1_selection':
        handle_k1_selection(bot, message, user_data)
    elif state == 'kn':
        handle_kn(bot, message, user_data)
    elif state == 'sigma_v':
        handle_sigma_v(bot, message, user_data)
    elif state == 'n':
        handle_n(bot, message, user_data)
    elif state == 'select_m_category':
        handle_select_m_category(bot, message, user_data)
    elif state == 'corrugation_check':
        handle_corrugation_check(bot, message, user_data)
    elif state == 'dent_check':
        handle_dent_check(bot, message, user_data)
    elif state == 'oval_dmax':
        handle_oval_dmax(bot, message, user_data)
    elif state == 'oval_dmin':
        handle_oval_dmin(bot, message, user_data)
    elif state == 'oval_dn':
        handle_oval_dn(bot, message, user_data)
    elif state == 'oval_tf':
        handle_oval_tf(bot, message, user_data)
    elif state == 'oval_tn':
        handle_oval_tn(bot, message, user_data)
    elif state == 'oval_kn':
        handle_oval_kn(bot, message, user_data)
    elif state == 'oval_p':
        handle_oval_p(bot, message, user_data)
    elif state == 'oval_sigma_t':
        handle_oval_sigma_t(bot, message, user_data)
    elif state == 'select_m_category_theta_kr':
        handle_select_m_category_theta_kr(bot, message, user_data)
    else:
        bot.send_message(
            message.chat.id,
            'Пожалуйста, начните сначала, введя команду /start или напишите "Старт".'
        )


def handle_defect_character(bot, message, user_data):
    defect = message.text
    user_data['defect_character'] = defect
    user_data['previous_state'].append('defect_character_selection')
    if defect == 'Поверхностные дефекты':
        user_data['state'] = 'defect_reason_selection'
        bot.send_message(message.chat.id,
                         'Выберите причину дефекта:',
                         reply_markup=defect_reason_keyboard)
    elif defect == 'Гофры':
        user_data['state'] = 'corrugation_check'
        bot.send_message(
            message.chat.id,
            'Высота гофр более 3 мм или 0,3 от толщины стенки трубы при толщине стенки < 10 мм?',
            reply_markup=defect_answer_keyboard)
    elif defect == 'Дефекты сварных соединений':
        bot.send_message(
            message.chat.id,
            'Оценку работоспособности кольцевых сварных соединений по результатам наружного обследования проводят в соответствии с СТО Газпром 15-1.3-004-2023',
            reply_markup=ReplyKeyboardRemove())
        bot.send_document(
            message.chat.id,
            open('documentation/СТО Газпром 15-1.3-004-2023.pdf', 'rb'))
        return_to_start(bot, message)
    elif defect == 'Вмятины':
        user_data['state'] = 'dent_check'
        bot.send_message(
            message.chat.id,
            'Вмятина глубиной менее 6,0 мм при любых значениях длины в окружном и продольных направлениях?',
            reply_markup=defect_answer_keyboard)
    elif defect == 'Дефекты овализации поперечного сечения':
        user_data['state'] = 'oval_dmax'
        bot.send_message(
            message.chat.id,
            'Введите значение Dmax (максимальная глубина дефекта, мм):',
            reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(
            message.chat.id,
            'Пожалуйста, выберите один из предложенных вариантов.',
            reply_markup=defect_character_keyboard)


def handle_defect_reason(bot, message, user_data):
    defect_reason = message.text
    if defect_reason == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    user_data['defect_reason'] = defect_reason
    user_data['previous_state'].append('defect_reason_selection')
    if defect_reason == 'Коррозионные дефекты, единичные трещины и дефекты КРН':
        user_data['state'] = 'defect_length_300mm'
        bot.send_message(message.chat.id,
                         'Дефект до 300 мм п.6.3.1',
                         reply_markup=defect_answer_keyboard)
        bot.send_document(message.chat.id, open('documentation/6.3.1.PNG',
                                                'rb'))
    elif defect_reason == 'Механические повреждения (риска, царапина, продир, плена закат)':
        user_data['state'] = 'defect_length'
        bot.send_message(
            message.chat.id,
            'Введите значение длины дефекта L (длина поверхностного дефекта, мм):',
            reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(
            message.chat.id,
            'Пожалуйста, выберите корректную причину дефекта из предложенных вариантов.',
            reply_markup=defect_reason_keyboard)


def handle_defect_length_300mm(bot, message, user_data):
    answer = message.text
    if answer == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if answer == 'Да':
        user_data['previous_state'].append('defect_length_300mm')
        user_data['state'] = 'defect_length'
        bot.send_message(
            message.chat.id,
            'Введите значение длины дефекта L (длина поверхностного дефекта, мм):',
            reply_markup=ReplyKeyboardRemove())
    elif answer == 'Нет':
        bot.send_message(
            message.chat.id,
            'Замена труб или ремонт врезкой катушки вне зависимости от глубины и ширины дефекта',
            reply_markup=ReplyKeyboardRemove())
        return_to_start(bot, message)
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, ответьте "Да" или "Нет".',
                         reply_markup=defect_answer_keyboard)


def handle_defect_length(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['L'] = value
        user_data['previous_state'].append('defect_length')
        user_data['state'] = 'defect_width'
        bot.send_message(
            message.chat.id,
            'Введите значение ширины дефекта B (ширина поверхностного дефекта, мм):',
            reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(
            message.chat.id,
            'Пожалуйста, введите числовое значение для длины L, мм.')


def handle_defect_width(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['width'] = value
        calculate_defect_area(bot, message.chat.id, user_data)
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для B, мм.')


def calculate_defect_area(bot, chat_id, user_data):
    L = user_data.get('L')
    width = user_data.get('width')
    defect_area = L * width / 1e6  # м²
    if defect_area > 0.3:
        bot.send_message(
            chat_id,
            'Допускается замена трубы без расчета по п. 5.4 и п. 6.3',
            reply_markup=ReplyKeyboardRemove())
        bot.send_document(
            chat_id,
            open(
                'documentation/СТО Газпром 27.3-2.2-006-2023 Инструкция по оценке дефектов труб и СДТ.pdf',
                'rb'))
        return_to_start_by_chat_id(bot, chat_id)
    else:
        bot.send_message(
            chat_id,
            'Площадь дефекта меньше 0.3 м². Переходим к дальнейшим расчетам.')
        user_data['previous_state'].append('defect_width')
        user_data['state'] = 'dmax'
        bot.send_message(
            chat_id,
            'Введите значение максимальной глубины дефекта dmax (максимальная глубина дефекта, мм):',
            reply_markup=ReplyKeyboardRemove())


def handle_dmax(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        adjusted_dmax = value + 0.2
        user_data['dmax'] = adjusted_dmax
        bot.send_message(message.chat.id,
                         f'Расчетное значение dmax: {adjusted_dmax:.2f} мм')
        user_data['previous_state'].append('dmax')
        user_data['state'] = 'p'
        bot.send_message(message.chat.id,
                         'Введите значение p (проектное давление), МПа:',
                         reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(
            message.chat.id,
            'Пожалуйста, введите числовое значение для dmax, мм.')


def handle_p(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['p'] = value
        user_data['previous_state'].append('p')
        user_data['state'] = 'Dn'
        bot.send_message(message.chat.id,
                         'Введите значение Dн (диаметр трубы, мм):',
                         reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для p, МПа.')


def handle_Dn(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['Dn'] = value
        user_data['previous_state'].append('Dn')
        user_data['state'] = 'tf'
        bot.send_message(
            message.chat.id,
            'Введите значение tф (фактическая толщина стенки трубы, мм):',
            reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для Dн, мм.')


def handle_tf(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['tf'] = value
        # Перед выбором k1 убираем клавиатуру
        bot.send_message(
            message.chat.id,
            'Выберите характеристику трубы для определения коэффициента надежности по материалу (k1):',
            reply_markup=ReplyKeyboardRemove())
        # Полное описание k1 (полностью прописываем)
        bot.send_message(
            message.chat.id,
            '1) 1,34: Сварные из стали контролируемой прокатки и термически упрочненные трубы, '
            'изготовленные двухсторонней электродуговой сваркой под флюсом по сплошному технологическому шву, '
            'с минусовым допуском по толщине стенки не более 5% и подвергнутые автоматическому контролю '
            'в объеме 100% на сплошность основного металла и сварных соединений неразрушающими методами.'
        )
        bot.send_message(
            message.chat.id,
            '2) 1,40: Сварные, изготовленные двухсторонней электродуговой сваркой под флюсом и подвергнутые '
            'автоматическому контролю в объеме 100% сварных соединений неразрушающими методами. '
            'Бесшовные, подвергнутые автоматическому контролю в объеме 100% на сплошность металла '
            'неразрушающими методами.')
        bot.send_message(
            message.chat.id,
            '3) 1,47: Сварные, изготовленные электроконтактной сваркой токами высокой частоты, '
            'сварные соединения которых термически обработаны и подвергнуты автоматическому контролю '
            'в объеме 100% неразрушающими методами.')
        bot.send_message(
            message.chat.id,
            '4) 1,55: Прочие бесшовные или электросварные трубы.')
        user_data['previous_state'].append('tf')
        user_data['state'] = 'k1_selection'
        bot.send_message(message.chat.id,
                         'Пожалуйста, выберите соответствующий вариант:',
                         reply_markup=k1_keyboard)
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для tф, мм.')


def handle_k1_selection(bot, message, user_data):
    selection = message.text.strip()
    if selection == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if selection == '1) 1,34':
        k1 = 1.34
    elif selection == '2) 1,40':
        k1 = 1.40
    elif selection == '3) 1,47':
        k1 = 1.47
    elif selection == '4) 1,55':
        k1 = 1.55
    else:
        bot.send_message(
            message.chat.id,
            'Пожалуйста, выберите один из предложенных вариантов.',
            reply_markup=k1_keyboard)
        return
    user_data['k1'] = k1
    user_data['previous_state'].append('k1_selection')
    user_data['state'] = 'kn'
    bot.send_message(
        message.chat.id,
        'Введите значение kн (коэффициент надежности по назначению):',
        reply_markup=ReplyKeyboardRemove())
    bot.send_document(message.chat.id, open('documentation/kн.png', 'rb'))


def handle_kn(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['kn'] = value
        user_data['previous_state'].append('kn')
        user_data['state'] = 'sigma_v'
        bot.send_message(
            message.chat.id,
            'Введите значение нормативного предела прочности материала σв, МПа (смотрите в сертификате на трубу):',
            reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для kн.')


def handle_sigma_v(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['sigma_v'] = value
        user_data['previous_state'].append('sigma_v')
        user_data['state'] = 'n'
        bot.send_message(
            message.chat.id,
            'Введите значение n (коэффициент надежности по нагрузке):',
            reply_markup=ReplyKeyboardRemove())
        bot.send_document(message.chat.id, open('documentation/n.png', 'rb'))
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для σв, МПа.')


def handle_n(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['n'] = value
        user_data['previous_state'].append('n')
        user_data['state'] = 'select_m_category'
        bot.send_message(message.chat.id,
                         'Выберите категорию трубопровода и его участка:',
                         reply_markup=category_keyboard)
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для n.')


def handle_select_m_category(bot, message, user_data):
    category = message.text
    if category == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if category == 'B':
        m = 0.660
    elif category == '1':
        m = 0.825
    elif category == '2':
        m = 0.825
    elif category == '3':
        m = 0.990
    elif category == '4':
        m = 0.990
    else:
        bot.send_message(
            message.chat.id,
            'Пожалуйста, выберите одну из категорий: B, 1, 2, 3, 4.',
            reply_markup=category_keyboard)
        return
    user_data['m'] = m
    user_data['previous_state'].append('select_m_category')
    calculate_result_surface_defect(bot, message.chat.id, user_data)


def calculate_result_surface_defect(bot, chat_id, user_data):
    try:
        dmax = user_data['dmax']
        p = user_data['p']
        Dn = user_data['Dn']
        tf = user_data['tf']
        k1 = user_data['k1']
        kn = user_data['kn']
        sigma_v = user_data['sigma_v']
        n = user_data['n']
        L = user_data['L']
        m = user_data['m']

        tost = tf - dmax
        R1 = (m * sigma_v) / (k1 * kn)
        tp = (n * p * Dn) / (2 * (R1 + (n * p)))
        Q = math.sqrt(a + ((c2 * L * L) / (Dn * tp)))
        numerator = c5 * tp * (Q - a)
        denominator = Q - c5

        if denominator == 0:
            bot.send_message(
                chat_id,
                'Ошибка: знаменатель при расчёте результата равен нулю.')
            return_to_start_by_chat_id(bot, chat_id)
            return

        result_value = numerator / denominator

        if tost >= result_value:
            result_phrase = 'Труба ремонтопригодна. Ремонт КШ на приобъектовых площадках.'
        else:
            result_phrase = 'Труба бракуется и вырезается.'

        bot.send_message(
            chat_id,
            f'Результат расчета:\n tост {"≥" if tost >= result_value else "<"} {result_value:.2f} мм\n{result_phrase}',
            reply_markup=ReplyKeyboardRemove())
        return_to_start_by_chat_id(bot, chat_id)
    except Exception as e:
        bot.send_message(chat_id,
                         f'Ошибка расчета: {str(e)}',
                         reply_markup=ReplyKeyboardRemove())
        return_to_start_by_chat_id(bot, chat_id)


def handle_corrugation_check(bot, message, user_data):
    answer = message.text
    if answer == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if answer == 'Да':
        bot.send_message(message.chat.id,
                         'Замена или ремонт врезкой катушки.',
                         reply_markup=ReplyKeyboardRemove())
    elif answer == 'Нет':
        bot.send_message(message.chat.id,
                         'Допустимый дефект.',
                         reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, ответьте "Да" или "Нет".',
                         reply_markup=defect_answer_keyboard)
        return
    return_to_start(bot, message)


def handle_dent_check(bot, message, user_data):
    answer = message.text
    if answer == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if answer == 'Да':
        bot.send_message(message.chat.id,
                         'Допустимый дефект.',
                         reply_markup=ReplyKeyboardRemove())
    elif answer == 'Нет':
        bot.send_message(message.chat.id,
                         'Труба бракуется и вырезается.',
                         reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, ответьте "Да" или "Нет".',
                         reply_markup=defect_answer_keyboard)
        return
    return_to_start(bot, message)


def handle_oval_dmax(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['Dmax'] = value
        user_data['previous_state'].append('oval_dmax')
        user_data['state'] = 'oval_dmin'
        bot.send_message(message.chat.id,
                         'Введите значение Dmin (мм):',
                         reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(
            message.chat.id,
            'Пожалуйста, введите числовое значение для Dmax, мм.')


def handle_oval_dmin(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['Dmin'] = value
        user_data['previous_state'].append('oval_dmin')
        user_data['state'] = 'oval_dn'
        bot.send_message(message.chat.id,
                         'Введите значение Dн (диаметр трубы, мм):',
                         reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(
            message.chat.id,
            'Пожалуйста, введите числовое значение для Dmin, мм.')


def handle_oval_dn(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['Dn'] = value
        user_data['h'] = h
        try:
            Dmax = user_data['Dmax']
            Dmin = user_data['Dmin']
            theta = ((Dmax - Dmin) / user_data['Dn']) * user_data['h']
            user_data['theta'] = theta
            bot.send_message(message.chat.id,
                             f'Значение овальности θ: {theta:.3f}%')
            user_data['previous_state'].append('oval_dn')
            user_data['state'] = 'oval_tf'
            bot.send_message(
                message.chat.id,
                'Введите значение tф (фактическая толщина стенки трубы, мм):',
                reply_markup=ReplyKeyboardRemove())
        except Exception as e:
            bot.send_message(message.chat.id, f'Ошибка расчета θ: {str(e)}')
            return_to_start(bot, message)
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для Dн, мм.')


def handle_oval_tf(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['tf'] = value
        theta = user_data['theta']
        tf = user_data['tf']
        if tf <= 20:
            theta_limit = 1.0
        else:
            theta_limit = 0.8
        if theta <= theta_limit:
            bot.send_message(message.chat.id,
                             'Допустимый дефект.',
                             reply_markup=ReplyKeyboardRemove())
            return_to_start(bot, message)
        else:
            bot.send_message(
                message.chat.id,
                f'Овальность θ = {theta:.3f}% превышает допустимое значение {theta_limit}%. Переходим к расчету [θ]кр.'
            )
            user_data['previous_state'].append('oval_tf')
            user_data['state'] = 'oval_tn'
            bot.send_message(
                message.chat.id,
                'Введите значение tн (номинальная толщина стенки трубы, мм):',
                reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для tф, мм.')


def handle_oval_tn(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['tn'] = value
        user_data['previous_state'].append('oval_tn')
        user_data['state'] = 'oval_kn'
        bot.send_message(
            message.chat.id,
            'Введите значение kн (коэффициент надежности по назначению):',
            reply_markup=ReplyKeyboardRemove())
        bot.send_document(message.chat.id, open('documentation/kн.png', 'rb'))
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для tн, мм.')


def handle_oval_kn(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['kn'] = value
        user_data['previous_state'].append('oval_kn')
        user_data['state'] = 'oval_p'
        bot.send_message(message.chat.id,
                         'Введите значение p (проектное давление), МПа:',
                         reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для kн.')


def handle_oval_p(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['p'] = value
        user_data['previous_state'].append('oval_p')
        user_data['state'] = 'oval_sigma_t'
        bot.send_message(
            message.chat.id,
            'Введите значение σт (предел текучести материала), МПа (смотрите в сертификате на трубу):',
            reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для p, МПа.')


def handle_oval_sigma_t(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['sigma_t'] = value
        user_data['previous_state'].append('oval_sigma_t')
        user_data['state'] = 'select_m_category_theta_kr'
        bot.send_message(message.chat.id,
                         'Выберите категорию трубопровода и его участка:',
                         reply_markup=category_keyboard)
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для σт, МПа.')


def handle_select_m_category_theta_kr(bot, message, user_data):
    category = message.text
    if category == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if category == 'B':
        m = 0.660
    elif category == '1':
        m = 0.825
    elif category == '2':
        m = 0.825
    elif category == '3':
        m = 0.990
    elif category == '4':
        m = 0.990
    else:
        bot.send_message(
            message.chat.id,
            'Пожалуйста, выберите одну из категорий: B, 1, 2, 3, 4.',
            reply_markup=category_keyboard)
        return
    user_data['m'] = m
    user_data['previous_state'].append('select_m_category_theta_kr')
    calculate_theta_kr(bot, message.chat.id, user_data)


def calculate_theta_kr(bot, chat_id, user_data):
    try:
        Dn = user_data['Dn']
        tf = user_data['tf']
        tn = user_data['tn']
        kn = user_data['kn']
        p = user_data['p']
        sigma_t = user_data['sigma_t']
        theta = user_data['theta']
        m = user_data['m']

        sigma_kc = (p * (Dn - b * tf)) / (b * tf)
        omega_okr = a - (c5 * kn * sigma_kc) / (m * sigma_t)
        beta = (a / (a - v**2)) * ((tf / Dn)**2) * (E / sigma_t)
        denominator = a - omega_okr

        if denominator == 0:
            bot.send_message(
                chat_id,
                'Ошибка: знаменатель равен нулю при вычислении [θ]кр.')
            return_to_start_by_chat_id(bot, chat_id)
            return

        theta_kr = ((b * tn) /
                    (c * Dn)) * (omega_okr / beta) * (a +
                                                      (beta / denominator)) * h
        bot.send_message(
            chat_id, f'Значение допустимой овальности [θ]кр: {theta_kr:.3f}%')

        if theta <= theta_kr:
            bot.send_message(chat_id, 'Условие θ ≤ [θ]кр соблюдается.')
            bot.send_message(chat_id,
                             'Подлежит ремонту по п. 7.12.',
                             reply_markup=ReplyKeyboardRemove())
            bot.send_document(chat_id, open('documentation/7.12.PNG', 'rb'))
        else:
            bot.send_message(chat_id, 'Условие θ ≤ [θ]кр не соблюдается.')
            bot.send_message(chat_id,
                             'Замена или ремонт обрезкой катушки.',
                             reply_markup=ReplyKeyboardRemove())
        return_to_start_by_chat_id(bot, chat_id)
    except Exception as e:
        bot.send_message(chat_id,
                         f'Ошибка расчета: {str(e)}',
                         reply_markup=ReplyKeyboardRemove())
        return_to_start_by_chat_id(bot, chat_id)


def return_to_start(bot, message):
    user_data = user_data_from_message(message)
    user_data['state'] = None
    user_data['previous_state'] = []
    bot.send_message(
        message.chat.id,
        'Вы можете начать новый расчет, введя команду /start или написав "Старт".',
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
            KeyboardButton('/start')))


def return_to_start_by_chat_id(bot, chat_id):
    user_data = user_data_global.get(chat_id, {})
    user_data['state'] = None
    user_data['previous_state'] = []
    bot.send_message(
        chat_id,
        'Вы можете начать новый расчет, введя команду /start или написав "Старт".',
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
            KeyboardButton('/start')))


def user_data_from_message(message):
    chat_id = message.chat.id
    if chat_id not in user_data_global:
        user_data_global[chat_id] = {}
    return user_data_global[chat_id]
