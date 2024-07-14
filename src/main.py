from gitlab_project_uploader import GitlabProjectUploader


def main():
    c = GitlabProjectUploader("../config/.env")
    c.run()


if __name__ == '__main__':
    main()

