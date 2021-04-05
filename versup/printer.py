from colorama import Fore, Style


def print_ok(message: str):
    print(f"{Fore.GREEN}\u2713 {Fore.RESET}{message}\n")


def print_error(message: str):
    print(f"{Fore.RED}{Style.BRIGHT}\u2717 {Style.RESET_ALL}{message}\n")


def print_warn(message: str):
    print(f"{Fore.RED}{Style.BRIGHT}! {Style.RESET_ALL}{message}\n")
