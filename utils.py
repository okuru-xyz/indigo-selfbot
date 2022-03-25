import os
from colorama import Fore, init

init()

class info:
    name = 'Indigo'
    prefix = '[Indigo]'
    version = 1.4
    logSmallActions = False

class logging:
    def print(message: str) -> str:
        return(
            print(f'{Fore.LIGHTBLUE_EX}{info.prefix} {Fore.RESET}{message}')
        )

    def printError(message: str) -> str:
        return(
            print(f'{Fore.LIGHTBLUE_EX}{info.prefix} {Fore.RED}{message}')
        )
    
    def verbose(message: str) -> str:
        if info.logSmallActions:
            return(print(message))
        else:
            return()
    
class utilities:
    def cls():
        return os.system('cls' if os.name == 'nt' else 'clear')
