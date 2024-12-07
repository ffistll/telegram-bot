# selective_repair.py

import math
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Константы
a = 1
b = 2
c = 3
c2 = 0.31
c5 = 0.9
c6 = 1.2
f = 4
pi = math.pi
h = 100

E = 206000  # МПа
v = 0.3

# Клавиатуры
defect_character_keyboard = ReplyKeyboardMarkup(row_width=1,
                                                resize_keyboard=True)
defect_character_keyboard.add(
    KeyboardButton('Поверхностные дефекты(в/р)'), KeyboardButton('Гофры(в/р)'),
    KeyboardButton('Дефекты сварных соединений(в/р)'),
    KeyboardButton('Вмятины(в/р)'),
    KeyboardButton('Дефекты овализации поперечного сечения(в/р)'))

defect_answer_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
defect_answer_keyboard.add(KeyboardButton('Да'), KeyboardButton('Нет'))

dent_type_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
dent_type_keyboard.add(KeyboardButton('Плавная локальная'),
                       KeyboardButton('С внутренним угловым углублением'))

k1_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
k1_keyboard.add(KeyboardButton('1) 1,34'), KeyboardButton('2) 1,40'),
                KeyboardButton('3) 1,47'), KeyboardButton('4) 1,55'))

category_keyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
category_keyboard.add(KeyboardButton('B'), KeyboardButton('1'),
                      KeyboardButton('2'), KeyboardButton('3'),
                      KeyboardButton('4'))

user_data_global = {}


def parse_float(value):
    try:
        return float(value.replace(',', '.'))
    except ValueError:
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


def start_selective_repair(bot, message, user_data):
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

    # Поверхностные дефекты (в/р)
    elif state == 'vr_surface_defect_tf':
        handle_vr_surface_defect_tf(bot, message, user_data)
    elif state == 'vr_surface_defect_dmax':
        handle_vr_surface_defect_dmax(bot, message, user_data)
    elif state == 'vr_surface_defect_p':
        handle_vr_surface_defect_p(bot, message, user_data)
    elif state == 'vr_surface_defect_Dn':
        handle_vr_surface_defect_Dn(bot, message, user_data)
    elif state == 'vr_surface_defect_sigma_v':
        handle_vr_surface_defect_sigma_v(bot, message, user_data)
    elif state == 'vr_surface_defect_k1_selection':
        handle_vr_surface_defect_k1_selection(bot, message, user_data)
    elif state == 'vr_surface_defect_kn':
        handle_vr_surface_defect_kn(bot, message, user_data)
    elif state == 'vr_surface_defect_n':
        handle_vr_surface_defect_n(bot, message, user_data)
    elif state == 'vr_surface_defect_area_check':
        handle_vr_surface_defect_area_check(bot, message, user_data)
    elif state == 'vr_surface_defect_kp':
        handle_vr_surface_defect_kp(bot, message, user_data)
    elif state == 'vr_surface_defect_L':
        handle_vr_surface_defect_L(bot, message, user_data)
    elif state == 'vr_surface_defect_Q':
        handle_vr_surface_defect_Q(bot, message, user_data)
    elif state == 'vr_surface_defect_complex_profile':
        handle_vr_surface_defect_complex_profile(bot, message, user_data)
    elif state == 'vr_complex_profile_N':
        handle_vr_complex_profile_N(bot, message, user_data)
    elif state == 'vr_complex_profile_z':
        handle_vr_complex_profile_z(bot, message, user_data)
    elif state == 'vr_complex_profile_d':
        handle_vr_complex_profile_d(bot, message, user_data)
    elif state == 'vr_simple_omega':
        handle_vr_simple_omega(bot, message, user_data)
    elif state == 'vr_pipe_replacement_check_simple':
        handle_vr_pipe_replacement_check_simple(bot, message, user_data)
    elif state == 'vr_pipe_replacement_check_complex':
        handle_vr_pipe_replacement_check_complex(bot, message, user_data)

    # Гофры(в/р)
    elif state == 'gofer_defect_height_check':
        handle_gofer_defect_height_check(bot, message, user_data)

    # Вмятины(в/р)
    elif state == 'dent_depth_check':
        handle_dent_depth_check(bot, message, user_data)
    elif state == 'dent_on_weld_check':
        handle_dent_on_weld_check(bot, message, user_data)
    elif state == 'dent_depth_percentage_check':
        handle_dent_depth_percentage_check(bot, message, user_data)
    elif state == 'dent_type_selection':
        handle_dent_type_selection(bot, message, user_data)
    elif state == 'dent_tf':
        handle_dent_tf(bot, message, user_data)
    elif state == 'dent_Dn':
        handle_dent_Dn(bot, message, user_data)
    elif state == 'dent_d':
        handle_dent_d(bot, message, user_data)
    elif state == 'dent_L1':
        handle_dent_L1(bot, message, user_data)
    elif state == 'dent_L2':
        handle_dent_L2(bot, message, user_data)

    # Дефекты овализации (в/р)
    elif state == 'oval_dmax':
        handle_oval_dmax(bot, message, user_data)
    elif state == 'oval_dmin':
        handle_oval_dmin(bot, message, user_data)
    elif state == 'oval_Dn':
        handle_oval_Dn(bot, message, user_data)
    elif state == 'oval_tf':
        handle_oval_tf(bot, message, user_data)
    elif state == 'oval_p':
        handle_oval_p(bot, message, user_data)
    elif state == 'oval_sigma_t':
        handle_oval_sigma_t(bot, message, user_data)

    elif state == 'select_m_category':
        handle_select_m_category(bot, message, user_data)
    else:
        bot.send_message(
            message.chat.id,
            'Пожалуйста, начните сначала, введя команду /start или напишите "Старт".'
        )


