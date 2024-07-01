# Base de dados de números - substitua esta lista pelos seus números reais
from test2 import base

def classify_number(num):
    """Classifica o número como cinza ou verde."""
    if 0 <= num <= 1.99:
        return 'cinza'
    elif 2 <= num <= 99999999:
        return 'verde'
    return 'indefinido'

LOSS_COUNT = 0
GREEN_COUNT = 0

def analyze_data(data):
    global LOSS_COUNT
    global GREEN_COUNT

    green_counter = 0  # Contador de "Green"
    
    i = 0
    while i <= len(data) - 36:
        last_16 = data[i:i + 16]  # Últimos 16 Resultados
        last_15 = data[i + 1:i + 16]  # Últimos 15 Resultados
        last_5 = last_16[-5:]  # Últimos 5 Resultados
        last_4 = last_16[-4:]  # Últimos 4 Resultados
        
        # Filtra os números verdes
        greens = [num for num in last_16 if classify_number(num) == 'verde']
        green_percentage = len(greens) / 16

        # Filtra os números cinzas
        grays = [num for num in last_16 if classify_number(num) == 'cinza']
        gray_percentage = len(grays) / 16

        # Filtra os números verdes nos últimos 15 resultados
        last_15_greens = [num for num in last_15 if classify_number(num) == 'verde']
        last_15_green_percentage = len(last_15_greens) / 15

        # Filtra os números cinzas nos últimos 15 resultados
        last_15_grays = [num for num in last_15 if classify_number(num) == 'cinza']
        last_15_gray_percentage = len(last_15_grays) / 15

        # Verifica se a porcentagem de verdes nos últimos 15 resultados é superior a 72% e os últimos 4 resultados são verdes
        if last_15_green_percentage > 0.72 and all(classify_number(num) == 'verde' for num in last_4):
            if green_counter >= 1:
                print("Analisando Entrada (Verde)")

        # Verifica se a porcentagem de verdes nos últimos 16 resultados é superior a 74% e os últimos 5 resultados são verdes    
        if green_percentage > 0.74 and all(classify_number(num) == 'verde' for num in last_5):
            if green_counter >= 1:
                print("Entrada Autorizada (Verde)")

            # Verifica os próximos 20 números
            next_20 = data[i + 16:i + 36]
            for num in next_20:
                if num > 30: # Em Busca de um 30x+
                    if green_counter >= 1:
                        GREEN_COUNT += 1
                        print(f"Green: {num}")
                        # i += 13 # Apos Mach do Resultado do bloco de 16, pular 13 do indice para testar somente os proximos 16 após esses 13 e não seguidos para evitar greens falsos repetidos e loss falsos repetidos
                    green_counter += 1
                    if green_counter == 1:
                        print("FIQUE ATENTO(A) AO JOGO")
                    break
            else:
                if green_counter >= 1:
                    LOSS_COUNT += 1
                    print("Loss")
                    # i += 13 # Apos Mach do Resultado do bloco de 16, pular 13 do indice para testar somente os proximos 16 após esses 13 e não seguidos para evitar greens falsos repetidos e loss falsos repetidos
                    green_counter = 0
            i = i + 35

        # Verifica se a porcentagem de cinzas nos últimos 15 resultados é superior a 72% e os últimos 4 resultados são cinzas
        if last_15_gray_percentage > 0.72 and all(classify_number(num) == 'cinza' for num in last_4):
            if green_counter >= 1:
                print("Analisando Entrada (Cinza)")
                
        # Verifica se a porcentagem de cinzas nos últimos 16 resultados é superior a 74% e os últimos 5 resultados são cinzas    
        if gray_percentage > 0.74 and all(classify_number(num) == 'cinza' for num in last_5):
            if green_counter >= 1:
                print("Entrada Autorizada (Cinza)")

            # Verifica os próximos 20 números
            next_20 = data[i + 16:i + 36]
            for num in next_20:
                if num > 30:  # Em Busca de um 30x+
                    if green_counter >= 1:
                        GREEN_COUNT += 1
                        print(f"Green: {num}") # print(f"Green: {num}")  # print("Green !!!!")
                        # i += 13 # Apos Mach do Resultado do bloco de 16, pular 13 do indice para testar somente os proximos 16 após esses 13 e não seguidos para evitar greens falsos repetidos e loss falsos repetidos
                    green_counter += 1
                    if green_counter == 1:
                        print("FIQUE ATENTO(A) AO JOGO")
                    break
            else:
                if green_counter >= 1:
                    print("Loss")
                    LOSS_COUNT += 1
                    # i += 13 # Apos Mach do Resultado do bloco de 16, pular 13 do indice para testar somente os proximos 16 após esses 13 e não seguidos para evitar greens falsos repetidos e loss falsos repetidos
                    green_counter = 0
            i = i + 35
        i += 1

# Chama a função para analisar os dados
analyze_data(base)


print('LOSS: ', LOSS_COUNT)
print('GREEN: ', GREEN_COUNT)
# print(LOSS_COUNT, GREEN_COUNT)