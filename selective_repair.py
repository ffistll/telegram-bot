# selective_repair.py

import math
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Константы
m_default = 0.99
a = 1
b = 2
c = 3
c2 = 0.31
c5 = 0.9
c6 = 1.2
f = 4
pi = math.pi
h = 100

# Клавиатуры
defect_character_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
defect_character_keyboard.add(
    KeyboardButton('Поверхностные дефекты(в/р)'),
    KeyboardButton('Гофры(в/р)'),
    KeyboardButton('Дефекты сварных соединений(в/р)'),
    KeyboardButton('Вмятины(в/р)'),
    KeyboardButton('Дефекты овализации поперечного сечения(в/р)')
)

defect_answer_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
defect_answer_keyboard.add(KeyboardButton('Да'), KeyboardButton('Нет'))

dent_type_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
dent_type_keyboard.add(KeyboardButton('Плавная локальная'), KeyboardButton('С внутренним угловым углублением'))

# Клавиатура для выбора k1
k1_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
k1_keyboard.add(
    KeyboardButton('1) 1,34'),
    KeyboardButton('2) 1,40'),
    KeyboardButton('3) 1,47'),
    KeyboardButton('4) 1,55')
)

# Клавиатура для выбора категории трубопровода
category_keyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
category_keyboard.add(
    KeyboardButton('B'),
    KeyboardButton('1'),
    KeyboardButton('2'),
    KeyboardButton('3'),
    KeyboardButton('4')
)

# Глобальный словарь для хранения данных пользователей
user_data_global = {}

# Вспомогательная функция для обработки числовых значений с запятой
def parse_float(value):
    try:
        return float(value.replace(',', '.'))
    except ValueError:
        return None

# Функция для обработки команды "Назад"
def handle_back_command(bot, message, user_data):
    if 'previous_state' in user_data and user_data['previous_state']:
        user_data['state'] = user_data['previous_state'].pop()
        bot.send_message(message.chat.id, 'Хорошо, давайте вернёмся назад.')
        # Изменяем текст сообщения, чтобы избежать повторной обработки "Назад"
        message.text = ''
        handle_state(bot, message, user_data)
    else:
        bot.send_message(message.chat.id, 'Невозможно вернуться назад.', reply_markup=ReplyKeyboardRemove())

# Функция для начала метода выборочного ремонта
def start_selective_repair(bot, message, user_data):
    user_data['state'] = 'defect_character_selection'
    user_data['previous_state'] = []
    bot.send_message(
        message.chat.id,
        'Выберите характер дефекта:',
        reply_markup=defect_character_keyboard
    )

# Обработчик состояния
def handle_state(bot, message, user_data):
    state = user_data.get('state')
    if state is None:
        bot.send_message(message.chat.id, 'Пожалуйста, начните сначала, введя команду /start.')
        return

    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return

    if state == 'defect_character_selection':
        handle_defect_character(bot, message, user_data)
    elif state == 'vr_surface_defect_tost':
        handle_vr_surface_defect_tost(bot, message, user_data)
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
    elif state == 'gofer_defect_height_check':
        handle_gofer_defect_height_check(bot, message, user_data)
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
    elif state == 'oval_dmax':
        handle_oval_dmax(bot, message, user_data)
    elif state == 'oval_dmin':
        handle_oval_dmin(bot, message, user_data)
    elif state == 'oval_Dn':
        handle_oval_Dn(bot, message, user_data)
    elif state == 'oval_tf':
        handle_oval_tf(bot, message, user_data)
    elif state == 'oval_theta_check':
        handle_oval_theta_check(bot, message, user_data)
    elif state == 'oval_tn':
        handle_oval_tn(bot, message, user_data)
    elif state == 'oval_kn':
        handle_oval_kn(bot, message, user_data)
    elif state == 'oval_p':
        handle_oval_p(bot, message, user_data)
    elif state == 'oval_E':
        handle_oval_E(bot, message, user_data)
    elif state == 'oval_v':
        handle_oval_v(bot, message, user_data)
    elif state == 'oval_sigma_t':
        handle_oval_sigma_t(bot, message, user_data)
    elif state == 'select_m_category_theta_kr':
        handle_select_m_category_theta_kr(bot, message, user_data)
    elif state == 'select_m_category':
        handle_select_m_category(bot, message, user_data)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, начните сначала, введя команду /start.')

