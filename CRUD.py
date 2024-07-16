from models import User, UserRole, UserStatus
from utils import hash_password

@commit
def create_user(username: str, password: str, role: UserRole, status: UserStatus):
    hashed_password = hash_password(password)
    query = """
    INSERT INTO users (username, password, role, status, login_try_count)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id;
    """
    cursor.execute(query, (username, hashed_password, role.value, status.value, 0))
    user_id = cursor.fetchone()[0]
    return user_id

def read_user(user_id: Optional[int] = None, username: Optional[str] = None):
    query = "SELECT id, username, role, status, login_try_count FROM users WHERE "
    if user_id:
        query += "id = %s;"
        cursor.execute(query, (user_id,))
    elif username:
        query += "username = %s;"
        cursor.execute(query, (username,))
    else:
        raise ValueError("Either user_id or username must be provided")
    
    return cursor.fetchone()

@commit
def update_user(user_id: int, username: Optional[str] = None, 
                password: Optional[str] = None, role: Optional[UserRole] = None, 
                status: Optional[UserStatus] = None, login_try_count: Optional[int] = None):
    query = "UPDATE users SET "
    updates = []
    params = []
    
    if username:
        updates.append("username = %s")
        params.append(username)
    if password:
        updates.append("password = %s")
        params.append(hash_password(password))
    if role:
        updates.append("role = %s")
        params.append(role.value)
    if status:
        updates.append("status = %s")
        params.append(status.value)
    if login_try_count is not None:
        updates.append("login_try_count = %s")
        params.append(login_try_count)
    
    if not updates:
        raise ValueError("At least one field must be provided for update")
    
    query += ", ".join(updates) + " WHERE id = %s RETURNING id;"
    params.append(user_id)
    cursor.execute(query, params)
    return cursor.fetchone()[0]

@commit
def delete_user(user_id: int):
    query = "DELETE FROM users WHERE id = %s RETURNING id;"
    cursor.execute(query, (user_id,))
    return cursor.fetchone()[0]
