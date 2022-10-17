# Script para automatizar a prestação de contas do Empresa Cidadã

import fitz
from os import listdir
from os.path import isfile, join
import pandas as pd
from tabulate import tabulate

def ocr_checker(pdf): #Abre o pdf, checa se ele tem OCR, passa se precisar, e chama a função seguinte.
    pass

def ec_tipo_dct(pdf): #Identifica se o documento é GFIP ou FGTS e chama a função adequada.
    documento = fitz.open(pdf)
    documento_txt = ''
    tipo_documento = 'Não sei que documento é esse.'
    lista_possibilidades = ['RELAÇÃO DOS TRABALHADORES CONSTANTES NO ARQUIVO SEFIP',
    'Extrato de Conta do Fundo de Garantia', 'FGTS - EXTRATO ANALITICO DO TRABALHADOR',
    'Para uso da Caixa:']
    for pagina in documento:
        documento_txt += pagina.get_text()
    if lista_possibilidades[0] in documento_txt:
        return ec_gfip(pdf)
    elif lista_possibilidades[0] not in documento_txt:
        for possibilidade in lista_possibilidades:
            if possibilidade in documento_txt:
                return ec_fgts(pdf)
    else:
        return tipo_documento

def ec_gfip(pdf): #Verifica a competência da GFIP e o número de funcionários no mês.
    gfip = fitz.open(pdf)
    pagina_buscada = ''
    for pagina in gfip:
        if "RELAÇÃO DOS TRABALHADORES" in pagina.get_text() \
                and "RESUMO DO FECHAMENTO - EMPRESA" not in pagina.get_text():
            pagina_buscada += pagina.get_text()
    lista_buscada = pagina_buscada.split('\n')
    funcionários = 0
    for info in lista_buscada:
        if 'COMP' in info:
            competência = info
        if info == '01':
            funcionários +=1
    return f'GFIP: {competência[9:13]}: {competência} / Funcionários: {funcionários}'

def ec_fgts(pdf): # Verifica os depósitos de FGTS
    lista_fgts = []
    lista_anos = ['2020','2021']
    lista_deposito = ['JANEIRO', 'FEVEREIRO', 'MARCO', 'ABRIL', 'MAIO', 'JUNHO',
                          'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']
    fgts = fitz.open(pdf)
    fgts_txt = ''
    for pagina in fgts:
        fgts_txt += pagina.get_text()
    for ano in lista_anos:
        for competência in lista_deposito:
            deposito_barra = f'DEPOSITO {competência}/{ano}'
            deposito_sem_barra = f'DEPOSITO {competência} {ano}'
            atraso_barra = f'DEPOSITO EM ATRASO {competência}/{ano}'
            atraso_sem_barra = f'DEPOSITO EM ATRASO {competência} {ano}'
            if deposito_barra in fgts_txt:
                lista_fgts.append(f'{competência}/{ano}: OK')
            elif deposito_sem_barra in fgts_txt:
                lista_fgts.append(f'{competência}/{ano}: OK')
            elif atraso_barra in fgts_txt:
                lista_fgts.append(f'{competência}/{ano}: OK')
            elif atraso_sem_barra in fgts_txt:
                lista_fgts.append(f'{competência}/{ano}: OK')
            else:
                lista_fgts.append(f'{competência}/{ano}: FALTA')
    #if '' in fgts_txt:

    df_fgts = pd.DataFrame(lista_fgts, columns = ['FGTS'])
    return df_fgts

def ec_pasta(caminho):''' Abre todos os arquivos contidos na pasta do caminho indicado como argumento
                        e escreve no arquivo txt.'''
    arquivos_buscados = [arquivo for arquivo in listdir(caminho)]
    resultados_fgts = pd.DataFrame()
    resultados_gfip = []
    for arquivo in arquivos_buscados:
        resultado = ec_tipo_dct(f'{caminho}/{arquivo}')
        if 'FGTS' in resultado:
            resultados_fgts[arquivo]= resultado
        elif 'GFIP' in resultado:
            resultados_gfip.append(resultado)
    resultados_gfip_ordem = sorted(resultados_gfip)
    with open(r'C:\Users\Vitor\Desktop\Vítor\SMF\EC - Prestação de Contas\resultado.txt', 'a') as arquivo_análise:
        arquivo_análise.write('GFIPs encontradas:\n')
        total_gfips = 0
        for comp in resultados_gfip_ordem:
            arquivo_análise.write(f'{comp}\n')
            total_gfips +=1
        arquivo_análise.write(f'Total de competências encontradas: {total_gfips}\n')
        arquivo_análise.write('\n')
        arquivo_análise.write('FGTS recolhidos:\n')
        arquivo_análise.write(' \n')
        arquivo_análise.write(resultados_fgts.to_markdown())
        arquivo_análise.write('\n')
        arquivo_análise.write('\n')
        arquivo_análise.write('----------Análise concluída ----------\n')

def ec_input_dados(): #Recebe input do usuário sobre o protocolo analisado e chama as demais funções.
    solicitante = input('Solicitante: ')
    CNPJ = input('CNPJ: ')
    protocolo = input('Protocolo: ')
    caminho = input('Caminho: ')
    cabeçalho = f'Solicitante:{solicitante} / CNPJ:{CNPJ} / Protocolo:{protocolo}'
    with open(r'C:\Users\Vitor\Desktop\Vítor\SMF\EC - Prestação de Contas\resultado.txt','a') as arquivo_análise:
        arquivo_análise.write('\n')
        arquivo_análise.write('----------Início da análise----------\n')
        arquivo_análise.write('\n')
        arquivo_análise.write(f'{cabeçalho}')
        arquivo_análise.write(f'\n')
    ec_pasta(caminho)






