# Вспомогательная функция для получения user_data по сообщению
def user_data_from_message(message):
    chat_id = message.chat.id
    if chat_id not in user_data_global:
        user_data_global[chat_id] = {}
    return user_data_global[chat_id]

# Обработчик для выбора характера дефекта
def handle_defect_character(bot, message, user_data):
    defect = message.text
    user_data['defect_character'] = defect
    user_data['previous_state'].append('defect_character_selection')
    if defect == 'Поверхностные дефекты(в/р)':
        handle_surface_defect(bot, message, user_data)
    elif defect == 'Гофры(в/р)':
        handle_gofer_defect(bot, message, user_data)
    elif defect == 'Дефекты сварных соединений(в/р)':
        handle_weld_defect(bot, message, user_data)
    elif defect == 'Вмятины(в/р)':
        handle_dent_defect(bot, message, user_data)
    elif defect == 'Дефекты овализации поперечного сечения(в/р)':
        handle_oval_defect(bot, message, user_data)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, выберите один из предложенных вариантов.', reply_markup=defect_character_keyboard)

# =================== Поверхностные дефекты(в/р) ===================
def handle_surface_defect(bot, message, user_data):
    bot.send_message(
        message.chat.id,
        'Введите значение tост (фактическая остаточная толщина стенки), мм:',
        reply_markup=ReplyKeyboardRemove()
    )
    user_data['state'] = 'vr_surface_defect_tost'

