def echo(message: str) -> str:
    return message


def reverse_string(message: str) -> str:
    return message[::-1]


def load_names_from_text_file(filename: str) -> list[str]:
    with open(filename, 'r') as f:
        return f.readlines()
