# Empresa Cidadã - Automatização da tomada de contas
## INTRODUÇÃO

Este projeto tem como objetivo desenvolver automatização para análise preliminar dos documentos (extratos de FGTS e GFIP) enviados pelas empresas obrigadas à prestação de contas no âmbito do programa Empresa Cidadã, do município de Niterói - RJ.

## DESCRIÇÃO

O programa Empresa Cidadã foi instituído pela prefeitura de Niterói como medida de enfrentamento à pandemia da COVID-19. Foi iniciado em Abril de 2020 e, após duas prorrogações, encerrado em Novembro de 2021. 

No âmbito do programa, as empresas poderiam cadastrar um determinado número de funcionários e receberiam um valor especificado para auxílio no custeio ao pagamento dos salários. Em troca, comprometiam-se, ao longo da participação no programa, a não reduzir o número de postos de trabalho apresentado no mês de adesão.

Na prestação de contas (realizada em plataforma própria), as empresas enviam, em regra, dois tipos de documentos: a GFIP, que indica o número de trabalhadores, e o FGTS, que evidencia recolhimento do Fundo de Garantia. Outros documentos podem também constar, como o relatório de suspensões de contrato de trabalho ou de redução de jornada de trabalho. 

O escopo deste projeto engloba a análise de GFIP e FGTS. Na GFIP, deve ser verificado o número de trabalhadores. No FGTS, os recolhimentos mensais.

## TAREFAS

### 1 - Análise das GFIP (ec_gfip(pdf)):

A empresa envia uma GFIP por competência, ou seja, uma para 01/2020, uma para 02/2020, etc, até 11/2021. O máximo será, portanto, de 20 GFIPs.

Em cada uma delas, consta a lista de trabalhadores por categoria. O objetivo é verificar a quantidade de trabalhadores categoria 01 (CAT 01 na GFIP).

#### 1.1 - Questões a considerar:

- Os pdfs enviados possuem várias páginas e, apesar de se repetirem, não seguem um padrão homogêneo. Há arquivos com 2 folhas, outros com 6, 9, etc. Além disso, a lista buscada não estará sempre na mesma página. No código, a solução encontrada foi buscar texto específico da página buscada, que se repete independente da ordem ou quantidade de páginas no documento ("RELAÇÃO DOS TRABALHADORES"). Esse texto, todavia, consta também em outra página, então foi necessário aliar a ele um excludente ("RESUMO DO FECHAMENTO - EMPRESA") a fim de garantir tratar-se da página correta.

### 2 - Análise do FGTS (ec_fgts(pdf)):

A empresa envia um FGTS para cada trabalhador cadastro no programa, limitada ao máximo de 9 funcionários (e, consequentemente, 9 documentos).

O documento, ao menos no modelo mais enviado, o EXTRATO ANALÍTICO DO TRABALHADOR (EAT), lista os meses em que houve recolhimento do FGTS (os meses nos quais não houve recolhimento não aparecem na lista).

#### 2.1 - Questões a considerar:

- Ainda que a maioria das empresas envie o EAT, há diversos outros modelos, o que dificulta a identificação pelo sistema de que aquele documento é um FGTS. No código, optou-se por criar uma lista que congrega textos específicos encontrados no modelo: ['Extrato de Conta do Fundo de Garantia', 'FGTS - EXTRATO ANALITICO DO TRABALHADOR', 'Para uso da Caixa:']. Conforme novos modelos forem aparecendo, a ideia é incluir na lista as novas possibilidades.
- Identificado o documento como FGTS, surge outra questão: os modelos variam muito entre si: alguns vêm como 'COMPETÊNCIA/2020', outros 'COMPETÊNCIA 2020', '115-COMPETÊNCIA/ 2020'. Então, encontrar as competências em cada um gera uma proliferação de ifs, elifs e elses. Possível que isso seja resolvido com o uso de REGEX.
- Há um modelo próprio de documento que não exibe nenhum recolhimento, mas sim as competências em atraso. Nesse caso, as demais podem ser consideradas recolhidas. Quando não há competências em atraso, o documento exibe um texto próprio, tipo 'não há recolhimentos em atraso'. A função que analisa os FGTS também precisa comportar essa possibilidade.


### 3 - Definir o tipo de documento (ec_tipo_dct(pdf)):
Aqui, o sistema lê o pdf e busca por uma string específica no texto para, a partir dela, definir se é um FGTS ou uma GFIP.
Após a verificação, ele chama a função adequada (ec_fgts(pdf) ou ec_gfip(pdf)).
Caso não seja possível identificar o tipo de documento, ele retorna a string "Não sei que documento é esse".

### 4 - Abrir todos os arquivos da pasta e escrever o arquivo .txt com o resumo:

## ESTRUTURA DO CÓDIGO

## PROBLEMAS A SOLUCIONAR

- PROBLEMAS GFIP
- PROBLEMAS FGTS
- PROBLEMAS GERAIS

## SUGESTÕES DE MELHORIA
