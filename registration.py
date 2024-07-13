from session import Session
from db import cursor, conn, commit
from models import User
from utils import Response, hash_password, match_password

session = Session()


@commit
def register(username: str, password: str):
    get_user_by_username = '''
    select * from users where username = %s;
    '''
    cursor.execute(get_user_by_username, (username,))
    user_data = cursor.fetchone()
    if user_data:
        return Response('Username already taken', 409)
    
    hashed_password = hash_password(password)
    
    insert_user_query = '''
    insert into users (username, password, role, status, login_try_count) 
    values (%s, %s, %s, %s, %s);
    '''
    cursor.execute(insert_user_query, (username, hashed_password, 'user', 'active', 0))
    
    return Response('User successfully registered', 201)


@commit
def login(username: str, password: str):
    user: User | None = session.check_session()
    if user:
        return Response('You already logged in', 404)
    get_user_by_username = '''
    select * from users where username = %s;
    '''
    cursor.execute(get_user_by_username, (username,))
    user_data = cursor.fetchone()
    if not user_data:
        return Response('User not found', 404)
    user = User(username=user_data[1], password=user_data[2], role=user_data[3],
                status=user_data[4], login_try_count=user_data[5])
    if not match_password(password, user_data[2]):
        update_user_query = '''
        update users set login_try_count = login_try_count + 1 where username = %s;
        '''
        cursor.execute(update_user_query, (username,))
        return Response('Wrong Password', 404)
    session.add_session(user)
    return Response('User successfully logged in', 200)


if __name__ == "__main__":
    response = register('Biloliddin', 'admin123')
    print(f"Registration: {response.data}, Status Code: {response.status_code}")

    response = login('Bilol', 'admin123')
    print(f"Login: {response.data}, Status Code: {response.status_code}")

    if response.status_code == 200:
        print('True')
    else:
        print('False')
