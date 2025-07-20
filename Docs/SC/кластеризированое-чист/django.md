СП    -> Страница пагинации
ЧАСТЬ -> Используй данный кластер как часть семантики контента страницы
>>    -> Узнай больше об этом кластере
?>    -> Смотри структуру кластеров в другом файле
(...) -> Похожие, синонимические кластеры
//    -> Комментарии и заметки автора
ХЗ    -> Я не знаю куда и как это использовать

# django
  ## СП >>            django docker
    ЧАСТЬ django docker nginx
    ЧАСТЬ django docker postgres
    ЧАСТЬ django celery docker
  ## СП ?>            django rest 
  ## ЧАСТЬ            django models (django import models, django orm) // Используй следующие кластеры при необходимости как части статей, инструментов
    ЧАСТЬ django model object (django model delete) 
    ЧАСТЬ django get (django get or create) (django get or 404) 
    ЧАСТЬ django create (django запись в базу данных, django add) 
    ЧАСТЬ django user 
    ЧАСТЬ django fields (django поля) (django models поля) (default value django) 
    ЧАСТЬ django filter (django фильтры) 
    ЧАСТЬ django name 
    ЧАСТЬ django миграции 
    ЧАСТЬ django file (django загрузка файлов) (django файлы) (django import file) (django model file) 
    ЧАСТЬ django verbose 
    ЧАСТЬ django list 
    ЧАСТЬ django one to one 
    ЧАСТЬ foreign key django 
    ЧАСТЬ django many to many 
    ЧАСТЬ django queryset 
    ЧАСТЬ django id 
    ЧАСТЬ django update 
    ЧАСТЬ constraint django 
    ЧАСТЬ django related 
    ЧАСТЬ django choices / Как использовать данное поле
    ЧАСТЬ django ordering (order by django) C / Как использовать данный фильтр
    ЧАСТЬ django связи (связанные объекты django) C / Как связывать между собой разные модели
    ЧАСТЬ django db connection (django connections, ) / Как подключиться к базе данных
    ЧАСТЬ django array C / Специф. полt для PostgreSQL, как добавить аналоги для других дб
    ЧАСТЬ django number field
    ЧАСТЬ django фото
  ## СП + СТАТЬЯ      django admin (django панель) // Написать гайд, про то как поменять админку по умолчанию под себя
    СТАТЬЯ cpanel django // Как поменять стандартную админку на cPanel
    $ СТАТЬЯ django grappelli // Как поменять стандартную админку на Grappelli
    $ СТАТЬЯ django jet // Как поменять стандартную админку на Jet
    СТАТЬЯ django grafana // Фреймворк для мониторинга состояния сайта/приложений на сайте, настройка
    $ СТАТЬЯ django baton // Как поменять стандартную админку на baton
    ЧАСТЬ django admin forms // Как переопределять Django формы и шаблоны в админке
    ЧАСТЬ django inline // Про инлайн режим
    ЧАСТЬ django admin url 
    ЧАСТЬ display django // Про отображение списков записей в бд
    ЧАСТЬ django admin actions 
    ЧАСТЬ django admin ordering 
    ЧАСТЬ django admin fields 
    ЧАСТЬ django admin filter 
    ЧАСТЬ django user groups
    ЧАСТЬ django permissions
  ## СП               сайт на django (django site, создание сайта на django) // Для показа процесса создания тех или иных сайтов (SRP, PeoBel)
    СП django магазин // про то как создать интернет магазин
    СП django ecommerce // про то как создать ecommerce сайт
    СП django проект для управления задачами // про то как создать проект по управлению задачами
  ## СП-ИНСТРУМЕНТОВ  django примеры (django примеры скачать, django примеры проектов, django by example, websites built with django) // Готовые сайты для скачивания или другие сайты
  ## ХЗ               venv django (django requirements)
  ## СП               хостинг django (deploying django) (как развернуть django)
    СТАТЬЯ django reg // Как развернуть сайт на reg.ru /DONE
    СТАТЬЯ nginx django (django nginx) // Как развернуть сайт c nginx
    $ СТАТЬЯ digitalocean django // Как развернуть сайт на digitalocean
    $ СТАТЬЯ serverless django // Как развернуть сайт без сервера
    СТАТЬЯ hostinger django // Как развернуть сайт на hostinger
    СТАТЬЯ перенос django // Как перенести сайт с одного хостинга на другой
    СТАТЬЯ apache django // Как развернуть сайт c apache
    СТАТЬЯ heroku django // Как развернуть сайт, проект 
    СТАТЬЯ vercel django // Как быстро развернуть сайт
    СТАТЬЯ django elastic beanstalk // Как развернуть сайт
    СТАТЬЯ netlify django // Как развернуть сайт
    $ СТАТЬЯ django gunicorn // Как развернуть сайт
  ## СП               django db
    СТАТЬЯ django postgresql // Как подключить, особенности работы с django, преимущества-недостатки
    СТАТЬЯ django mysql // Как подключить, особенности работы с django, преимущества-недостатки
    СТАТЬЯ django sql // Как подключить, особенности работы с django, преимущества-недостатки
    СТАТЬЯ django mongodb // Как подключить, особенности работы с django, преимущества-недостатки
    СТАТЬЯ psycopg2 django // Как подключить, особенности работы с django, преимущества-недостатки
    СТАТЬЯ django sqlite3 // Как подключить, особенности работы с django, преимущества-недостатки
    СТАТЬЯ django firebase // Как подключить, особенности работы с django, преимущества-недостатки
    СТАТЬЯ django несколько баз // Как и можно ли использовать несколько баз данных одновременно
    СТАТЬЯ django dynamodb // Как подключить, особенности работы с django, преимущества-недостатки
    СТАТЬЯ django redis // Как подключить, особенности работы с django, преимущества-недостатки
    СТАТЬЯ django cassandra // Как подключить, особенности работы с django, преимущества-недостатки
  ## СП               django auth
    СТАТЬЯ django регистрация // Как настроить нативную регистрацию
    СТАТЬЯ social django // Как настроить нативную аутентификацию
    СТАТЬЯ django 2fa // Как настроить нативную двухфакторную аутентификацию
    СТАТЬЯ django single sign on // Как настроить и(или) подключить SSO к сайту
    СТАТЬЯ django auth0 // Интеграция со сторонней организацией для SSO-like аутентификации. Как настроить и подключить такую аутентификацию
    СТАТЬЯ oauth2 django // Пакет по настройке аутентификации
    СТАТЬЯ django djoser // Пакет по настройке аутентификации
    СТАТЬЯ django keycloak // Пакет по настройке аутентификации
    СТАТЬЯ django otp // Пакет для создания аутентификации с одноразовым паролем
    СТАТЬЯ django knox // Пакет по настройке аутентификации
    ЧАСТЬ django get user 
    ЧАСТЬ django auth user
    ЧАСТЬ django ldap
    ЧАСТЬ django auth backend
  ## СТАТЬЯ           django forms (django forms fields, crispy django) // Сделать полный гайд по созданию форм на django
    ЧАСТЬ widget django (django forms select) (django custom widget) 
    ЧАСТЬ django modelform (django forms views) (django form class)
    ЧАСТЬ валидация django 
    ЧАСТЬ django captcha (recaptcha django) 
    ЧАСТЬ initial django  // Про то как задать изначальные параметры для формы
    ЧАСТЬ django обязательное поле 
    ЧАСТЬ django форма отправки 
  ## СП               django and (django with )
    СП >> django and react (django react) // Frontend фреймворк
    СП >> vue django // Frontend фреймворк
    СП >> django angular // Frontend фреймворк
    СП >> django flutter // Frontend фреймворк
    СП >> next js django // Frontend фреймворк 
    СП >> svelte django // Frontend фреймворк
    СТАТЬЯ django jquery // JS-заменитель
    СТАТЬЯ django bootstrap (django bootstrap 4) // UI библиотека
    СТАТЬЯ django tailwind // CSS-заменитель, почти UI библиотека
    СТАТЬЯ django vite // Frontend-build инструмент
    
    СТАТЬЯ stripe django // Система оплаты
    
    СТАТЬЯ django kubernetes // Система управления несколькими сервисами/контейнерами
    
    СТАТЬЯ django node // Пакетный менеджер
    СТАТЬЯ conda django // Пакетный менеджер, аналог pip8
    
    СТАТЬЯ django graphql // Метод общения с сервером, аналог REST API
    СТАТЬЯ django kafka // Метод общения с сервером, аналог REST API
    СТАТЬЯ django grpc // Метод общения с сервером, аналог REST API8
    
    ИНСТРУМЕНТ >> celery django (django celery) // Ассинхронный распределитель задач
    ИНСТРУМЕНТ >> cron django // Поверменной выполнитель задач
    ИНСТРУМЕНТ >> django huey // Ассинхронный распределитель задач, аналог celery8☻
    
    ИНСТРУМЕНТ >> django elasticsearch // Пакет по добавления Поиска по моделям
    ИНСТРУМЕНТ >> django haystack  // Пакет по добавления Поиска по моделям
    ИНСТРУМЕНТ >> pandas django // Пакет по работе с таблицами и документами
    ИНСТРУМЕНТ >> django tables // Некое встроенное django-приложение для генерации таблиц из моделей
    ИНСТРУМЕНТ >> django tables2 // Пакет по созданию таблиц из моделей
    ИНСТРУМЕНТ >> spectacular django // Пакет по автоматической документации REST API
    $ ИНСТРУМЕНТ >> django swagger // Пакет по автоматической документации REST API
    
    ИНСТРУМЕНТ >> django matplotlib // Пакет по визуализации данных
    $ ИНСТРУМЕНТ >> django chart // Пакет по визуализации данных
    
    $ ИНСТРУМЕНТ >> geodjango // Пакет для работы с картами
    ИНСТРУМЕНТ >> django leaflet // Пакет для работы с картами

    СП django quill // Библиотека для создания WYSIWYG редакторов /DONE

    ИНСТРУМЕНТ >> django silk (django profiling) C // Пакет про профайлинг и отладку
    ИНСТРУМЕНТ >> django postman // Фреймворк для тестирования API
    ИНСТРУМЕНТ >> selenium django // Фреймворк для тестирования
    ИНСТРУМЕНТ >> django jenkins // Фреймворк для тестирования
    ИНСТРУМЕНТ >> opentelemetry django // Пакет про профайлинг и отладку
    ИНСТРУМЕНТ >> datadog django // Пакет про профайлинг и отладку

    ИНСТРУМЕНТ >> django opencv // Пакет для работы компъютерного зрения

    СТАТЬЯ cloudinary django // Пакет для работы с медиа файлами

    ИНСТРУМЕНТ >> django fsm // Пакет для работы с состояниями

    ИНСТРУМЕНТ >> webrtc django // Пакет для работы с потоковыми данными
    ИНСТРУМЕНТ >> django websocket // Пакет для работы с потоковыми данными, Django Channels аналог

    ИНСТРУМЕНТ >> django twilio // Пакет для работы с СМС и Звуковыми сообщениями

    ИНСТРУМЕНТ >> sendgrid django (django mailgun) // Пакет для отправки почтовых сообщений // Возможность отправлять почту с переключением бэкенда
  ## $ СТАТЬЯ           django use (для чего нужен django) // Где и как применяется Django
  ## СП               django exceptions (django ошибки)
    СТАТЬЯ operationalerror django
    СТАТЬЯ django no module named
    СТАТЬЯ improperlyconfigured django
    СТАТЬЯ django importerror
    СТАТЬЯ django cannot import name
    СТАТЬЯ noreversematch django
    СТАТЬЯ django templatedoesnotexist
    СТАТЬЯ django admin not found
    СТАТЬЯ django db utils programmingerror (django db utils programmingerror ошибка отношение)
    СТАТЬЯ django db utils integrityerror (django integrityerror)
    СТАТЬЯ fielderror django  (field error django)
    СТАТЬЯ django no such table
    СТАТЬЯ object has no attribute django
    СТАТЬЯ django db utils operationalerror connection failed
    СТАТЬЯ does not exist django
    СТАТЬЯ имя django admin не распознано
    СТАТЬЯ no matching distribution found for django
    СТАТЬЯ django reverse for not found
    СТАТЬЯ unresolved reference django
    СТАТЬЯ connection refused django
    СТАТЬЯ django db migrations exceptions inconsistentmigrationhistory
    СТАТЬЯ django relation does not exist
    СТАТЬЯ django core exceptions appregistrynotready
  ## ХЗ               django шаблоны (django templates, django переменные, django теги, django length, язык шаблонов django)
  ## СП-ИНСТРУМЕНТОВ  django приложения (django apps, django sass) // Бесплатные django-приложения для скачивания
  ## СТАТЬЯ           django response file // О том как вернуть файл вместо html
  ## СТАТЬЯ           django static (django media, django collectstatic, django css) // О том, как управлять файлами и куда их сохранять
  ## СТАТЬЯ           django post (django csrf) // Как отправлять POST-запросы
  ## СТАТЬЯ           django email (django отправка email) // Как отправить email и подключиться к email-провайдерам
  ## СП               django с нуля (django для начинающих, django уроки, курс по django)
    СТАТЬЯ django проект (django hello world) // Кажется уже есть перепроверь
  ## СТАТЬЯ           django tests // Как писать тесты для Django
  ## СТАТЬЯ           django jinja // Как сменить бэкенд Django шаблонов
  ## СТАТЬЯ           django redirect // Всё о редиректах в Django и какие и когда использовать
  ## СТАТЬЯ           django environment // Как сконфигирировать Django проект через переменные окружения
  ## ИНСТРУМЕНТ       django pdf // Как генерировать PDF файлы, сделай инструмент(Или улучши Редактор постов) + статьи объясняющие его работу
  ## СП               django cache // Топик большой, будет целая серия 
  ## СТАТЬЯ           django vs code // Покажи как установить и настроить расширения
  ## $ СТАТЬЯ           структура django // Про то как можно структурировать свой проект
  ## $ СТАТЬЯ           книги по django (django книга скачать, django в pdf скачать) // Обзор и рейтинг книг по Django
  ## СТАТЬЯ           django 404 (not found django) // Про страницу 404 /DONE
  ## СП               django vs // Сравнение Django с другими фреймворками
    СТАТЬЯ fastapi или django (django fastapi)
    СТАТЬЯ flask или django
    СТАТЬЯ django vs symfony
  ## СТАТЬЯ           как запустить сервер django // Про то как развернуть django на vps сервере
  ## ХЗ               django async
  ## СТАТЬЯ           django telegram // Как сделать ТГ бота на django
  ## ИНСТРУМЕНТ       django excel // Пример работы с exel файлами
  ## СТАТЬЯ           как удалить django // Про то как делать приложения на джанго так чтобы их было легко удалять
  ## ХЗ               django thread (django main thread) 
  ## СТАТЬЯ           django register tag // Как зарегистрировать кастомный тег
  ## СТАТЬЯ           django practice // Собери лучшие практики при разработке