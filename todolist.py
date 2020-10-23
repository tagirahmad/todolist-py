from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    date = Column(Date, default=datetime.today())
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def get_all_todos(session):
    tasks_raw = session.query(Table).order_by(Table.deadline).all()
    if tasks_raw:
        tasks = [f'{task.task}. {task.deadline.day} {task.deadline.strftime("%b")}' for task in tasks_raw]
        for index, todo in enumerate(tasks):
            print(f'{index + 1}. {todo}')

        ids = dict()
        for index, task in enumerate(tasks_raw):
            ids[index] = task.id

        return ids
    else:
        print('Nothing to do!')


def get_todays_tasks(session):
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    if rows:
        tasks = [task.task for task in rows]
        return tasks
    else:
        print('Nothing to do!')


def get_tasks_rows(date, session):
    day_todos = session.query(Table).filter(Table.deadline == date.date()).all()
    if date.weekday() == 0:
        print('')
        print(f'Monday {date.strftime("%b")} {date.day}:')
    elif date.weekday() == 1:
        print('')
        print(f'Tuesday {date.strftime("%b")} {date.day}:')
    elif date.weekday() == 2:
        print('')
        print(f'Wednesday {date.strftime("%b")} {date.day}:')
    elif date.weekday() == 3:
        print('')
        print(f'Thursday {date.strftime("%b")} {date.day}:')
    elif date.weekday() == 4:
        print('')
        print(f'Friday {date.strftime("%b")} {date.day}:')
    elif date.weekday() == 5:
        print('')
        print(f'Saturday {date.strftime("%b")} {date.day}:')
    elif date.weekday() == 6:
        print('')
        print(f'Sunday {date.strftime("%b")} {date.day}:')
        # print('')

    if day_todos:
        for i, day_todo in enumerate(day_todos):
            print(f'{i + 1}. {day_todo}')
        print('')
    else:
        print('Nothing to do!')
        print('')


def get_week_tasks(session):
    today_day = datetime.today()
    tomorrow = today_day + timedelta(days=1)
    day_after_tomorrow = today_day + timedelta(days=2)
    third_day = today_day + timedelta(days=3)
    forth_day = today_day + timedelta(days=4)
    fifth_day = today_day + timedelta(days=5)
    sixth_day = today_day + timedelta(days=6)
    seventh_day = today_day + timedelta(days=7)
    days_times = [
        today_day,
        tomorrow,
        day_after_tomorrow,
        third_day,
        forth_day,
        fifth_day,
        sixth_day,
        seventh_day
    ]
    for day_time in days_times:
        get_tasks_rows(day_time, session)


def create_new_task(task, session, deadline):
    new_row = Table(task=task, date=datetime.now(),
                    deadline=datetime.strptime(deadline, '%Y-%m-%d'))
    session.add(new_row)
    session.commit()


def get_missed_tasks(session):
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline < today.date()).all()
    if rows:
        tasks = [f'{task.task}. {task.deadline.day} {task.deadline.strftime("%b")}' for task in rows]
        for index, todo in enumerate(tasks):
            print(f'{index + 1}. {todo}')
        print('')
    else:
        print('Nothing to do!')


def delete_task(id):
    specific_row = session.query(Table).filter(Table.id == id)[0]
    session.delete(specific_row)
    session.commit()
    print('The task has been deleted!')

program_is_working = True

while program_is_working:
    menu = [
        '1) Today\'s tasks',
        '2) Week\'s tasks',
        '3) All tasks',
        '4) Missed tasks',
        '5) Add task',
        '6) Delete task',
        '0) Exit'
    ]

    for item in menu:
        print(item)

    menu_input = input()

    if menu_input == '1':
        today = datetime.today()
        print(f'Today {today.strftime("%b")} {today.day} :')
        todos = get_todays_tasks(session)
        if todos:
            for index, todo in enumerate(todos):
                print(f'{index + 1}. {todo}')
    elif menu_input == '2':
        get_week_tasks(session)
    elif menu_input == '3':
        print('All tasks:')
        get_all_todos(session)
    elif menu_input == '4':
        print('Missed tasks:')
        get_missed_tasks(session)
    elif menu_input == '5':
        print('Enter task')
        new_task = input()
        print('Enter deadline')
        deadline = input()
        create_new_task(new_task, session, deadline)
        print('The task has been added!')
    elif menu_input == '6':
        print('Choose the number of the task you want to delete:')
        ids = get_all_todos(session)
        index = int(input())
        delete_task(ids[index - 1])
    elif menu_input == '0':
        print('Bye!')
        program_is_working = False