def handle_vr_surface_defect_tost(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['tost'] = value
        bot.send_message(message.chat.id, 'Введите значение p (давление), МПа:')
        user_data['previous_state'].append('vr_surface_defect_tost')
        user_data['state'] = 'vr_surface_defect_p'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для tост.')

def handle_vr_surface_defect_p(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['p'] = value
        bot.send_message(message.chat.id, 'Введите значение Dн (наружный диаметр трубы), мм:')
        user_data['previous_state'].append('vr_surface_defect_p')
        user_data['state'] = 'vr_surface_defect_Dn'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для p.')

def handle_vr_surface_defect_Dn(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['Dn'] = value
        bot.send_message(message.chat.id, 'Введите значение σв (нормативный предел прочности материала), МПа:')
        user_data['previous_state'].append('vr_surface_defect_Dn')
        user_data['state'] = 'vr_surface_defect_sigma_v'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для Dн.')

def handle_vr_surface_defect_sigma_v(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['sigma_v'] = value
        # Предлагаем выбрать k1 с пояснениями
        bot.send_message(
            message.chat.id,
            'Выберите характеристику трубы для определения коэффициента надежности по материалу (k1):',
            reply_markup=ReplyKeyboardRemove()
        )
        bot.send_message(
            message.chat.id,
            '1) Сварные из стали контролируемой прокатки и термически упрочненные трубы, изготовленные двухсторонней электродуговой сваркой под флюсом по сплошному технологическому шву, с минусовым допуском по толщине стенки не более 5% и подвергнутые автоматическому контролю в объеме 100% на сплошность основного металла и сварных соединений неразрушающими методами.'
        )
        bot.send_message(
            message.chat.id,
            '2) Сварные, изготовленные двухсторонней электродуговой сваркой под флюсом и подвергнутые автоматическому контролю в объеме 100% сварных соединений неразрушающими методами. Бесшовные, подвергнутые автоматическому контролю в объеме 100% на сплошность металла неразрушающими методами.'
        )
        bot.send_message(
            message.chat.id,
            '3) Сварные, изготовленные электроконтактной сваркой токами высокой частоты, сварные соединения которых термически обработаны и подвергнуты автоматическому контролю в объеме 100% неразрушающими методами.'
        )
        bot.send_message(
            message.chat.id,
            '4) Прочие бесшовные или электросварные.'
        )
        user_data['previous_state'].append('vr_surface_defect_sigma_v')
        user_data['state'] = 'vr_surface_defect_k1_selection'
        bot.send_message(
            message.chat.id,
            'Пожалуйста, выберите соответствующий вариант:',
            reply_markup=k1_keyboard
        )
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для σв.')

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
        bot.send_message(message.chat.id, 'Пожалуйста, выберите один из предложенных вариантов.', reply_markup=k1_keyboard)
        return

    user_data['k1'] = k1
    user_data['previous_state'].append('vr_surface_defect_k1_selection')
    user_data['state'] = 'vr_surface_defect_kn'
    bot.send_message(
        message.chat.id,
        'Введите значение коэффициента надежности по назначению kн согласно таблице 12 СП 36.13330.2012:',
        reply_markup=ReplyKeyboardRemove()
    )

def handle_vr_surface_defect_kn(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['kn'] = value
        bot.send_message(message.chat.id, 'Введите значение n (коэффициент надежности по нагрузке):')
        user_data['previous_state'].append('vr_surface_defect_kn')
        user_data['state'] = 'vr_surface_defect_n'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для kн.')

def handle_vr_surface_defect_n(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['n'] = value
        user_data['previous_state'].append('vr_surface_defect_n')
        # Запрашиваем категорию трубопровода для определения m
        user_data['state'] = 'select_m_category'
        bot.send_message(
            message.chat.id,
            'Выберите категорию трубопровода и его участка:',
            reply_markup=category_keyboard
        )
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для n.')

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
        bot.send_message(message.chat.id, 'Пожалуйста, выберите одну из категорий: B, 1, 2, 3, 4.', reply_markup=category_keyboard)
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
            bot.send_message(chat_id, 'Ошибка: знаменатель при вычислении tp равен нулю.')
            return_to_start_by_chat_id(bot, chat_id)
            return
        tp = (n * p * Dn) / denominator
        user_data['tp'] = tp
        bot.send_message(chat_id, f'Значение tp: {tp:.7f} мм')
        compare_tost_tp(bot, chat_id, user_data)
    except Exception as e:
        bot.send_message(chat_id, f'Ошибка расчета tp: {str(e)}')
        return_to_start_by_chat_id(bot, chat_id)

def compare_tost_tp(bot, chat_id, user_data):
    try:
        tost = user_data['tost']
        tp = user_data['tp']
        if tost < 0.7 * tp:
            bot.send_message(chat_id, 'Дефект соответствует п.6.3.1')
            bot.send_message(chat_id, 'Замена труб или ремонт врезкой катушки вне зависимости от длины и ширины дефекта.', reply_markup=ReplyKeyboardRemove())
            return_to_start_by_chat_id(bot, chat_id)
        else:
            bot.send_message(chat_id, 'Дефект не соответствует п.6.3.1')
            bot.send_message(chat_id, 'Оценка ремонтопригодности трубы с одиночным поверхностным дефектом или дефектной областью п.6.3.2')
            bot.send_message(chat_id, 'Суммарная площадь дефектов, подлежащих КШ > 0,3 м²?', reply_markup=defect_answer_keyboard)
            user_data['previous_state'].append('compare_tost_tp')
            user_data['state'] = 'vr_surface_defect_area_check'
    except Exception as e:
        bot.send_message(chat_id, f'Ошибка при сравнении tост и tp: {str(e)}')
        return_to_start_by_chat_id(bot, chat_id)

def handle_vr_surface_defect_area_check(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if message.text == 'Да':
        bot.send_message(message.chat.id, 'Допускается замена трубы без расчета по п. 5.4 и п. 6.3', reply_markup=ReplyKeyboardRemove())
        return_to_start(bot, message)
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, 'Введите значение kп (коэффициент пропорциональности):', reply_markup=ReplyKeyboardRemove())
        user_data['previous_state'].append('vr_surface_defect_area_check')
        user_data['state'] = 'vr_surface_defect_kp'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, ответьте "Да" или "Нет".', reply_markup=defect_answer_keyboard)

def handle_vr_surface_defect_kp(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['kp'] = value
        user_data['previous_state'].append('vr_surface_defect_kp')
        calculate_omega_vr(bot, chat_id=message.chat.id, user_data=user_data)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для kп.')

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
        bot.send_message(chat_id, 'Введите значение длины дефекта L, мм:')
        user_data['state'] = 'vr_surface_defect_L'
    except Exception as e:
        bot.send_message(chat_id, f'Ошибка при расчете [ω]^в вр: {str(e)}')
        return_to_start_by_chat_id(bot, chat_id)

def handle_vr_surface_defect_L(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['L'] = value
        bot.send_message(message.chat.id, 'Введите значение Q:')
        user_data['previous_state'].append('vr_surface_defect_L')
        user_data['state'] = 'vr_surface_defect_Q'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для L, мм.')

def handle_vr_surface_defect_Q(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['Q'] = value
        user_data['previous_state'].append('vr_surface_defect_Q')
        calculate_tost_condition(bot, chat_id=message.chat.id, user_data=user_data)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для Q.')

def calculate_tost_condition(bot, chat_id, user_data):
    try:
        tost = user_data['tost']
        omega_vr = user_data['omega_vr']
        tp = user_data['tp']
        Q = user_data['Q']
        denominator = Q - (1 - omega_vr)
        if denominator == 0:
            bot.send_message(chat_id, 'Ошибка: знаменатель при расчёте условия равен нулю.')
            return_to_start_by_chat_id(bot, chat_id)
            return
        condition_value = (1 - omega_vr) * tp * ((Q - 1) / denominator)
        if tost >= condition_value:
            bot.send_message(chat_id, 'Труба ремонтопригодна.', reply_markup=ReplyKeyboardRemove())
            return_to_start_by_chat_id(bot, chat_id)
        else:
            bot.send_message(chat_id, 'Требуется дополнительная оценка.', reply_markup=ReplyKeyboardRemove())
            bot.send_message(chat_id, 'Дефект сложного профиля?', reply_markup=defect_answer_keyboard)
            user_data['previous_state'].append('calculate_tost_condition')
            user_data['state'] = 'vr_surface_defect_complex_profile'
    except Exception as e:
        bot.send_message(chat_id, f'Ошибка при проверке условия tост ≥ ...: {str(e)}')
        return_to_start_by_chat_id(bot, chat_id)

def handle_vr_surface_defect_complex_profile(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if message.text == 'Да':
        bot.send_message(message.chat.id, 'Введите количество точек измерений глубины дефекта (N):', reply_markup=ReplyKeyboardRemove())
        user_data['previous_state'].append('vr_surface_defect_complex_profile')
        user_data['state'] = 'vr_complex_profile_N'
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, 'Введите значение ω:', reply_markup=ReplyKeyboardRemove())
        user_data['previous_state'].append('vr_surface_defect_complex_profile')
        user_data['state'] = 'vr_simple_omega'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, ответьте "Да" или "Нет".', reply_markup=defect_answer_keyboard)

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
        bot.send_message(message.chat.id, f'Количество расчетных частей K: {K}')
        user_data['current_k'] = 1
        user_data['Ak_list'] = []
        user_data['omega_k_list'] = []
        user_data['previous_state'].append('vr_complex_profile_N')
        request_z_and_d(bot, message.chat.id, user_data)
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите целое число для N.')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при вычислении K: {str(e)}')
        return_to_start_by_chat_id(bot, message.chat.id)

def request_z_and_d(bot, chat_id, user_data):
    bot.send_message(chat_id, f'Начинаем ввод данных для расчетной части {user_data["current_k"]}.')
    user_data['zi_list'] = []
    user_data['di_list'] = []
    user_data['current_point'] = 1
    request_z(bot, chat_id, user_data)

def request_z(bot, chat_id, user_data):
    bot.send_message(chat_id, f'Введите z_{user_data["current_point"]}:')
    user_data['state'] = 'vr_complex_profile_z'

def handle_vr_complex_profile_z(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['zi_list'].append(value)
        bot.send_message(message.chat.id, f'Введите d_{user_data["current_point"]}:')
        user_data['previous_state'].append('vr_complex_profile_z')
        user_data['state'] = 'vr_complex_profile_d'
    else:
        bot.send_message(message.chat.id, f'Пожалуйста, введите числовое значение для z_{user_data["current_point"]}.')

def handle_vr_complex_profile_d(bot, message, user_data):
    if message.text == 'Назад':
        # Удаляем последний z, так как мы вернулись назад
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
        bot.send_message(message.chat.id, f'Пожалуйста, введите числовое значение для d_{user_data["current_point"]}.')

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
        c2_value = c2
        Lk = sum(Lj_list)
        A0k = tf * Lk
        Qk = math.sqrt(1 + (c2_value * Lk ** 2) / (Dn * tp))
        Ak_over_A0k = Ak / A0k
        denominator = Qk - Ak_over_A0k
        if denominator == 0:
            bot.send_message(chat_id, 'Ошибка: знаменатель при расчёте ωk равен нулю.')
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
            bot.send_message(chat_id, 'Труба ремонтопригодна согласно п.6.3.13.', reply_markup=ReplyKeyboardRemove())
            return_to_start_by_chat_id(bot, chat_id)
        else:
            bot.send_message(chat_id, 'Труба или ее часть (катушку) необходимо вырезать согласно п.6.3.13.', reply_markup=ReplyKeyboardRemove())
            bot.send_message(chat_id, 'Замена или ремонт врезкой катушки.')
            bot.send_message(chat_id, '7.16 При ВР вместо замены трубы или врезки катушки допускается устанавливать муфту на поврежденную часть при выполнении условий по 7.16.1-7.16.2...')
            bot.send_message(chat_id, 'Катушка ≥ 3 м или Количество катушек >1?', reply_markup=defect_answer_keyboard)
            user_data['state'] = 'vr_pipe_replacement_check_complex'
    except Exception as e:
        bot.send_message(chat_id, f'Ошибка при сравнении ω и [ω]^в вр: {str(e)}')
        return_to_start_by_chat_id(bot, chat_id)

def handle_vr_pipe_replacement_check_complex(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if message.text == 'Нет':
        bot.send_message(message.chat.id, 'Врезка катушки.', reply_markup=ReplyKeyboardRemove())
        return_to_start(bot, message)
    elif message.text == 'Да':
        bot.send_message(message.chat.id, 'Полная замена трубы.', reply_markup=ReplyKeyboardRemove())
        return_to_start(bot, message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, ответьте "Да" или "Нет".', reply_markup=defect_answer_keyboard)

def handle_vr_simple_omega(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['omega'] = value
        compare_omega_omega_vr_simple(bot, message.chat.id, user_data)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для ω.')

def compare_omega_omega_vr_simple(bot, chat_id, user_data):
    try:
        omega = user_data['omega']
        omega_vr = user_data['omega_vr']
        if omega <= omega_vr:
            bot.send_message(chat_id, 'Труба ремонтопригодна.', reply_markup=ReplyKeyboardRemove())
            return_to_start_by_chat_id(bot, chat_id)
        else:
            bot.send_message(chat_id, 'Труба или ее часть (катушку) необходимо вырезать.', reply_markup=ReplyKeyboardRemove())
            bot.send_message(chat_id, 'Замена или ремонт врезкой катушки.')
            bot.send_message(chat_id, '7.16 При ВР вместо замены трубы или врезки катушки допускается устанавливать муфту...')
            bot.send_message(chat_id, 'Катушка ≥ 3 м или Количество катушек >1?', reply_markup=defect_answer_keyboard)
            user_data['state'] = 'vr_pipe_replacement_check_simple'
    except Exception as e:
        bot.send_message(chat_id, f'Ошибка при сравнении ω и [ω]^в вр: {str(e)}')
        return_to_start_by_chat_id(bot, chat_id)

def handle_vr_pipe_replacement_check_simple(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if message.text == 'Нет':
        bot.send_message(message.chat.id, 'Врезка катушки.', reply_markup=ReplyKeyboardRemove())
        return_to_start(bot, message)
    elif message.text == 'Да':
        bot.send_message(message.chat.id, 'Полная замена трубы.', reply_markup=ReplyKeyboardRemove())
        return_to_start(bot, message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, ответьте "Да" или "Нет".', reply_markup=defect_answer_keyboard)

# =================== Гофры(в/р) ===================
def handle_gofer_defect(bot, message, user_data):
    bot.send_message(
        message.chat.id,
        'Высота гофр более 3 мм или 0,3 толщины стенки трубы при толщине стенки < 10 мм?',
        reply_markup=defect_answer_keyboard
    )
    user_data['previous_state'].append('defect_character_selection')
    user_data['state'] = 'gofer_defect_height_check'

def handle_gofer_defect_height_check(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if message.text == 'Да':
        bot.send_message(message.chat.id, 'Замена или ремонт врезкой катушки.', reply_markup=ReplyKeyboardRemove())
        return_to_start(bot, message)
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, 'Допустимый дефект.', reply_markup=ReplyKeyboardRemove())
        return_to_start(bot, message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, ответьте "Да" или "Нет".', reply_markup=defect_answer_keyboard)

# =================== Дефекты сварных соединений(в/р) ===================
def handle_weld_defect(bot, message, user_data):
    bot.send_message(
        message.chat.id,
        'Оценку работоспособности кольцевых сварных соединений по результатам наружного обследования проводят в соответствии с СТО Газпром 2-2.4-715-2013.',
        reply_markup=ReplyKeyboardRemove()
    )
    return_to_start(bot, message)

# =================== Вмятины(в/р) ===================
def handle_dent_defect(bot, message, user_data):
    bot.send_message(
        message.chat.id,
        'Вмятина глубиной < 6,0 мм при любых значениях длины в окружном и продольных направления?',
        reply_markup=defect_answer_keyboard
    )
    user_data['previous_state'].append('defect_character_selection')
    user_data['state'] = 'dent_depth_check'

def handle_dent_depth_check(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if message.text == 'Да':
        bot.send_message(message.chat.id, 'Относится к допустимым без проведения расчетной оценки.', reply_markup=ReplyKeyboardRemove())
        return_to_start(bot, message)
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, 'Вмятина на сварном соединении?', reply_markup=defect_answer_keyboard)
        user_data['previous_state'].append('dent_depth_check')
        user_data['state'] = 'dent_on_weld_check'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, ответьте "Да" или "Нет".', reply_markup=defect_answer_keyboard)

def handle_dent_on_weld_check(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    user_data['dent_on_weld'] = message.text == 'Да'
    user_data['previous_state'].append('dent_on_weld_check')
    if user_data['dent_on_weld']:
        bot.send_message(message.chat.id, 'Глубина < 2% от наружного диаметра?', reply_markup=defect_answer_keyboard)
    else:
        bot.send_message(message.chat.id, 'Глубина < 5% от наружного диаметра?', reply_markup=defect_answer_keyboard)
    user_data['state'] = 'dent_depth_percentage_check'

def handle_dent_depth_percentage_check(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if message.text == 'Да':
        bot.send_message(message.chat.id, 'Какой тип вмятины? Выберите вариант:', reply_markup=dent_type_keyboard)
        user_data['previous_state'].append('dent_depth_percentage_check')
        user_data['state'] = 'dent_type_selection'
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, 'Замена или ремонт врезкой катушки.', reply_markup=ReplyKeyboardRemove())
        return_to_start(bot, message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, ответьте "Да" или "Нет".', reply_markup=defect_answer_keyboard)

def handle_dent_type_selection(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    if message.text in ['Плавная локальная', 'С внутренним угловым углублением']:
        user_data['dent_type'] = message.text
        user_data['previous_state'].append('dent_type_selection')
        request_dent_calculation_data(bot, message.chat.id, user_data)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, выберите тип вмятины из предложенных вариантов.', reply_markup=dent_type_keyboard)

def request_dent_calculation_data(bot, chat_id, user_data):
    bot.send_message(chat_id, 'Введите значение tф (фактическая толщина стенки), мм:', reply_markup=ReplyKeyboardRemove())
    user_data['state'] = 'dent_tf'

def handle_dent_tf(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['t_f'] = value
        bot.send_message(message.chat.id, 'Введите значение Dн (наружный диаметр трубы), мм:')
        user_data['previous_state'].append('dent_tf')
        user_data['state'] = 'dent_Dn'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для tф.')

def handle_dent_Dn(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['Dn'] = value
        user_data['R0'] = user_data['Dn'] / 2  # Радиус трубы
        bot.send_message(message.chat.id, 'Введите значение d (глубина вмятины), мм:')
        user_data['previous_state'].append('dent_Dn')
        user_data['state'] = 'dent_d'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для Dн.')

def handle_dent_d(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['d'] = value
        bot.send_message(message.chat.id, 'Введите значение L1 (длина вмятины в окружном направлении), мм:')
        user_data['previous_state'].append('dent_d')
        user_data['state'] = 'dent_L1'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для d.')

def handle_dent_L1(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['L1'] = value
        bot.send_message(message.chat.id, 'Введите значение L2 (длина вмятины в продольном направлении), мм:')
        user_data['previous_state'].append('dent_L1')
        user_data['state'] = 'dent_L2'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для L1.')

def handle_dent_L2(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['L2'] = value
        user_data['previous_state'].append('dent_L2')
        calculate_dent_deformations(bot, message.chat.id, user_data)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для L2.')

def calculate_dent_deformations(bot, chat_id, user_data):
    try:
        t_f = user_data['t_f']
        Dn = user_data['Dn']
        d = user_data['d']
        L1 = user_data['L1']
        L2 = user_data['L2']
        R0 = user_data['R0']
        dent_on_weld = user_data['dent_on_weld']
        dent_type = user_data['dent_type']

        # Calculating R1 and R2
        if dent_type == 'Плавная локальная':
            R1 = (d ** 2 + (L1 / b) ** 2) / (b * d)
            R2 = (d ** 2 + (L2 / b) ** 2) / (b * d)
        elif dent_type == 'С внутренним угловым углублением':
            denominator_R1 = d * (c * pi ** 2 - f * (L1 / R0) ** 2)
            if denominator_R1 == 0:
                bot.send_message(chat_id, 'Ошибка: знаменатель при вычислении R1 равен нулю.')
                return_to_start_by_chat_id(bot, chat_id)
                return
            R1 = - (L1 ** 2) / denominator_R1
            R2 = L2 ** 2 / (c * pi ** 2 * d)
        else:
            bot.send_message(chat_id, 'Некорректный тип вмятины.')
            return_to_start_by_chat_id(bot, chat_id)
            return

        # Calculating e1, e2, e3
        e1 = (t_f / b) * (a / R0 - a / R1)
        e2 = (t_f / b) * (a / R2)
        e3 = (a / b) * (d / L2) ** 2

        # Calculating e
        sum_e2_e3 = e2 + e3
        sqrt_argument = e1 ** 2 + e1 * sum_e2_e3 + sum_e2_e3 ** 2
        if sqrt_argument < 0:
            bot.send_message(chat_id, 'Ошибка: подкоренное выражение меньше нуля при вычислении e.')
            return_to_start_by_chat_id(bot, chat_id)
            return
        e = (b / math.sqrt(c)) * math.sqrt(sqrt_argument)
        user_data['e'] = e
        bot.send_message(chat_id, f'Значение эквивалентной деформации e: {e:.7f} %')

        # Final check
        # Используем сохраненное значение dent_on_weld
        if user_data['dent_on_weld']:
            if e < 6:
                bot.send_message(chat_id, 'Допустимый дефект.', reply_markup=ReplyKeyboardRemove())
            else:
                bot.send_message(chat_id, 'Замена или ремонт врезкой катушки.', reply_markup=ReplyKeyboardRemove())
        else:
            if e < 12:
                bot.send_message(chat_id, 'Допустимый дефект.', reply_markup=ReplyKeyboardRemove())
            else:
                bot.send_message(chat_id, 'Замена или ремонт врезкой катушки.', reply_markup=ReplyKeyboardRemove())
        return_to_start_by_chat_id(bot, chat_id)
    except Exception as ex:
        bot.send_message(chat_id, f'Ошибка при вычислении деформаций: {str(ex)}')
        return_to_start_by_chat_id(bot, chat_id)

# =================== Дефекты овализации поперечного сечения(в/р) ===================
def handle_oval_defect(bot, message, user_data):
    bot.send_message(message.chat.id, 'Введите значение Dmax, мм:', reply_markup=ReplyKeyboardRemove())
    user_data['previous_state'].append('defect_character_selection')
    user_data['state'] = 'oval_dmax'

def handle_oval_dmax(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['Dmax'] = value
        bot.send_message(message.chat.id, 'Введите значение Dmin, мм:')
        user_data['previous_state'].append('oval_dmax')
        user_data['state'] = 'oval_dmin'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для Dmax, мм.')

def handle_oval_dmin(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['Dmin'] = value
        bot.send_message(message.chat.id, 'Введите значение Dн, мм:')
        user_data['previous_state'].append('oval_dmin')
        user_data['state'] = 'oval_Dn'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для Dmin, мм.')

def handle_oval_Dn(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['Dn'] = value
        theta = ((user_data['Dmax'] - user_data['Dmin']) / user_data['Dn']) * h
        user_data['theta'] = theta
        bot.send_message(message.chat.id, f'Значение θ: {theta:.3f}%')
        bot.send_message(
            message.chat.id,
            'Введите значение tф (фактическая толщина стенки), мм:',
            reply_markup=ReplyKeyboardRemove()
        )
        user_data['previous_state'].append('oval_Dn')
        user_data['state'] = 'oval_tf'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для Dн, мм.')

def handle_oval_tf(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['tf'] = value
        theta = user_data['theta']
        tf = user_data['tf']
        # Определяем допустимое значение θ
        if tf <= 20:
            theta_limit = 1.0
        else:
            theta_limit = 0.8
        if theta <= theta_limit:
            bot.send_message(message.chat.id, 'Допустимый дефект.', reply_markup=ReplyKeyboardRemove())
            return_to_start(bot, message)
        else:
            bot.send_message(message.chat.id, f'Овальность θ = {theta:.3f}% превышает допустимое значение {theta_limit}%. Переходим к расчету [θ]кр.')
            # Продолжаем дальнейшие расчёты
            user_data['previous_state'].append('oval_tf')
            bot.send_message(message.chat.id, 'Введите значение tн (номинальная толщина стенки), мм:')
            user_data['state'] = 'oval_tn'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для tф, мм.')

def handle_oval_tn(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['tn'] = value
        bot.send_message(
            message.chat.id,
            'Введите значение коэффициента надежности по назначению kн согласно таблице 12 СП 36.13330.2012:',
            reply_markup=ReplyKeyboardRemove()
        )
        user_data['previous_state'].append('oval_tn')
        user_data['state'] = 'oval_kn'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для tн, мм.')

def handle_oval_kn(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['kn'] = value
        bot.send_message(message.chat.id, 'Введите значение p (рабочее давление), МПа:')
        user_data['previous_state'].append('oval_kn')
        user_data['state'] = 'oval_p'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для kн.')

def handle_oval_p(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['p'] = value
        bot.send_message(message.chat.id, 'Введите значение E (модуль упругости), МПа:')
        user_data['previous_state'].append('oval_p')
        user_data['state'] = 'oval_E'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для p, МПа.')

def handle_oval_E(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['E'] = value
        bot.send_message(message.chat.id, 'Введите значение v (коэффициент Пуассона):')
        user_data['previous_state'].append('oval_E')
        user_data['state'] = 'oval_v'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для E, МПа.')

def handle_oval_v(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['v'] = value
        bot.send_message(message.chat.id, 'Введите значение σт (предел текучести), МПа:')
        user_data['previous_state'].append('oval_v')
        user_data['state'] = 'oval_sigma_t'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для v.')

def handle_oval_sigma_t(bot, message, user_data):
    if message.text == 'Назад':
        handle_back_command(bot, message, user_data)
        return
    value = parse_float(message.text)
    if value is not None:
        user_data['sigma_t'] = value
        # Запрашиваем категорию трубопровода для определения m
        user_data['previous_state'].append('oval_sigma_t')
        user_data['state'] = 'select_m_category_theta_kr'
        bot.send_message(
            message.chat.id,
            'Выберите категорию трубопровода и его участка:',
            reply_markup=category_keyboard
        )
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение для σт, МПа.')

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
        bot.send_message(message.chat.id, 'Пожалуйста, выберите одну из категорий: B, 1, 2, 3, 4.', reply_markup=category_keyboard)
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
        E = user_data['E']
        v = user_data['v']
        sigma_t = user_data['sigma_t']
        theta = user_data['theta']
        m = user_data['m']
        sigma_kc = (p * (Dn - b * tf)) / (b * tf)
        omega_okr = a - (c5 * kn * sigma_kc) / (m * sigma_t)
        beta = (a / (a - v**2)) * ((tf / Dn)**2) * (E / sigma_t)
        denominator = a - omega_okr
        if denominator == 0:
            bot.send_message(chat_id, 'Ошибка: знаменатель равен нулю при вычислении [θ]кр.')
            return_to_start_by_chat_id(bot, chat_id)
            return
        theta_kr = ((b * tn) / (c * Dn)) * (omega_okr / beta) * (a + (beta / denominator)) * h
        bot.send_message(chat_id, f'Значение допустимой овальности [θ]кр: {theta_kr:.3f}%')
        if theta <= theta_kr:
            bot.send_message(chat_id, 'Условие θ ≤ [θ]кр соблюдается.')
            bot.send_message(chat_id, 'Подлежит ремонту по п. 7.12.', reply_markup=ReplyKeyboardRemove())
        else:
            bot.send_message(chat_id, 'Условие θ ≤ [θ]кр не соблюдается.')
            bot.send_message(chat_id, 'Замена или ремонт обрезкой катушки.', reply_markup=ReplyKeyboardRemove())
        return_to_start_by_chat_id(bot, chat_id)
    except Exception as e:
        bot.send_message(chat_id, f'Ошибка при вычислении [θ]кр: {str(e)}')
        return_to_start_by_chat_id(bot, chat_id)

# Функции возврата к началу
def return_to_start(bot, message):
    user_data = user_data_from_message(message)
    user_data['state'] = None
    user_data['previous_state'] = []
    bot.send_message(
        message.chat.id,
        'Вы можете начать новый расчет, введя команду /start.',
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/start'))
    )

def return_to_start_by_chat_id(bot, chat_id):
    user_data = user_data_global.get(chat_id, {})
    user_data['state'] = None
    user_data['previous_state'] = []
    bot.send_message(
        chat_id,
        'Вы можете начать новый расчет, введя команду /start.',
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/start'))
    )
