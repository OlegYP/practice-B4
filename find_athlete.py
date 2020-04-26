# Напишите модуль find_athlete.py поиска ближайшего к пользователю атлета. Логика работы модуля такова:
#
# запросить идентификатор пользователя;
# если пользователь с таким идентификатором существует в таблице athelete, то вывести на экран двух атлетов:
# ближайшего по дате рождения к данному пользователю и ближайшего по росту к данному пользователю;
# если пользователя с таким идентификатором нет, вывести соответствующее сообщение.
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

class Athelete(Base):
    """
    Описывает структуру таблицы athelete для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'athelete'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # возраст
    age = sa.Column(sa.Integer)
    # дата рождения пользователя
    birthdate = sa.Column(sa.Text)
    # Пол пользователя
    gender = sa.Column(sa.Text)
    # рост пользователя
    height = sa.Column(sa.Float)
    # имя
    name = sa.Column(sa.Text)
    # вес пользователя
    weight = sa.Column(sa.Float)
    # золотые медали
    gold_medals = sa.Column(sa.Integer)
    # серебрянные медали
    silver_medals = sa.Column(sa.Integer)
    # бронзовые медали
    bronze_medals = sa.Column(sa.Integer)
    # всего медалей
    total_medals = sa.Column(sa.Integer)
    # вид спорта
    sport = sa.Column(sa.Text)
    # страна
    country = sa.Column(sa.Text)

    def __str__(self):
        mylist = [str(self.id), str(self.age), self.birthdate, self.gender]
        mylist += [str(self.height), self.name, str(self.weight), str(self.gold_medals)]
        mylist += [str(self.silver_medals), str(self.bronze_medals), str(self.total_medals), self.sport, self.country]
        return "|".join(mylist)

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

def print_atheletes_list(session):
    """
    Выводит на экран список пользователей,
    """
    atheletes = session.query(Athelete).all()
    # проверяем на пустоту список
    if atheletes:
        # проходимся по каждой записи и выводим на экран
        for athelete in atheletes:
            # print("|".join([str(athelete.id),str(athelete.age),athelete.birthdate,athelete.gender,athelete.name,athelete.sport,athelete.country]))
            print(athelete)
    else:
        # если список оказался пустым, выводим сообщение об этом
        print("Список пользователей пуст")

def time_delta(date1,date2):
    return abs(datetime.datetime.strptime(date1, "%Y-%m-%d") - datetime.datetime.strptime(date2, "%Y-%m-%d"))

def request_and_find(session):
    """
    Запрашивает id атлета
    """
    try:
        input_id = int(input("Введите идентификатор атлета в виде числа: "))
    except ValueError:
        print("Вы вввели не число")
        return
    # if not (input_id > 0):
    #    print("Неверный ввод")
    #    return
    my_athelete = session.query(Athelete).filter(Athelete.id == input_id).first()
    if not my_athelete:
       print('\nАтлета с таким идентификатором не найдено')
       return
    # Читаем всю таблицу
    ath_list = session.query(Athelete).all()
    athlete_b = Athelete()
    athlete_h = Athelete()
    min_height = 100;
    min_time_delta = datetime.timedelta(days=99000)
    # Перебираем всю таблицу и ищем нужных атлетов
    # ближайшего по дате рождения ( birthdate) и ближайшего по росту ( height )
    for ath in ath_list:
        # если текущий атлет отличается от найденного ранее, то продолжаем
        if (my_athelete.id != ath.id):
            # если у кого-то нет информации по росту, то дальше ничего не надо делать.
            if (ath.height is not None) and (my_athelete.height is not None):
                if (abs(my_athelete.height - ath.height) < min_height):
                    min_height = abs(my_athelete.height - ath.height)
                    athlete_h = ath
            # если у кого-то нет информации по дате, то дальше ничего не надо делать.
            if (ath.birthdate is not None) and (my_athelete.birthdate is not None):
                if time_delta(ath.birthdate,my_athelete.birthdate) < min_time_delta:
                    min_time_delta = time_delta(ath.birthdate,my_athelete.birthdate)
                    athlete_b = ath

    # Если дошли до этого места, то атлета с нужным id мы точно нашли
    print('Информация о нашем атлете:')
    print(my_athelete)
    if athlete_b.id is not None:
        print('\nИнформация о ближайшем по дате рождения атлете '+"(разница в дате = "+str(min_time_delta)+"):")
        print(athlete_b)
    else:
        print("\nИнформация о ближайшем по дате рождения атлете не найдена")

    if athlete_h.id is not None:
        print('\nИнформация о ближайшем по росту атлете '+"(разница в росте = "+str(min_height)+"):")
        print(athlete_h)
    else:
        print("\nИнформация о ближайшем по росту рождения атлете не найдена")

    print('\n\n')
    return

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # просим пользователя выбрать режим
    while True:
        mode = input("\nВыберите:\n1 - Запрос id атлета и вывод резудьтата\n2 - посмотреть список атлетов\n3 - завершить\n")
        # проверяем режим
        if mode == "1":
            # узнаем id и выведем результат
            request_and_find(session)
        elif mode =="2":
            # выведем список записей в таблице athelete
            print_atheletes_list(session)
        elif mode == "3":
            # Завершаем работу и выходим из вечного цикла
            break
        else:
            # Введено что-то другое. Говорим об этом
            print("Вы ввели "+mode+".  Это неверный ввод\n")


if __name__ == "__main__":
    main()