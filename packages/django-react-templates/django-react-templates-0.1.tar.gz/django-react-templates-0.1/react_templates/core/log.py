from termcolor import colored


def log(msg: str):
    title = colored("Reactive: ", "blue", attrs=["bold"])
    print(title + msg)
