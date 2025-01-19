from datetime import date
from dotenv import load_dotenv
import os


load_dotenv()

def calcular_idade(data_atual, ano_nasc, mes_nasc, dia_nasc):
    contagem_em_dias = data_atual - date(int(ano_nasc),int(mes_nasc),int(dia_nasc))
    print(contagem_em_dias)
    quebra_em_anos = int(contagem_em_dias.days/365)
    dias_anos_bissextos = int(quebra_em_anos/4)
    print(dias_anos_bissextos)
    diferenca = contagem_em_dias.days - dias_anos_bissextos
    print(diferenca)
    idade = int(diferenca/365)
    return idade
