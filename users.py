# Напишите модуль users.py, который регистрирует новых пользователей. Скрипт должен запрашивать следующие данные:
# имя
# фамилию
# пол
# адрес электронной почты
# дату рождения
# рост
# Все данные о пользователях сохраните в таблице user нашей базы данных sochi_athletes.sqlite3.

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'
    __table_args__ = {'sqlite_autoincrement': True}
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # Пол пользователя
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # дата рождения пользователя
    birthdate = sa.Column(sa.Text)
    # рост пользователя
    height = sa.Column(sa.Float)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Начинаем ввод данных нового пользователя!")
    # запрашиваем у пользователя данные
    first_name = input("Введите имя: ")
    last_name = input("Введите фамилию: ")
    gender = input("Укажите пол (М или Ж): ")
    email = input("Адрес  электронной почты: ")
    birthdate = input("Введите дату рождения (YYYY-MM-DD): ")
    height = input("И последнее - укажите его рост: ")
    # генерируем идентификатор пользователя и сохраняем его строковое представление
    # user_id = str(uuid.uuid4())

    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height,
    )
    # возвращаем созданного пользователя
    return user

def print_users_list(session):
    """
    Выводит на экран список пользователей,
    """
    users = session.query(User).all()
    # проверяем на пустоту список
    if users:
        # проходимся по каждой записи и выводим на экран
        for user in users:
            print("|".join([str(user.id),user.first_name,user.last_name,user.gender,user.email,user.birthdate,str(user.height)]))
            # print()
    else:
        # если список оказался пустым, выводим сообщение об этом
        print("Список пользователей пуст")

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # просим пользователя выбрать режим
    while True:
        mode = input("Выберите:\n1 - добавить пользователя\n2 - посмотреть список пользователей\n3 - завершить\n")
        # проверяем режим
        if mode == "1":
            # запрашиваем данные пользоватлея
            user = request_data()
            # добавляем нового пользователя в сессию
            session.add(user)
            # сохраняем все изменения, накопленные в сессии
            session.commit()
            print("Данные сохранены!\n")
        elif mode =="2":
            # выведем список записей в таблице user
            print_users_list(session)

        elif mode == "3":
            # Завершаем работу и выходим из вечного цикла
            break
        else:
            # Введено что-то другое. Говорим об этом
            print("Вы ввели "+mode+".  Это неверный ввод\n")


if __name__ == "__main__":
    main()

