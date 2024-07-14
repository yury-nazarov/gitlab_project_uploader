# Gitlab Project Uploader

## About 
Утилита для переноса части репозиториев в другой gitlab `GL_SERVER`.

## Prepare and installation
0. Переместить все необходимые репозитори, которые нужно загрузить в одну группу (`GL_GROUP_PATH`, `GL_GROUP_ID`) в gitlab в локальный каталог `FS_LOCAL_PATH`
1. `git pull git@github.com:yury-nazarov/gitlab_project_uploader.git`
2. `cd gitlab_project_uploader/`
3. `mv config/.demo-env config/.env`  
4. Поправить переменные в `.env` в зависимости от ваших credential, см следующий раздел
5. `python3 -m venv venv`
6. `source venv/bin/activate`
7. `pip install -r requirements.txt`
8. `chmod +x src/*`
9. `./src/main.py`
10. enjoy


## Переменные окружения

| VAR               | Example                   |  Description                                          |
| -------------     | -------------             |-------------                                          |
| LOG_LEVEL         | "DEBUG"                   | Уровень логирования: DEBUG, INFO, WARNING             |
| FS_LOCAL_PATH     | "/Users/admin/move_repos/"| Адрес локального каталога с git проектами от корня FS |
| GL_SERVER         | "gitlab.com"              | FQDN Gitlab сервера                                   |
| GL_PRIVATE_TOKEN  | "XXXXYYYYZZZZHHHHWWW123"  | [Gitlab Personal Access Token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) |
| GL_GROUP_PATH     | "ansible-galaxy/proxies"  | Путь в gitlab webui до группы с проектами
| GL_GROUP_ID       | "123"                     | ID группы, которая доступна по https://GL_SERVER/GL_GROUP_PATH. Посмотрет можно в настройках Группа -> General -> Group ID