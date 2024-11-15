from src.controller.consulting import download_total, download_incremental
import time

def main():
    while True:
        escolha = input('''
    Escolha uma das opções:
    1 - Download inicial
    2 - Download incremental (Somente hoje)
    Q - Sair
    >>> ''')
        if escolha == '1':
            download_total()
            print()
        elif escolha == '2':
            download_incremental()
        elif escolha.upper() == 'Q':
            exit()
        else:
            time.sleep(1)
            print('\nOpção inválida. Tente novamente.')
            time.sleep(1)

main()