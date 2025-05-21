import os
from dotenv import load_dotenv
import psycopg2
import boto3

class Colors:
    """
    ANSI escape-коды для форматирования текста в терминале.
    Используется для цветного вывода результатов health check.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """
    Печатает заголовок (выделенный синим и жирным шрифтом).

    Args:
        text (str): Текст заголовка.
    """
    print(f"{Colors.OKBLUE}{Colors.BOLD}\n{text}{Colors.ENDC}")

def print_success(text):
    """
    Печатает сообщение об успехе (зелёным цветом).

    Args:
        text (str): Текст сообщения.
    """
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_fail(text):
    """
    Печатает сообщение об ошибке (красным цветом).

    Args:
        text (str): Текст ошибки.
    """
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_info(text):
    """
    Печатает информационное сообщение (фиолетовым цветом).

    Args:
        text (str): Текст сообщения.
    """
    print(f"{Colors.HEADER}{text}{Colors.ENDC}")

load_dotenv()  # Загружаем переменные окружения из .env

def check_pg_connection(host, port, dbname, user, password, role):
    """
    Проверяет подключение к PostgreSQL базе данных.

    Args:
        host (str): Адрес сервера БД.
        port (str or int): Порт сервера БД.
        dbname (str): Имя базы данных.
        user (str): Имя пользователя.
        password (str): Пароль пользователя.
        role (str): Роль/описание базы (например, 'SOURCE (readonly)').

    Returns:
        bool: True если подключение успешно, иначе False.
    """
    print_info(f"Проверка PostgreSQL ({role}):")
    try:
        conn = psycopg2.connect(
            host=host,
            port=int(port) if port else None,
            dbname=dbname,
            user=user,
            password=password,
            connect_timeout=5
        )
        conn.close()
        print_success(f"Успешно подключено к базе данных {role}!")
        return True
    except Exception as e:
        print_fail(f"Ошибка подключения к базе данных {role}: {e}")
        return False

def check_s3_connection(bucket_name, access_key, secret_key):
    """
    Проверяет подключение к S3 бакету в Яндекс Облаке.

    Args:
        bucket_name (str): Имя S3-бакета.
        access_key (str): AWS Access Key ID.
        secret_key (str): AWS Secret Access Key.

    Returns:
        bool: True если подключение успешно, иначе False.
    """
    print_info("Проверка S3:")
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='ru-central1',
            endpoint_url='https://storage.yandexcloud.net'
        )
        # Пробуем получить список файлов
        s3.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
        print_success(f"Успешно подключено к S3 бакету {bucket_name}!")
        return True
    except Exception as e:
        print_fail(f"Ошибка подключения к S3 бакету {bucket_name}: {e}")
        return False

if __name__ == "__main__":
    """
    Точка входа: запускает health check для обеих баз данных и S3 бакета.
    """
    print_header("=== HEALTH CHECK MLE ENVIRONMENT ===")

    # Source DB (readonly)
    check_pg_connection(
        host=os.environ.get("DB_SOURCE_HOST"),
        port=os.environ.get("DB_SOURCE_PORT"),
        dbname=os.environ.get("DB_SOURCE_NAME"),
        user=os.environ.get("DB_SOURCE_USER"),
        password=os.environ.get("DB_SOURCE_PASSWORD"),
        role="SOURCE (readonly)"
    )

    # Destination DB (personal)
    check_pg_connection(
        host=os.environ.get("DB_DESTINATION_HOST"),
        port=os.environ.get("DB_DESTINATION_PORT"),
        dbname=os.environ.get("DB_DESTINATION_NAME"),
        user=os.environ.get("DB_DESTINATION_USER"),
        password=os.environ.get("DB_DESTINATION_PASSWORD"),
        role="DESTINATION (personal)"
    )

    # S3
    check_s3_connection(
        bucket_name=os.environ.get("S3_BUCKET_NAME"),
        access_key=os.environ.get("AWS_ACCESS_KEY_ID"),
        secret_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    print_header("=== CHECK COMPLETE ===\n")
