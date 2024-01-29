В данном примере мы будем использовать Langserve (https://github.com/langchain-ai/langserve?ref=blog.langchain.dev) для деплоя цепочек LangChain как REST API. Для развертывания Docker-образа будет использоваться ML-платформа Yandex DataSphere.

1. Настройте проект в DataSphere для развертывания веб-сервиса как описано в пункте 1: https://cloud.yandex.ru/ru/docs/datasphere/tutorials/node-from-docker. 
2. Соберите Docker-образ с помощью docker build --platform linux/amd64 -t langserve-demo. При сборке обязательно нужно указать параметр --platform, чтобы образ корректно запустился в DataSphere. 
3. Задайте каталог, в котором вы будете развертывать сервис, каталогом по умолчанию: yc config set folder-name <название_каталога>.
4. Получите IAM-токен для своего пользовательского аккаунта: yc iam create-token
5. Выполните команду, подставив вместо <IAM-токен> значение токена с предыдущего шага: docker login \
  --username iam \
  --password <IAM-токен> \
  cr.yandex
6. Загрузите Docker-образ в Container Registry:
docker tag langserve-demo cr.yandex/<идентификатор_реестра>/langserve-demo:latest
docker push cr.yandex/<идентификатор_реестра>/langserve-demo:latest
При необходимости можно использовать Docker Hub или другое registry для хранения образа.
7. Создайте авторизованный ключ для сервисного аккаунта и сохраните его в файл json.key. Инструкция: https://cloud.yandex.ru/ru/docs/cli/operations/authentication/service-account (шаги 1-2).
8. В проекте DataSphere создайте секрет, хранящий все содержимое файла (json) с авторизованным ключом для сервисного аккаунта.
9. В проекте DataSphere создайте новый ресурс "Нода". При создании укажите следующие параметры:
Имя
Тип: Docker-образ
Путь к образу: cr.yandex/<id_container_registry>/langserve-demo
Дополнительные параметры:
Имя пользователя: json_key
Секрет с паролем: укажите секрет, созданный выше
Порт: 8000
Таймаут: 180 секунд
10. Для тестирования развернутой ноды сделайте запрос: 
curl -H "x-node-id: <id_ноды>" -H "Authorization: Bearer <IAM_TOKEN>" -H "x-folder-id: <id_каталога>" -X POST -d '{
    "input": "Привет. Как дела?"
}' https://node-api.datasphere.yandexcloud.net/invoke