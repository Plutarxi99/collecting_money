# Collect money
Приложение для создания групповых платежей и отправка письма о создании сбора и платеже.

<details>

<summary>Данный проект содержит в себе 3 приложения:</summary>

* **collect**
   - позволяет работать с групповыми сборами:
       - в ней переопределен метод save с установкой значений в поля amount_now and count_people
       - имеет класс для выбора причины сбора Reason
       - имеет celery задачу на отправку письма при успешном создании сбора
       - все get запросы обложены кэшем
       - имеет команду наполнения моко данными addcol
* **payment**
   - позволяет работать с платежами
       - создаёт платежи и привязывает по связи M2M с полем donates с таблицей Collect
       - создана celery задача на отправку письма и надобалвении платежа и обработка платежа
       - имеет команду наполнения моко данными addpay
* **users**
   - служит для аунтификации пользователя и регистрации пользователя, а также получения токена
       - имеет команду наполнения моко данными adduser 
</details>

<details>

<summary>Что делает приложение?</summary>
Функционал:

* Регистрация пользователя, получение токена и использование в запросах bearer token
* Создание группового платежа и отправка письма о его создании с таким содержанием
![Screenshot from 2024-04-04 00-40-23](https://github.com/Plutarxi99/collecting_money/assets/132927381/b557bbec-990e-4d30-ad03-ec667eb5c001)
* Платеж с получением письма о состояние платежа с таким содержанием
![Screenshot from 2024-04-04 00-41-24](https://github.com/Plutarxi99/collecting_money/assets/132927381/f794f109-43a8-4eee-ac72-50c4285fffa1)
* CRUD обложен на групповые сборы, а также ваиладация на актуальную дату времени и права на удаление и обновление только своих сборов


</details>

> [!IMPORTANT]
> Добавлен файл https://github.com/Plutarxi99/mailing_list/blob/main/.env.sample (для использования надо привести к ввиду **<.env>**) с помощью, которого можно настроить работу проекта. В нем лежат настройки (далее идут примеры заполнения полей):
<details>
<summary>Настройки, которые надо установить для работы приложения</summary>

| Значение | Содержание | Примечание |
|-----|-----------|-----:|
|     **SECRET_KEY**| django-insecure-hu213gr51uh234gbrtf34oqufg35835g3q5g       |     код генерируется автоматически при создании приложения|
|     **POSTGRES_DB**| NAME_BD   |     название базы данных |
|     **POSTGRES_USER**| USER_BD   |     название пользователя базы данных |
|     **POSTGRES_PASSWORD**| PASSWORD_BD   |     пароль базы данных |
|     **POSTGRES_HOST**| HOST_BD   |     название твоего сервиса используемый для контейнеризации |
|     **SUPERUSER_EMAIL**| email_superuser       |     установить почту суперюзера|
|     **SUPERUSER_PASSWORD**| password_superuser       |     установить пароль суперюзера|
|     **USER_PASSWORD**| password_user       |     установить пароль юзера|
|     **TELEGRAM_TOKEN**| 1234567899:QWERTYUIOPSSDFGHJKLZXCVBNM<>QWERTYU         |     телеграмм токен полученный от Bot_Father|
|     **CELERY_BROKER_URL_LOCAL**| <pre><code>redis://127.0.0.1:6379</code></pre>    |     база данных для работы celery|
|     **CELERY_RESULT_BACKEND_LOCAL**| <pre><code>redis://127.0.0.1:6379</code></pre>    |     база данных для работы celery|
|     **CELERY_BROKER_URL_DOCKER**| <pre><code>redis://redis:6379</code></pre>    |     база данных для работы celery в контейнере|
|     **CELERY_RESULT_BACKEND_DOCKER**| <pre><code>redis://redis:6379</code></pre>    |     база данных для работы celery в контейнере|
|     **CHAT_ID_TG_TEST**| 123456789   |     получение chat id пользователя для работы кастомной команды проверки бота|
|     **ENV_TYPE**| local/server   |     для использования разных настроек для запуска локально-local для запуска с сервера-server |
|     **HOST_IP**| 0.0.0.0   |     id- адрес твоего сервера базы данных |
</details>

<details>

<summary>Как использовать?</summary>

* Переходим в папку где будет лежать код

* Копируем код с git:
  <pre><code>git clone git@github.com:Plutarxi99/collecting_money.git</code></pre>

* Создаем виртуальное окружение:
  <pre><code>python3 -m venv env</code></pre>
  <pre><code>source env/bin/activate</code></pre>

* Создать секретный ключ:
  <pre><code>openssl rand -hex 32</code></pre>

* Вставить его в .env

* Создать базу данных:
  <pre><code>psql -U postgres</code></pre>
  <pre><code>create database name_your_db;</code></pre>

* После установки нужных настроук в файле **<.env>**. Надо выполнить команду для установки пакетов:
  <pre><code>pip install -r requirements.txt </code></pre>

* Применить миграции:
  <pre><code>python3 manage.py migrate</code></pre>

* Создать суперюзера:
  <pre><code>python3 manage.py ccsu</code></pre>

* Создать пользователей системы (P.S можно использовать любой число, есть и другие параметры, смотри в докстринги) <a href="https://github.com/Plutarxi99/collecting_money/blob/a3b5201763ee284159e2dd864e51741419a30fff/users/management/commands/adduser.py">смотри код</a> :
  <pre><code>python3 manage.py adduser 10</code></pre>

* Создать групповые сборы (P.S можно использовать любой число):
  <pre><code>python3 manage.py addcol 10</code></pre>

* Создать платежи (P.S можно использовать любой число):
  <pre><code>python3 manage.py addpay 10</code></pre>

* Для запуска работы celery worker:
  <pre><code>python3 manage.py celery_worker</code></pre>
  или использовать иную команду дефолтную
  <pre><code>python -m celery -A django worker -l infor</code></pre>


</details>

<details>

<summary>Что использовалось в приложение?</summary>
Функционал:

* Подключено rest_framework для использоваеть API приложения
* Подключено rest_framework_simplejwt для использоваеть API приложения авторизации пользователя Bearer token
* Подключено drf_yasg для создания автоматической документации и возможность работать в браузере с приложением
* Подключено django_filters для использоваеть API приложения в публичных привычках филтрации по приятным привычкам и по дате начало привычек
* Подключена django_celery_beat для использования и создание переодической задачи
* Подключена django_celery для создание и использование отложенной задачи
* Обложил тестами CRUD привычек.
</details>

<details>

<summary>Запуск приложения на удаленном сервере из docker</summary>

* Переходим в папку где будет лежать код:
  <pre><code>cd /var/www/html/</code></pre>

* Копируем код с git:
  <pre><code>git clone <URL on GIT></code></pre>
  
* Копируем .env файл свои значения переменных и поменять в файле проекта deploy/habit_tracker: server_name <HOST_IP>;


* Далее выполнить bash команда на установку нужных компанентов и копирование настроек сайта для его работы:
  <pre><code>cd /var/www/html/habit_tracker/deploy/</code></pre>
  <pre><code>sh deploy_bash.sh</code></pre>

* Создаем виртуальное окружение:
  <pre><code>python3 -m venv env</code></pre>
  <pre><code>source env/bin/activate</code></pre>

* Создаем контейнер:
  <pre><code>docker-compose build</code></pre>
  
* Поднимаем контейнер в фоновом режиме:
  <pre><code>docker-compose up -d</code></pre>


</details>
