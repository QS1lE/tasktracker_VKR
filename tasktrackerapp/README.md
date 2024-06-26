Тестовое задание: таск-трекер.


Простой таск-трекер с возможностью создания задач и проектов. Разработан с использованием языка программирования Python и фреймворка Django.


Фичи ТаскТрекера:

1. Две страницы просмотра задач: "Все задачи" и "Задачи по проектам".
2. Панель навигации с разделами: "Все задачи", "Задачи по проектам" и "О трекере".
3. Сортировка задач по различным столбцам: название, дэдлайн, напоминание, статус, пользователь.
4. Возможность создания задач и проектов с заполнением обязательных полей.
5. Отображение информации о задаче при клике на её название.
6. Изменение и удаление задач/проектов через соответствующие кнопки.
7. Краткая инструкция в разделе "О трекере" (продублировано внизу readme.md в инструкции к приложению).

<details>
<summary>Для работы приложения инструкция к установке </summary>

- Клонировать репозиторий:
  
```bash
git clone https://github.com/BobrovGH/tasktrackerapp.git
```


- Создать вирутальное окружение
```bash
python -m venv venv
```
- Активировать виртуальное окружение
```bash
venv\Scripts\activate
```
```bash
source venv/bin/activate
```
- Установить зависимостей из файла requirements.txt:
```bash
pip install -r requirements.txt
```
- Запустить локальный сервер
```bash
py manage.py runserver
```


</details>


Сриншоты интерфейса представлены в папке screenshots. Ниже есть инструкция к приложению.
<details>
<summary>Инструкция к приложению </summary>

**Панель навигации**

В ТаскТрекере для задач есть 2 страницы просмотра:
- страница «Все задачи» — они представлены одной большой таблицей,
- страница  «Задачи по проектам» они сгруппированы в таблицы по проектам (в виде карточек с названием и описанием проекта).
Для переключения между страницами просмотра используется верхняя панель навигации, также включающая раздел «О трекере».

**Страницы просмотра**
В обоих страницах просмотра, в таблицах в заголовках столбцов справа от названия есть кнопка для сортировки таблицы по содержимому столба, а именно:
- Задача — название задачи. Название кликабельно, по нему можно открыть всю информацию о задаче;
- Дэдлайн — срок, к которому нужно выполнить задачу;
- Напоминание — дата и время, для присыпания напоминания о задаче;
- Статус — статус задачи
- Пользователь —  ответственный за задачу пользователь
- Действия — кнопки для изменения (жёлтая) и для удаления (красная) задачи.
На странице «Все задачи» есть ещё столбец с названием проекта задачи. В случае выбора сортировки на странице «Задачи по проектам», этот тип сортировки применяется ко всем таблицам всех проектов.  Тип сортировки указан под верхней панелью навигации справа.
Слева под панелью навигации на странице «Все задачи» есть кнопка «Создать задачу», а на странице «Задачи по проектам» есть кнопка «Создать проект»

**Создание задачи**
Для создания задачи можно:
1. Нажать кнопку «Создать задачу» слева под панелью навигации.
2. Заполнить форму (обязательные поля отмечены *). Можно вернуться назад с помощью соответствующей кнопки над заголовком формы создания.
3. Нажать сохранить
Кроме того, задачу можно создать, нажав кнопку «Добавить задачу» справа от названия проекта в шапке его карточки на странице «Задачи по проектам». Тогда изначально выбран проект задачи.

**Создание проекта**
Чтобы создать проект, нужно на странице «Задачи по проектам» нажать «Создать проект», далее действия аналогичны созданию задачи.

**Информация о задаче**
Информацию о задаче можно открыть при клике на название задачи. Помимо данных, видимых в таблице, показывается описание и дата и время создания задачи.

**Изменение и удаление задач/проектов**
Для задач (в таблице в самом правом столбе "Действия") и для проектов (на странице «Задачи по проектам» в шапке карточки справа от названия) есть кнопки для изменения (жёлтая) и для удаления (красная). При нажатии на изменение, открывается форма, аналогичная созданию.

**О трекере**
В разделе о трекера находится краткая инструкция
</details>

