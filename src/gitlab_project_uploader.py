import os
import sys
import shutil

import git
import requests
from loguru import logger
import config


class GitlabProjectUploader:
    """
    Массово загружает проекты в Gitlab, подготавливая все необходимое
    """

    def __init__(self, dotenv_path: str):
        log_level = self.__init_config(dotenv_path)
        self.logger = self.__init_logger(log_level)

        logger.info("object created")

    def __init_logger(self, log_level="DEBUG"):
        """
        Инициируем логер

        :param log_level: Уровень логирования
        :return: None
        """
        logger.remove(0)
        logger.add(sys.stdout, level=log_level)
        logger.info("logger initiated")
        return logger

    def __init_config(self, env_path: str):
        """
        Инициирует конфиг приложения

        :param env_path: путь до файла .env
        :return: None
        """
        # Инициируем переменные из конфигурационного файла
        log_level = config.LOG_LEVEL
        local_path = config.FS_LOCAL_PATH
        gitlab_server = config.GL_SERVER
        gitlab_private_token = config.GL_PRIVATE_TOKEN
        gitlab_group_path = config.GL_GROUP_PATH
        gitlab_group_id = config.GL_GROUP_ID

        # Создаем конфигруационные объекты на уровне всего класса
        self.repository = "origin"
        self.local_path = local_path
        self.gitlab_private_token = gitlab_private_token
        self.gitlab_api = f"https://{gitlab_server}/api/v4/projects/"
        self.gitlab_group_path = f"git@{gitlab_server}:{gitlab_group_path}"
        self.gitlab_namespace_id = gitlab_group_id

        print("log_level", log_level)
        print("log_level", log_level)

        return log_level

    def run(self):
        """
        Запускает методы в нужном порядке

        :return:
        """
        func = [self.git_init, self.git_add, self.create_gitlab_repo,
                self.git_commit, self.git_remote_add, self.git_push, self.git_push_tag]
        for item in func:
            self.make_it(item)

    def make_it(self, operation):
        """
        В цикле проходит по всем вложеным каталогам
        """
        for dir_name in sorted(os.listdir(self.local_path)):
            dir_path = f"{self.local_path}/{dir_name}"

            self.logger.debug(f"Выполняется: {operation.__name__} в каталоге: {dir_path}")

            # Удляем придыдущие коммиты после инициируем заново git init
            if operation.__name__ == "git_init":
                if os.path.isdir(f"{dir_path}/.git"):
                    self.remote_git_folder(dir_path)
                operation(dir_name)

            # Создаем проект в gitlab
            elif operation.__name__ == "create_gitlab_repo":
                self.create_gitlab_repo(dir_name)

            # Все остальные методы по заполнению проекта на gitlab
            else:
                repo = git.Repo(dir_path)
                operation(dir_name, repo)

    def git_init(self, dir_name: str):
        """
        Инициируем git репозиторий

        :param dir_name: название директории с проектом
        :return:
        """
        repo = git.Repo.init(f"{self.local_path}/{dir_name}")
        self.logger.debug(f"{dir_name} | git init")

        return repo

    def git_add(self, dir_name: str, repo):
        """
        Добавляет в файлы в индекс: git add .

        :param dir_name: название каталога с проектом
        :param repo: ссылка на объект представляющий .git в текущем каталоге
        :return: None
        """
        repo.git.add(all=True)
        self.logger.debug(f"{dir_name} | git add .")

    def git_commit(self, dir_name: str, repo):
        """
        git commit

        :param dir_name: название каталога с проектом
        :param repo: ссылка на объект представляющий .git в текущем каталоге
        :return: None
        """
        try:
            repo.git.commit('-m', 'init')
            self.logger.debug(f"{dir_name} | git commit -m 'init'")
        except Exception as e:
            self.logger.error(f"can't git commit -m 'init'")
            self.logger.debug(e)

    def git_remote_add(self, dir_name: str, repo):
        """
        Добавляет удаленный репозиторий: git remote add origin https://gitlab.com/path/to/prj.git

        :param dir_name: название каталога с проектом
        :param repo: ссылка на объект представляющий .git в текущем каталоге
        :return: None
        """
        gitlab = f"{self.gitlab_group_path}/{dir_name}.git"

        try:
            repo.create_remote(self.repository, gitlab)
            self.logger.debug(f"{dir_name} | git remote add {self.repository} {gitlab}")
        except Exception as e:
            self.logger.error(f"{dir_name} | can't git remote add {self.repository} {gitlab}")
            self.logger.debug(e)

    def git_push(self, dir_name: str, repo):
        """
        git push origin --set-upstream main

        :param dir_name: название каталога с проектом
        :param repo: ссылка на объект представляющий .git в текущем каталоге
        :return: None
        """

        # пушим
        try:
            repo.remotes.origin.push(refspec='main:main')
            self.logger.debug(f"{dir_name} | git push {self.repository} -b main")
        except Exception as e:
            self.logger.error(f"{dir_name} | can't git push {self.repository} -b main")
            self.logger.debug(e)

    def git_push_tag(self, dir_name: str, repo):
        """
        Создает и добавляем тег к коммиту:
            git tag 1.0.0
            git push origin 1.0.0

        Т.к. скрипт предназначен для первоначальной загрузки множества репозиториев,
        тег захардкожен, как точка счисления.

        :param dir_name: название каталога с проектом
        :param repo: ссылка на объект представляющий .git в текущем каталоге
        :return: None
        """
        TAG_NAME = "1.0.0"

        try:
            repo.create_tag(TAG_NAME)
            repo.remotes.origin.push(TAG_NAME)
            self.logger.debug(f"{dir_name} | git push {self.repository} {TAG_NAME}")
        except Exception as e:
            self.logger.error(f"{dir_name} | can't git push {self.repository} {TAG_NAME}")
            self.logger.debug(e)

    def remote_git_folder(self, dir_path:str):
        """
        Удаляет директорию .git

        :param dir_path: название каталога с проектом
        :return:
        """
        git_dir_path = f"{dir_path}/.git"
        if os.path.isdir(git_dir_path):
            shutil.rmtree(git_dir_path, ignore_errors=True)
            self.logger.info(f"Удалили: {git_dir_path}")

    def create_gitlab_repo(self, dir_name:str):
        """
        Создает репозиторий в Gitlab

        curl    --request POST
                --header "PRIVATE-TOKEN: gitlab_api_token"                \
                --header "Content-Type: application/json"                           \
                --data '{                                                           \
                    "name": "demo_api",                                             \
                    "description": "",                                              \
                    "path": "demoapi",                                              \
                    "namespace_id": "123",                                          \
                    "initialize_with_readme": "false"                               \
                    }'                                                              \
                --url "https://gitlab.com/api/v4/projects/"

        :param dir_name: название каталога с проектом
        :return: None
        """

        r = requests.post(self.gitlab_api,
                          headers={
                              'PRIVATE-TOKEN': self.gitlab_private_token,
                          },
                          data={"name": dir_name,
                                "path": dir_name,
                                "namespace_id": self.gitlab_namespace_id,
                                "initialize_with_readme": "false",
                                })
        if r.status_code == 201:
            self.logger.info(f"{dir_name} | проект создан")
        else:
            self.logger.error(f"{dir_name} | что то пошло не так. Gitlab API Status Code: {r.status_code}")