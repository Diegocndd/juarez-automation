import os

def main():
    # Substitua 'MY_SECRET' pelo nome da sua variável de ambiente
    secret_value = os.getenv('FIRST_ENV')
    
    if secret_value:
        print(f"O valor da variável MY_SECRET é: {secret_value}")
    else:
        print("A variável MY_SECRET não está definida.")

if __name__ == "__main__":
    main()
