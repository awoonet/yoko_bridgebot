import yaml


def load_i18n():
    i18n = {}
    with open("i18n/ru.yml") as file:
        i18n = yaml.load(file, Loader=yaml.Loader)

    def t(command: str, *args) -> str:
        command = command.split(".")

        response = i18n
        for i in command:
            response = response[i]

        return response.format(*args)

    return t
