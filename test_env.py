import os

def main():
    # Substitua 'MY_SECRET' pelo nome da sua variável de ambiente
    secret_value = os.getenv('FIRST_ENV')
    secret_value2 = os.getenv('NEXT_HI_EVERYONE')
    
    if secret_value:
        print(f"O valor da variável MY_SECRET é: {secret_value}")
    else:
        print("A variável MY_SECRET não está definida.")

    if secret_value2:
        print(f"O valor da variável MY_SECRET2 é: {secret_value2}")
    else:
        print("A variável MY_SECRET2 não está definida.")

if __name__ == "__main__":
    main()
