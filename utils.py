import bcrypt

class Response:
    def __init__(self, data: str, status_code: int):
        self.data = data
        self.status_code = status_code


def hash_password(raw_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(raw_password.encode(), salt)
    return hashed.decode()


def match_password(raw_password: str, encoded_password: str) -> bool:
    return bcrypt.checkpw(raw_password.encode(), encoded_password.encode())


if __name__ == "__main__":
    raw_password = "my_secret_password"
    hashed_password = hash_password(raw_password)
    print(f"Hashed Password: {hashed_password}")

    is_match = match_password("my_secret_password", hashed_password)
    print(f"Passwords match: {is_match}")