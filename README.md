# mle-dvc

## Создать файл .env

```python
[default]
# Source Database / Общая БД (только для чтения)
DB_SOURCE_HOST=
DB_SOURCE_PORT=
DB_SOURCE_NAME=
DB_SOURCE_USER=
DB_SOURCE_PASSWORD=

# Destination Database / Индивидуальная БД (запись и чтение)
DB_DESTINATION_HOST=
DB_DESTINATION_PORT=
DB_DESTINATION_NAME=
DB_DESTINATION_USER=
DB_DESTINATION_PASSWORD=

# S3 Connection / Соединение с S3
S3_BUCKET_NAME=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

```

## Создать виртуальное окружение

```bash
sudo vim /etc/resolv.conf
# Добавь строку в настройки DNS: 
# чтобы не было проблем с загрузкой - необходимо установить DNS Google
nameserver 8.8.8.8

python3.10 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
which python
python --version
pip --version
python -c "import dvc; import dotenv; import pandas; import psycopg2; import sklearn; import boto3; print('OK')"
pip install pyarrow
python -c "import dvc; import dotenv; import pandas; import psycopg2; import sklearn; import boto3; print('OK')"
pip freeze > requirements.txt

```