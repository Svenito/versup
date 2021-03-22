from colorama import Fore, Back, Style


def print_ok(message: str):
    print(u"{0}\u2713 {1}{2}\n".format(Fore.GREEN, Fore.RESET, message))


def print_error(message: str):
    print(
        u"{0}{1}\u2717 {2}{3}\n".format(
            Fore.RED, Style.BRIGHT, Style.RESET_ALL, message
        )
    )


def print_warn(message: str):
    print(u"{0}{1}! {2}{3}\n".format(Fore.RED, Style.BRIGHT, Style.RESET_ALL, message))