def user_data_from_message(message):
    chat_id = message.chat.id
    if chat_id not in user_data_global:
        user_data_global[chat_id] = {}
    return user_data_global[chat_id]


def handle_defect_character(bot, message, user_data):
    defect = message.text
    user_data['defect_character'] = defect
    user_data['previous_state'].append('defect_character_selection')

    if defect == 'Поверхностные дефекты(в/р)':
        bot.send_message(
            message.chat.id,
            'Введите значение tф (фактическая толщина стенки трубы, мм):',
            reply_markup=ReplyKeyboardRemove())
        user_data['state'] = 'vr_surface_defect_tf'
    elif defect == 'Гофры(в/р)':
        bot.send_message(
            message.chat.id,
            'Высота гофр более 3 мм или 0,3 толщины стенки трубы при толщине стенки < 10 мм?',
            reply_markup=defect_answer_keyboard)
        user_data['state'] = 'gofer_defect_height_check'
    elif defect == 'Дефекты сварных соединений(в/р)':
        bot.send_message(
            message.chat.id,
            'Оценку работоспособности кольцевых сварных соединений по результатам наружного обследования проводят по СТО Газпром 2-2.4-715-2013.',
            reply_markup=ReplyKeyboardRemove())
        bot.send_document(
            message.chat.id,
            open('documentation/СТО_Газпром_2-2.4-715-2013.pdf', 'rb'))
        return_to_start(bot, message)
    elif defect == 'Вмятины(в/р)':
        bot.send_message(
            message.chat.id,
            'Вмятина глубиной < 6,0 мм при любых значениях длины?',
            reply_markup=defect_answer_keyboard)
        user_data['state'] = 'dent_depth_check'
    elif defect == 'Дефекты овализации поперечного сечения(в/р)':
        bot.send_message(
            message.chat.id,
            'Введите значение Dmax (наибольшее значение диаметра сечения трубы, мм):',
            reply_markup=ReplyKeyboardRemove())
        user_data['state'] = 'oval_dmax'
    else:
        bot.send_message(
            message.chat.id,
            'Пожалуйста, выберите один из предложенных вариантов.',
            reply_markup=defect_character_keyboard)


