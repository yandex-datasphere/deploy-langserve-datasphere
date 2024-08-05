# Внимание!

> Данный репозиторий устарел, текущая версия: https://github.com/all-mute/deploy-langserve-datashpere-2.0

# Деплой LangServe в Yandex DataSphere

В данном примере мы будем использовать 🦜️🏓[Langserve](https://github.com/langchain-ai/langserve?ref=blog.langchain.dev) для деплоя цепочек LangChain как REST API. Для развертывания Docker-образа будет использоваться ML-платформа [Yandex DataSphere](https://cloud.yandex.ru/ru/services/datasphere).

## Подготовительные работы

1. Если вы ранее не работали в DataSphere, то рекомендуем начать с создания сообщества и проекта, в котором будет развернут код LangServe. Как это сделать описано [здесь](https://cloud.yandex.ru/ru/docs/datasphere/tutorials/basics).
2. Настройте проект в DataSphere для развертывания веб-сервиса как описано в пункте 1 в [документации](https://cloud.yandex.ru/ru/docs/datasphere/tutorials/node-from-docker).

## Пошаговая инструкция

### Локально соберите Docker-образ и добавьте его в Container Registry

1. Склонируйте данный репозиторий, откройте терминал на локальном компьютере и перейдите в нем в папку с файлами данного репозитория.
2. Соберите Docker-образ с помощью `docker build --platform linux/amd64 -t langserve-demo`. При сборке обязательно нужно указать параметр `--platform`, чтобы образ корректно запустился в DataSphere.
3. Если у вас не установлен интерфейс командной строки Yandex Cloud, то выполните шаги в этой [инструкции](https://cloud.yandex.ru/ru/docs/cli/quickstart#install).
4. Задайте каталог, в котором вы будете развертывать сервис, каталогом по умолчанию: `yc config set folder-name <название_каталога>`.
5. Получите IAM-токен для своего пользовательского аккаунта: `yc iam create-token`.
6. Выполните команду, подставив вместо <IAM-токен> значение токена с предыдущего шага:
```
docker login \
--username iam \
--password <IAM-токен> \
cr.yandex
```
7. Загрузите Docker-образ в Container Registry:

`docker tag langserve-demo cr.yandex/<идентификатор_реестра>/langserve-demo:latest`

`docker push cr.yandex/<идентификатор_реестра>/langserve-demo:latest`

При необходимости можно использовать Docker Hub или другое registry для хранения образа.
8. Создайте авторизованный ключ для сервисного аккаунта и сохраните его в файл `json.key` как описано в [документации](https://cloud.yandex.ru/ru/docs/cli/operations/authentication/service-account) (шаги 1-2).

### В DataSphere создайте ноду из Docker-образа в Сontainer Registry

10. В проекте DataSphere создайте секрет, хранящий все содержимое файла (json) с авторизованным ключом для сервисного аккаунта.
11. В проекте DataSphere создайте [новый ресурс "Нода" из Docker-образа](https://cloud.yandex.ru/ru/docs/datasphere/operations/deploy/node-create). При создании укажите следующие параметры:
```
Имя: <имя_ноды>
Тип: Docker-образ
Путь к образу: cr.yandex/<id_container_registry>/langserve-demo
Дополнительные параметры:
    Имя пользователя: json_key
    Секрет с паролем: укажите секрет, созданный выше
Порт: 8000
Таймаут: 180 секунд
```
12. Для тестирования развернутой ноды сделайте запрос: 
```
curl -H "x-node-id: <id_ноды>" -H "Authorization: Bearer <IAM_TOKEN>" -H "x-folder-id: <id_каталога>" -X POST -d '{
    "input": "Привет. Как дела?"
}' https://node-api.datasphere.yandexcloud.net/invoke
```
13. Для балансировки нагрузки между нодами и обновления развернутых сервисов во время работы создайте [алиас](https://cloud.yandex.ru/ru/docs/datasphere/operations/deploy/alias-create).
