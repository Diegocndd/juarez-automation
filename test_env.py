import os

def main():
    # Substitua 'MY_SECRET' pelo nome da sua variável de ambiente
    SECRET1 = os.getenv('SECRET1')
    print(SECRET1)
    if SECRET1:
        print(f"O valor da variável MY_SECRET é: {SECRET1}")
    else:
        print("A variável MY_SECRET não está definida.")

if __name__ == "__main__":
    main()