################ Поверхностные дефекты(в/р) ###################
def handle_vr_surface_defect_tf(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    t_f = parse_float(message.text)
    if t_f is not None:
        user_data['tf'] = t_f
        bot.send_message(
            message.chat.id,
            'Введите значение dmax (максимальная глубина дефекта, мм):',
            reply_markup=ReplyKeyboardRemove())
        user_data['previous_state'].append('vr_surface_defect_tf')
        user_data['state'] = 'vr_surface_defect_dmax'
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для tф, мм.')


def handle_vr_surface_defect_dmax(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    dmax = parse_float(message.text)
    if dmax is not None:
        user_data['dmax'] = dmax
        tf = user_data['tf']
        tost = tf - dmax
        user_data['tost'] = tost
        bot.send_message(message.chat.id,
                         'Введите значение p (проектное давление, МПа):',
                         reply_markup=ReplyKeyboardRemove())
        user_data['previous_state'].append('vr_surface_defect_dmax')
        user_data['state'] = 'vr_surface_defect_p'
    else:
        bot.send_message(
            message.chat.id,
            'Пожалуйста, введите числовое значение для dmax, мм.')


def handle_vr_surface_defect_p(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    p = parse_float(message.text)
    if p is not None:
        user_data['p'] = p
        bot.send_message(message.chat.id,
                         'Введите значение Dн (диаметр трубы, мм):',
                         reply_markup=ReplyKeyboardRemove())
        user_data['previous_state'].append('vr_surface_defect_p')
        user_data['state'] = 'vr_surface_defect_Dn'
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для p, МПа.')


def handle_vr_surface_defect_Dn(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    Dn = parse_float(message.text)
    if Dn is not None:
        user_data['Dn'] = Dn
        bot.send_message(
            message.chat.id,
            'Введите значение σв (нормативный предел прочности материала), МПа (смотрите в сертификате на трубу):',
            reply_markup=ReplyKeyboardRemove())
        user_data['previous_state'].append('vr_surface_defect_Dn')
        user_data['state'] = 'vr_surface_defect_sigma_v'
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для Dн, мм.')


def handle_vr_surface_defect_sigma_v(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    sigma_v = parse_float(message.text)
    if sigma_v is not None:
        user_data['sigma_v'] = sigma_v
        # Перед выбором k1 убираем клавиатуру
        bot.send_message(message.chat.id,
                         'Выберите характеристику трубы для определения k1:',
                         reply_markup=ReplyKeyboardRemove())
        # Полное описание k1
        bot.send_message(
            message.chat.id,
            '1) k1 = 1,34: Сварные из стали контролируемой прокатки и термически упрочненные трубы, '
            'изготовленные двухсторонней электродуговой сваркой под флюсом по сплошному технологическому шву, '
            'с минусовым допуском по толщине стенки не более 5% и подвергнутые автоматическому контролю '
            'в объеме 100% на сплошность основного металла и сварных соединений.'
        )
        bot.send_message(
            message.chat.id,
            '2) k1 = 1,40: Сварные, изготовленные двухсторонней электродуговой сваркой под флюсом и '
            'подвергнутые автоматическому контролю в объеме 100% сварных соединений. '
            'Бесшовные трубы, подвергнутые автоматическому контролю в объеме 100% на сплошность металла.'
        )
        bot.send_message(
            message.chat.id,
            '3) k1 = 1,47: Сварные, изготовленные электроконтактной сваркой токами высокой частоты, '
            'сварные соединения которых термически обработаны и подвергнуты автоматическому контролю '
            'в объеме 100% неразрушающими методами.')
        bot.send_message(
            message.chat.id,
            '4) k1 = 1,55: Прочие бесшовные или электросварные трубы.')

        user_data['previous_state'].append('vr_surface_defect_sigma_v')
        user_data['state'] = 'vr_surface_defect_k1_selection'
        bot.send_message(message.chat.id,
                         'Пожалуйста, выберите соответствующий вариант:',
                         reply_markup=k1_keyboard)
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для σв, МПа.')


def handle_vr_surface_defect_k1_selection(bot, message, user_data):
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
    user_data['previous_state'].append('vr_surface_defect_k1_selection')

    bot.send_message(
        message.chat.id,
        'Введите значение kн (коэффициент надежности по назначению):',
        reply_markup=ReplyKeyboardRemove())
    bot.send_document(message.chat.id, open('documentation/kн.png', 'rb'))
    user_data['state'] = 'vr_surface_defect_kn'


def handle_vr_surface_defect_kn(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    kn = parse_float(message.text)
    if kn is not None:
        user_data['kn'] = kn

        bot.send_message(
            message.chat.id,
            'Введите значение n (коэффициент надежности по нагрузке):',
            reply_markup=ReplyKeyboardRemove())
        bot.send_document(message.chat.id, open('documentation/n.png', 'rb'))

        user_data['previous_state'].append('vr_surface_defect_kn')
        user_data['state'] = 'vr_surface_defect_n'
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для kн.')


def handle_vr_surface_defect_n(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    n = parse_float(message.text)
    if n is not None:
        user_data['n'] = n
        user_data['previous_state'].append('vr_surface_defect_n')

        # Выбор категории - показываем клавиатуру
        bot.send_message(message.chat.id,
                         'Выберите категорию трубопровода:',
                         reply_markup=category_keyboard)
        user_data['state'] = 'select_m_category'
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
    calculate_tp(bot, message.chat.id, user_data)


def calculate_tp(bot, chat_id, user_data):
    try:
        p = user_data['p']
        Dn = user_data['Dn']
        sigma_v = user_data['sigma_v']
        k1 = user_data['k1']
        kn = user_data['kn']
        n = user_data['n']
        m = user_data['m']

        R_t1 = (m * sigma_v) / (k1 * kn)
        denominator = 2 * (R_t1 + n * p)
        if denominator == 0:
            bot.send_message(
                chat_id, 'Ошибка: знаменатель при вычислении tр равен нулю.')
            return_to_start_by_chat_id(bot, chat_id)
            return
        tp = (n * p * Dn) / denominator
        user_data['tp'] = tp
        bot.send_message(
            chat_id,
            f'Значение расчетной толщины стенки трубы (tр): {tp:.7f} мм')

        tost = user_data['tost']
        if tost < 0.7 * tp:
            bot.send_message(
                chat_id,
                'Дефект соответствует п.6.3.1\nЗамена труб или ремонт врезкой катушки.',
                reply_markup=ReplyKeyboardRemove())
            return_to_start_by_chat_id(bot, chat_id)
        else:
            bot.send_message(chat_id, 'Дефект не соответствует п.6.3.1')
            bot.send_message(
                chat_id,
                'Оценка ремонтопригодности трубы с одиночным поверхностным дефектом или дефектной областью длиной L п.6.3.2'
            )
            bot.send_message(
                chat_id,
                'Суммарная площадь дефектов, подлежащих КШ > 0,3 м²?',
                reply_markup=defect_answer_keyboard)
            user_data['previous_state'].append('calculate_tp')
            user_data['state'] = 'vr_surface_defect_area_check'

    except Exception as e:
        bot.send_message(chat_id, f'Ошибка расчета tр: {str(e)}')
        return_to_start_by_chat_id(bot, chat_id)


def handle_vr_surface_defect_area_check(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if message.text == 'Да':
        bot.send_message(
            message.chat.id,
            'Допускается замена трубы без расчета по п.5.4 и п.6.3',
            reply_markup=ReplyKeyboardRemove())
        return_to_start(bot, message)
    elif message.text == 'Нет':
        bot.send_message(
            message.chat.id,
            'Введите значение kп (коэффициент пропорциональности):',
            reply_markup=ReplyKeyboardRemove())
        user_data['previous_state'].append('vr_surface_defect_area_check')
        user_data['state'] = 'vr_surface_defect_kp'
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, ответьте "Да" или "Нет".',
                         reply_markup=defect_answer_keyboard)


def handle_vr_surface_defect_kp(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    kp = parse_float(message.text)
    if kp is not None:
        user_data['kp'] = kp
        user_data['previous_state'].append('vr_surface_defect_kp')
        calculate_omega_vr(bot, message.chat.id, user_data)
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для kп.')


def calculate_omega_vr(bot, chat_id, user_data):
    try:
        kp = user_data['kp']
        k1 = user_data['k1']
        Kf = k1 + c6 * kp
        omega_vr = 1 - ((k1 * (1 + c6 * kp)) / (Kf * (k1 + c6)))
        if omega_vr < 0:
            omega_vr = 0
        user_data['omega_vr'] = omega_vr
        bot.send_message(chat_id, f'Значение [ω]^в вр: {omega_vr:.7f}')
        bot.send_message(chat_id,
                         'Введите значение длины дефекта L, мм:',
                         reply_markup=ReplyKeyboardRemove())
        user_data['state'] = 'vr_surface_defect_L'
    except Exception as e:
        bot.send_message(chat_id, f'Ошибка при расчете [ω]^в вр: {str(e)}')
        return_to_start_by_chat_id(bot, chat_id)


def handle_vr_surface_defect_L(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    L = parse_float(message.text)
    if L is not None:
        user_data['L'] = L
        bot.send_message(message.chat.id,
                         'Введите значение Q:',
                         reply_markup=ReplyKeyboardRemove())
        user_data['previous_state'].append('vr_surface_defect_L')
        user_data['state'] = 'vr_surface_defect_Q'
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для L, мм.')


def handle_vr_surface_defect_Q(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    Q = parse_float(message.text)
    if Q is not None:
        user_data['Q'] = Q
        user_data['previous_state'].append('vr_surface_defect_Q')
        calculate_tost_condition(bot, message.chat.id, user_data)
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для Q.')


def calculate_tost_condition(bot, chat_id, user_data):
    try:
        tost = user_data['tost']
        omega_vr = user_data['omega_vr']
        tp = user_data['tp']
        Q = user_data['Q']
        denominator = Q - (1 - omega_vr)
        if denominator == 0:
            bot.send_message(
                chat_id, 'Ошибка: знаменатель при расчёте условия равен нулю.')
            return_to_start_by_chat_id(bot, chat_id)
            return
        condition_value = (1 - omega_vr) * tp * ((Q - 1) / denominator)
        if tost >= condition_value:
            bot.send_message(chat_id,
                             'Труба ремонтопригодна.',
                             reply_markup=ReplyKeyboardRemove())
            return_to_start_by_chat_id(bot, chat_id)
        else:
            bot.send_message(chat_id,
                             'Требуется дополнительная оценка.',
                             reply_markup=ReplyKeyboardRemove())
            bot.send_message(chat_id,
                             'Дефект сложного профиля?',
                             reply_markup=defect_answer_keyboard)
            user_data['previous_state'].append('calculate_tost_condition')
            user_data['state'] = 'vr_surface_defect_complex_profile'
    except Exception as e:
        bot.send_message(chat_id,
                         f'Ошибка при проверке условия tост ≥ ...: {str(e)}')
        return_to_start_by_chat_id(bot, chat_id)


def handle_vr_surface_defect_complex_profile(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if message.text == 'Да':
        bot.send_message(
            message.chat.id,
            'Введите количество точек измерений глубины дефекта (N):',
            reply_markup=ReplyKeyboardRemove())
        user_data['previous_state'].append('vr_surface_defect_complex_profile')
        user_data['state'] = 'vr_complex_profile_N'
    elif message.text == 'Нет':
        bot.send_message(message.chat.id,
                         'Введите значение ω:',
                         reply_markup=ReplyKeyboardRemove())
        user_data['previous_state'].append('vr_surface_defect_complex_profile')
        user_data['state'] = 'vr_simple_omega'
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, ответьте "Да" или "Нет".',
                         reply_markup=defect_answer_keyboard)


def handle_vr_complex_profile_N(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    try:
        N = int(parse_float(message.text))
        if N < 2:
            bot.send_message(message.chat.id, 'N должно быть больше 1.')
            return
        user_data['N'] = N
        K = N - 1
        user_data['K'] = K
        bot.send_message(message.chat.id,
                         f'Количество расчетных частей K: {K}')
        user_data['current_k'] = 1
        user_data['Ak_list'] = []
        user_data['omega_k_list'] = []
        user_data['previous_state'].append('vr_complex_profile_N')
        request_z_and_d(bot, message.chat.id, user_data)
    except ValueError:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите целое число для N.')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при вычислении K: {str(e)}')
        return_to_start_by_chat_id(bot, message.chat.id)


def request_z_and_d(bot, chat_id, user_data):
    bot.send_message(
        chat_id,
        f'Начинаем ввод данных для расчетной части {user_data["current_k"]}.')
    user_data['zi_list'] = []
    user_data['di_list'] = []
    user_data['current_point'] = 1
    request_z(bot, chat_id, user_data)


def request_z(bot, chat_id, user_data):
    bot.send_message(chat_id, f'Введите z_{user_data["current_point"]} (мм):')
    user_data['state'] = 'vr_complex_profile_z'


def handle_vr_complex_profile_z(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['zi_list'].append(value)
        bot.send_message(message.chat.id,
                         f'Введите d_{user_data["current_point"]} (мм):')
        user_data['previous_state'].append('vr_complex_profile_z')
        user_data['state'] = 'vr_complex_profile_d'
    else:
        bot.send_message(
            message.chat.id,
            f'Пожалуйста, введите числовое значение для z_{user_data["current_point"]}.'
        )


def handle_vr_complex_profile_d(bot, message, user_data):
    if message.text == 'Назад':
        if user_data['zi_list']:
            user_data['zi_list'].pop()
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['di_list'].append(value)
        if user_data['current_point'] < user_data['N']:
            user_data['current_point'] += 1
            request_z(bot, message.chat.id, user_data)
        else:
            user_data['previous_state'].append('vr_complex_profile_d')
            calculate_Ak(bot, message.chat.id, user_data)
    else:
        bot.send_message(
            message.chat.id,
            f'Пожалуйста, введите числовое значение для d_{user_data["current_point"]}.'
        )


def calculate_Ak(bot, chat_id, user_data):
    try:
        zi_list = user_data['zi_list']
        di_list = user_data['di_list']
        N = user_data['N']
        Ak = 0
        Lj_list = []
        dj_list = []
        for i in range(N - 1):
            Lj = abs(zi_list[i + 1] - zi_list[i])
            Lj_list.append(Lj)
            dj = (di_list[i + 1] + di_list[i]) / 2
            dj_list.append(dj)
            Ak += dj * Lj
        user_data['Ak_list'].append(Ak)
        tf = user_data['tost']
        Dn = user_data['Dn']
        tp = user_data['tp']
        Lk = sum(Lj_list)
        A0k = tf * Lk
        Qk = math.sqrt(1 + (c2 * Lk**2) / (Dn * tp))
        Ak_over_A0k = Ak / A0k
        denominator = Qk - Ak_over_A0k
        if denominator == 0:
            bot.send_message(chat_id,
                             'Ошибка: знаменатель при расчёте ωk равен нулю.')
            return_to_start_by_chat_id(bot, chat_id)
            return
        omega_k = Ak_over_A0k * ((Qk - 1) / denominator)
        user_data['omega_k_list'].append(omega_k)
        if user_data['current_k'] < user_data['K']:
            user_data['current_k'] += 1
            request_z_and_d(bot, chat_id, user_data)
        else:
            omega = max(user_data['omega_k_list'])
            user_data['omega'] = omega
            bot.send_message(chat_id, f'Значение ω = {omega:.7f}')
            compare_omega_omega_vr_complex(bot, chat_id, user_data)
    except Exception as e:
        bot.send_message(chat_id, f'Ошибка при расчёте Ak и ωk: {str(e)}')
        return_to_start_by_chat_id(bot, chat_id)


def compare_omega_omega_vr_complex(bot, chat_id, user_data):
    try:
        omega = user_data['omega']
        omega_vr = user_data['omega_vr']
        if omega <= omega_vr:
            bot.send_message(chat_id,
                             'Труба ремонтопригодна согласно п.6.3.13.',
                             reply_markup=ReplyKeyboardRemove())
            return_to_start_by_chat_id(bot, chat_id)
        else:
            bot.send_message(chat_id, 'Замена или ремонт врезкой катушки.')
            bot.send_message(
                chat_id,
                '7.16 при ВР вместо замены трубы или врезки катушки допускается устанавливать муфту на поврежденную часть при выполнении условий по 7.16.1 - 7.16.2.\n'
                '7.16.1 При проведении ремонта дефектов труб с параметром снижения несущей способности, '
                'рассчитанным по фактическим размерам вышлифованной области по 6.3, '
                'значение контактного давления между трубой и устанавливаемой муфтой должно быть меньше значения w * p.\n'
                '7.16.2 Муфты (устанавливающие конструкции), применяемые для ремонта труб и технологии ремонта '
                'методом установки муфт (усиливающих конструкций), должны пройти оценку соответствия и быть допущены '
                'к применению в установленном ПАО "Газпром" порядке.',
                reply_markup=ReplyKeyboardRemove())
            bot.send_message(chat_id,
                             'Катушка ≥ 3 м или Количество катушек >1?',
                             reply_markup=defect_answer_keyboard)
            user_data['state'] = 'vr_pipe_replacement_check_complex'
    except Exception as e:
        bot.send_message(chat_id,
                         f'Ошибка при сравнении ω и [ω]^в вр: {str(e)}')
        return_to_start_by_chat_id(bot, chat_id)


def handle_vr_pipe_replacement_check_complex(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if message.text == 'Нет':
        bot.send_message(message.chat.id,
                         'Врезка катушки.',
                         reply_markup=ReplyKeyboardRemove())
        return_to_start(bot, message)
    elif message.text == 'Да':
        bot.send_message(message.chat.id,
                         'Полная замена трубы.',
                         reply_markup=ReplyKeyboardRemove())
        return_to_start(bot, message)
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, ответьте "Да" или "Нет".',
                         reply_markup=defect_answer_keyboard)


def handle_vr_simple_omega(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    omega = parse_float(message.text)
    if omega is not None:
        user_data['omega'] = omega
        compare_omega_omega_vr_simple(bot, message.chat.id, user_data)
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для ω.')


def compare_omega_omega_vr_simple(bot, chat_id, user_data):
    try:
        omega = user_data['omega']
        omega_vr = user_data['omega_vr']
        if omega <= omega_vr:
            bot.send_message(chat_id,
                             'Труба ремонтопригодна.',
                             reply_markup=ReplyKeyboardRemove())
            return_to_start_by_chat_id(bot, chat_id)
        else:
            bot.send_message(chat_id, 'Замена или ремонт врезкой катушки.')
            bot.send_message(
                chat_id,
                '7.16 при ВР вместо замены трубы или врезки катушки допускается устанавливать муфту на поврежденную часть при выполнении условий по 7.16.1 - 7.16.2.\n'
                '7.16.1 При проведении ремонта дефектов труб ... значение контактного давления < w * p.\n'
                '7.16.2 Муфты должны пройти оценку соответствия и быть допущены к применению в порядке ПАО "Газпром".',
                reply_markup=ReplyKeyboardRemove())
            bot.send_message(chat_id,
                             'Катушка ≥ 3 м или Количество катушек >1?',
                             reply_markup=defect_answer_keyboard)
            user_data['state'] = 'vr_pipe_replacement_check_simple'
    except Exception as e:
        bot.send_message(chat_id,
                         f'Ошибка при сравнении ω и [ω]^в вр: {str(e)}')
        return_to_start_by_chat_id(bot, chat_id)


def handle_vr_pipe_replacement_check_simple(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if message.text == 'Нет':
        bot.send_message(message.chat.id,
                         'Врезка катушки.',
                         reply_markup=ReplyKeyboardRemove())
        return_to_start(bot, message)
    elif message.text == 'Да':
        bot.send_message(message.chat.id,
                         'Полная замена трубы.',
                         reply_markup=ReplyKeyboardRemove())
        return_to_start(bot, message)
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, ответьте "Да" или "Нет".',
                         reply_markup=defect_answer_keyboard)


# Гофры(в/р)
def handle_gofer_defect_height_check(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if message.text == 'Да':
        bot.send_message(message.chat.id,
                         'Замена или ремонт врезкой катушки.',
                         reply_markup=ReplyKeyboardRemove())
        return_to_start(bot, message)
    elif message.text == 'Нет':
        bot.send_message(message.chat.id,
                         'Допустимый дефект.',
                         reply_markup=ReplyKeyboardRemove())
        return_to_start(bot, message)
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, ответьте "Да" или "Нет".',
                         reply_markup=defect_answer_keyboard)


# Вмятины(в/р)
def handle_dent_depth_check(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if message.text == 'Да':
        bot.send_message(message.chat.id,
                         'Относится к допустимым.',
                         reply_markup=ReplyKeyboardRemove())
        return_to_start(bot, message)
    elif message.text == 'Нет':
        bot.send_message(message.chat.id,
                         'Вмятина на сварном соединении?',
                         reply_markup=defect_answer_keyboard)
        user_data['previous_state'].append('dent_depth_check')
        user_data['state'] = 'dent_on_weld_check'
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, ответьте "Да" или "Нет".',
                         reply_markup=defect_answer_keyboard)


def handle_dent_on_weld_check(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    user_data['dent_on_weld'] = (message.text == 'Да')
    user_data['previous_state'].append('dent_on_weld_check')
    if user_data['dent_on_weld']:
        bot.send_message(message.chat.id,
                         'Глубина < 2% от Dн?',
                         reply_markup=defect_answer_keyboard)
    else:
        bot.send_message(message.chat.id,
                         'Глубина < 5% от Dн?',
                         reply_markup=defect_answer_keyboard)
    user_data['state'] = 'dent_depth_percentage_check'


def handle_dent_depth_percentage_check(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if message.text == 'Да':
        bot.send_message(message.chat.id,
                         'Тип вмятины?',
                         reply_markup=dent_type_keyboard)
        user_data['previous_state'].append('dent_depth_percentage_check')
        user_data['state'] = 'dent_type_selection'
    elif message.text == 'Нет':
        bot.send_message(message.chat.id,
                         'Замена или ремонт врезкой катушки.',
                         reply_markup=ReplyKeyboardRemove())
        return_to_start(bot, message)
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, ответьте "Да" или "Нет".',
                         reply_markup=defect_answer_keyboard)


def handle_dent_type_selection(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if message.text in [
            'Плавная локальная', 'С внутренним угловым углублением'
    ]:
        user_data['dent_type'] = message.text
        user_data['previous_state'].append('dent_type_selection')
        bot.send_message(message.chat.id,
                         'Введите tф (фактическая толщина стенки трубы, мм):',
                         reply_markup=ReplyKeyboardRemove())
        user_data['state'] = 'dent_tf'
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, выберите тип вмятины.',
                         reply_markup=dent_type_keyboard)


def handle_dent_tf(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    t_f = parse_float(message.text)
    if t_f is not None:
        user_data['t_f'] = t_f
        bot.send_message(message.chat.id,
                         'Введите Dн (диаметр трубы, мм):',
                         reply_markup=ReplyKeyboardRemove())
        user_data['previous_state'].append('dent_tf')
        user_data['state'] = 'dent_Dn'
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для tф, мм.')


def handle_dent_Dn(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    Dn = parse_float(message.text)
    if Dn is not None:
        user_data['Dn'] = Dn
        user_data['R0'] = Dn / 2
        bot.send_message(message.chat.id,
                         'Введите d (глубина вмятины, мм):',
                         reply_markup=ReplyKeyboardRemove())
        user_data['previous_state'].append('dent_Dn')
        user_data['state'] = 'dent_d'
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для Dн, мм.')


def handle_dent_d(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    d = parse_float(message.text)
    if d is not None:
        user_data['d'] = d
        bot.send_message(message.chat.id,
                         'Введите L1 (окружная длина вмятины, мм):',
                         reply_markup=ReplyKeyboardRemove())
        user_data['previous_state'].append('dent_d')
        user_data['state'] = 'dent_L1'
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для d.')


def handle_dent_L1(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    L1 = parse_float(message.text)
    if L1 is not None:
        user_data['L1'] = L1
        bot.send_message(message.chat.id,
                         'Введите L2 (продольная длина вмятины, мм):',
                         reply_markup=ReplyKeyboardRemove())
        user_data['previous_state'].append('dent_L1')
        user_data['state'] = 'dent_L2'
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для L1.')


def handle_dent_L2(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    L2 = parse_float(message.text)
    if L2 is not None:
        user_data['L2'] = L2
        user_data['previous_state'].append('dent_L2')
        calculate_dent_deformations(bot, message.chat.id, user_data)
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для L2.')


# calculate_dent_deformations и ниже уже описаны


# Дефекты овализации (в/р)
def handle_oval_dmax(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    Dmax = parse_float(message.text)
    if Dmax is not None:
        user_data['Dmax'] = Dmax
        bot.send_message(
            message.chat.id,
            'Введите значение Dmin (наименьшее значение диаметра сечения трубы, мм):',
            reply_markup=ReplyKeyboardRemove())
        user_data['previous_state'].append('oval_dmax')
        user_data['state'] = 'oval_dmin'
    else:
        bot.send_message(
            message.chat.id,
            'Пожалуйста, введите числовое значение для Dmax, мм.')


def handle_oval_dmin(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    Dmin = parse_float(message.text)
    if Dmin is not None:
        user_data['Dmin'] = Dmin
        bot.send_message(message.chat.id,
                         'Введите значение Dн (диаметр трубы, мм):',
                         reply_markup=ReplyKeyboardRemove())
        user_data['previous_state'].append('oval_dmin')
        user_data['state'] = 'oval_Dn'
    else:
        bot.send_message(
            message.chat.id,
            'Пожалуйста, введите числовое значение для Dmin, мм.')


def handle_oval_Dn(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    Dn = parse_float(message.text)
    if Dn is not None:
        user_data['Dn'] = Dn
        theta = ((user_data['Dmax'] - user_data['Dmin']) / Dn) * h
        user_data['theta'] = theta
        bot.send_message(message.chat.id, f'Значение θ: {theta:.3f}%')

        bot.send_message(
            message.chat.id,
            'Введите значение tф (фактическая толщина стенки трубы, мм):',
            reply_markup=ReplyKeyboardRemove())
        user_data['previous_state'].append('oval_Dn')
        user_data['state'] = 'oval_tf'
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для Dн, мм.')


def handle_oval_tf(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    tf = parse_float(message.text)
    if tf is not None:
        user_data['tf'] = tf
        bot.send_message(message.chat.id,
                         'Введите значение p (рабочее давление), МПа:',
                         reply_markup=ReplyKeyboardRemove())
        user_data['previous_state'].append('oval_tf')
        user_data['state'] = 'oval_p'
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для tф, мм.')


def handle_oval_p(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    p = parse_float(message.text)
    if p is not None:
        user_data['p'] = p
        bot.send_message(
            message.chat.id,
            'Введите значение σт (предел текучести материала), МПа (смотрите в сертификате на трубу):',
            reply_markup=ReplyKeyboardRemove())
        user_data['previous_state'].append('oval_p')
        user_data['state'] = 'oval_sigma_t'
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для p, МПа.')


def handle_oval_sigma_t(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    sigma_t = parse_float(message.text)
    if sigma_t is not None:
        user_data['sigma_t'] = sigma_t
        # Расчет [θ]вр сразу
        calculate_theta_vr_oval(bot, message.chat.id, user_data)
    else:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите числовое значение для σт, МПа.')


def calculate_theta_vr_oval(bot, chat_id, user_data):
    try:
        Dn = user_data['Dn']
        p = user_data['p']
        sigma_t = user_data['sigma_t']
        theta = user_data['theta']
        tf = user_data['tf']

        sigma_n = p * ((Dn - 2 * tf) / (2 * tf))
        omega_o_vr = a - (sigma_n / sigma_t)
        beta = (a / (a - v**2)) * ((tf / Dn)**2) * (E / sigma_t)
        denominator = (a - omega_o_vr)
        if denominator == 0:
            bot.send_message(chat_id,
                             'Ошибка: деление на ноль при вычислении [θ]вр.')
            return_to_start_by_chat_id(bot, chat_id)
            return
        theta_vr = (
            (b * tf) /
            (c * Dn)) * (omega_o_vr / beta) * (a + (beta / denominator)) * h

        bot.send_message(chat_id, f'Значение [θ]вр: {theta_vr:.3f}%')

        if theta <= theta_vr:
            bot.send_message(
                chat_id,
                'Условие θ ≤ [θ]вр соблюдается.\nПодлежит ремонту по п. 7.12.',
                reply_markup=ReplyKeyboardRemove())
            bot.send_document(chat_id, open('documentation/7.12.PNG', 'rb'))
        else:
            bot.send_message(
                chat_id,
                'Условие θ ≤ [θ]вр не соблюдается.\nЗамена или ремонт врезкой катушки.',
                reply_markup=ReplyKeyboardRemove())

        return_to_start_by_chat_id(bot, chat_id)
    except Exception as e:
        bot.send_message(chat_id,
                         f'Ошибка при вычислении [θ]вр: {str(e)}',
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
