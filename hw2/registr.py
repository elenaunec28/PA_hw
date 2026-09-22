from pydantic import ValidationError
from models import User

def register_user(json_input: str) -> str:
    try:
        user = User.model_validate_json(json_input)
        return user.model_dump_json()
    except ValidationError as e:
        return f"Ошибкак валидации: {e}"

# Пример JSON данных для регистрации пользователя

if __name__ == "__main__":
    # Ошибка: is_employed=true, но возраст 70 (вне диапазона 18-65)
    json_invalid = """{
            "name": "John Doe",
            "age": 70,
            "email": "john.doe@example.com",
            "is_employed": true,
            "address": {
                "city": "New York",
                "street": "5th Avenue",
                "house_number": 123
            }
        }"""

    # Ошибка: имя из цифр
    json_invalid2 = """{
                "name": "John 12321",
                "age": 70,
                "email": "john.doe@example.com",
                "is_employed": true,
                "address": {
                    "city": "New York",
                    "street": "5th Avenue",
                    "house_number": 123
                }
            }"""

    # Успешная регистрация
    json_valid = """{
        "name": "Alice Smith",
        "age": 30,
        "email": "alice.smith@example.com",
        "is_employed": true,
        "address": {
            "city": "Berlin",
            "street": "Hauptstrasse",
            "house_number": 42
        }
    }"""

print(register_user(json_invalid))
print("----------------------------")
print(register_user(json_invalid2))
print("----------------------------")
print(register_user(json_valid))
