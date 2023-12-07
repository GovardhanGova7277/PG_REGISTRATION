# Project has to be console based menu driven database based project.
# 1. PG booking system: where admin will add the rooms and vacancies,
# users will be able to book them...

import pymysql
from prettytable import PrettyTable 
#connect to the database
db=pymysql.connect(host='localhost',user='root',password='7277',database='pg_booking')

#create a cursor
cur=db.cursor()

#create a table DETAILS if not exist
cur.execute('CREATE TABLE IF NOT EXISTS details (id INT auto_increment PRIMARY KEY, username VARCHAR(255) UNIQUE, password VARCHAR(20), role VARCHAR(30))')

#create table pg_rooms if not exist
cur.execute('CREATE TABLE IF NOT EXISTS pg_details(id INT auto_increment PRIMARY KEY, room_number int unique, vacancies int,f_person varchar(20),s_person varchar(20))')

def sign_up():
    # user login
    username=input('Username: ')
    password=input('Password: ')
    role='user'
    cur.execute(f"insert into details(username,password,role) values('{username}','{password}','{role}')")
    db.commit()

    print('USER SIGN IN SUCCESSFULLY')


def authenticate_user():
    #ask user for the username and password
    username=input('Username: ')
    password=input('Password: ')

    #check is the username and password are correct
    cur.execute(f"select role from details where username='{username}' and password='{password}'")
    result=cur.fetchone()
    if result is None:
        print('Invalid Username or Password.')
        return None
    else:
        role=result[0]
        print(f"Welcome, {username} {(role)}!")
        return role

def view():
    #view the details of the pg by 'admin'
    cur.execute(f'select * from pg_details')
    results=cur.fetchall()

    table=PrettyTable()
    table.field_names=['ID','RoomNumber','Vacancies','FirstName','LastName']
    for result in results:
        table.add_row(result)
        
    print(table)

def add_rooms():
    # admin can add the rooms
    room_number=int(input('Enter the Room Number: '))
    vacancies=int(input('Enter the number of Vacancies: '))
    # inserting into pg_details table by admin only the room_number and vacancies 
    cur.execute(f'insert into pg_details(room_number,vacancies) values ({room_number},{vacancies})')

    db.commit()
    
    print('\nSuccessfully Room is Added')

def view_vacancies():
    
    cur.execute(f'select * from pg_details where vacancies>{0}')
    records=cur.fetchall()

    table=PrettyTable()
    table.field_names=['ID','RoomNumber','Vacancies','FirstName','LastName']
    for record in records:
        table.add_row(record)
    print(table)
    
    db.commit()
    print('\nFirstName and SecondName = "None" (They are Vacant)')

    print('\nYou can Book Your "Room"')
    
def book_room():
    room_no=int(input('Enter the room number you want to Book: '))
    cur.execute(f'select f_person,s_person from pg_details where room_number={room_no}')
    result=cur.fetchall()
    # if the f_name and s_name in the pg_details we will updats the name(book the room using the room)
    if result[0][0]==None and result[0][1]==None:
        print(f'{room_no} has vacancies you can book your room\n')
        name1=input('Enter your name to book the room: ')
        cur.execute(f"update pg_details set f_person='{name1}' where room_number={room_no}")
        db.commit()

        print('\nYou Have successfully Booked your room!!')
        view()
    elif result[0][1]==None:
        print(f'{room_no} has vacancies you can book your room')
        name1=input('Enter your name to book the room: ')
        cur.execute(f"update pg_details set s_person='{name1}' where room_number={room_no}")

        print('\nYou Have successfully Booked your room!!')
        db.commit()
        view()
    elif result[0][0]!=None and result[0][1]!=None:
        print(f'{room_no} The two vacancies are booked\n')

        print('You can book other room which are vacant\n')
        print('"These are the rooms which are vacant"\n')
        view_vacancies()
    else:
        print("You can't book the rooms that are not vacant")
        
    db.commit()
    
#main function
def main():
    #authenticate_user
    
    role=authenticate_user()
    
    if role=='admin':
        while True:
            print('\nMenu Options:')
            print('1. View Room details')
            print('2. Add Rooms')
            print('3. exit')
            choice1=input('Enter your choice: ')

            if choice1=='1':
                view()
            elif choice1=='2':
                add_rooms()
            elif choice1=='3':
                print('Goodbye!')
                break
            else:
                print('Invalid Choice')
                
    elif role=='user':

        while True:
            print('\nMenu Options:')
            print('1.View Vacancie Room Numbers')
            print('2.Book Your rooms')
            print('3.Exit')

            choice3=input('Enter your choice: ')
            if choice3=='1':
                view_vacancies()
            elif choice3=='2':
                book_room()
            elif choice3=='3':
                print('goodbye!')
                break
            else:
                print('Invalid Choice.')
    else:
        print("you don't have access to this system")
            
                
                
    
def start():
    print('PRESS')
    print('1. ALREADY REGISTERED')
    print('2. NOT REGISTERED')
    choice=input('Enter your choice: ')
    if choice=='1':
        main()
    elif choice=='2':
        sign_up()
        print('You can Login Now')
        main()
    else:
        print('Wrong Choice')

#callig the start function        
start()
