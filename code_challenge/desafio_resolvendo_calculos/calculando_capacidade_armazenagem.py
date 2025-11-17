"""
Desafio

Você foi contratado para desenvolver um sistema que determine a quantidade de paletes necessária para armazenar a produção diária de caixas.
Cada palete possui uma capacidade fixa de caixas, e o objetivo é calcular o número total de paletes requeridos para acomodar toda a produção do dia.
"""

import math

# Leitura das entradas como strings
total_caixas = input().strip()
capacidade_palete = input().strip()

# Conversão para inteiros
total_caixas = int(total_caixas)
capacidade_palete = int(capacidade_palete)

# Calcula o número de paletes necessários (arredondando para cima)
paletes_necessarios = math.ceil(total_caixas / capacidade_palete)

# Impressão como string (sem espaços ou caracteres especiais)
print(str(paletes_necessarios))
