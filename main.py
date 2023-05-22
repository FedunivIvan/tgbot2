import telebot
from telebot import types

bot = telebot.TeleBot('6289893709:AAFm0FZq7lNcucZwhkM4LSsWhpKVK3W8UnQ')

# Словарь с информацией о командах Git
git_commands = {
    "Работа с репозиторием": {
        "git init": {
            "description": "git init - инициализирует новый репозиторий Git",
            "example": "Пример использования: git init"
        },
        "git clone": {
            "description": "git clone - клонирует репозиторий Git на локальную машину",
            "example": "Пример использования: git clone <URL>"
        },
        "git branch": {
            "description": "git branch - показывает список веток в репозитории",
            "example": "Пример использования: git branch"
        },
        "git checkout": {
            "description": "git checkout - переключается на указанную ветку",
            "example": "Пример использования: git checkout <branch>"
        },
        "git merge": {
            "description": "git merge - объединяет выбранную ветку с текущей веткой",
            "example": "Пример использования: git merge <branch>"
        }
    },
    "Откат изменений": {
        "git reset": {
            "description": "git reset - отменяет изменения, возвращая указанный коммит",
            "example": "Пример использования: git reset <commit>"
        },
        "git revert": {
            "description": "git revert - создает новый коммит, отменяющий указанный коммит",
            "example": "Пример использования: git revert <commit>"
        }
    },
    "Отправка и получение изменений": {
        "git push": {
            "description": "git push - отправляет коммиты на удаленный репозиторий",
            "example": "Пример использования: git push origin <branch>"
        },
        "git pull": {
            "description": "git pull - получает и объединяет изменения из удаленного репозитория",
            "example": "Пример использования: git pull origin <branch>"
        }
    },
    "Работа с ветками": {
        "git branch -d": {
            "description": "git branch -d - удаляет указанную ветку",
            "example": "Пример использования: git branch -d <branch>"
        },
        "git branch -m": {
            "description": "git branch -m - переименовывает текущую ветку",
            "example": "Пример использования: git branch -m <new_name>"
        }
    },
    "История и логи": {
        "git log": {
            "description": "git log - показывает историю коммитов",
            "example": "Пример использования: git log"
        },
        "git blame": {
            "description": "git blame - показывает, кто сделал изменения в указанных строках файла",
            "example": "Пример использования: git blame <file>"
        }
    },
    "Удаленные репозитории": {
        "git remote": {
            "description": "git remote - показывает список удаленных репозиториев",
            "example": "Пример использования: git remote"
        },
        "git remote add": {
            "description": "git remote add - добавляет удаленный репозиторий",
            "example": "Пример использования: git remote add <name> <URL>"
        },
        "git remote remove": {
            "description": "git remote remove - удаляет удаленный репозиторий",
            "example": "Пример использования: git remote remove <name>"
        }
    },
    "Игнорирование файлов": {
        "gitignore": {
            "description": "gitignore - файл, содержащий шаблоны игнорируемых файлов и папок",
            "example": "Пример использования: .gitignore"
        }
    },
    "Работа с подмодулями": {
        "git submodule": {
            "description": "git submodule - управление подмодулями",
            "example": "Пример использования: git submodule <command>"
        }
    },
    "Полезные ссылки": {
    "Классная игра на русском языке для изучения гита": {
        "description": "https://learngitbranching.js.org/?locale=ru_RU"
    },
    "Огромная шпора по гиту на русском языке": {
        "description": "https://github.com/cyberspacedk/Git-commands"
    },
    "Линуксовый тренажёр по гиту": {
        "description": "https://github.com/benthayer/git-gud"
    },
    "Бесплатный курс по git": {
        "description": "https://ru.hexlet.io/courses/intro_to_git"
    },
    "Квиз по гиту": {
        "description": "https://www.w3schools.com/quiztest/quiztest.asp?qtest=GIT"
    },
    "Шпаргалка по синтаксису для оформления файла readme.md": {
        "description": "https://gitcareer.com/"
    }
}
}

user_state = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = create_main_menu_markup()
    welcome_message = "Привет! Я бот-справочник по командам Git. Выберите действие из меню ниже:"
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    chat_id = message.chat.id

    if text == "Назад":
        if chat_id in user_state:
            user_state.pop(chat_id)
            markup = create_main_menu_markup()
            welcome_message = "Выберите действие из меню ниже:"
            bot.send_message(chat_id, welcome_message, reply_markup=markup)
    elif text == "Вернуться в главное меню":
        user_state.pop(chat_id, None)
        markup = create_main_menu_markup()
        welcome_message = "Выберите действие из меню ниже:"
        bot.send_message(chat_id, welcome_message, reply_markup=markup)
    elif text in git_commands.keys():
        user_state[chat_id] = text
        subcategories = git_commands[text].keys()
        markup = create_submenu_markup(subcategories)
        markup.add("Вернуться в главное меню")
        response = "Выберите подраздел из списка:"
        bot.send_message(chat_id, response, reply_markup=markup)
    elif chat_id in user_state:
        command = text
        category = user_state[chat_id]
        response = get_command_info(category, command)
        bot.send_message(chat_id, response)
    else:
        bot.send_message(chat_id, "Извините, я не понимаю эту команду. Пожалуйста, выберите команду из меню.")

def create_main_menu_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for command in git_commands.keys():
        markup.add(command)
    return markup

def create_submenu_markup(options):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for option in options:
        markup.add(option)
    return markup

def get_command_info(category, command):
    info = git_commands.get(category, {}).get(command)
    if info:
        description = info.get("description")
        example = info.get("example")
        response = f"Команда: {command}\n\nОписание: {description}\n\nПример использования: {example}"
        return response
    else:
        return "К сожалению, информация о данной команде отсутствует."

bot.polling()