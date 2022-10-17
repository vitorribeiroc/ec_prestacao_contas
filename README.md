# Empresa Cidadã - Automatização da tomada de contas
INTRODUÇÃO

Este projeto tem como objetivo desenvolver automatização para análise preliminar dos documentos (extratos de FGTS e GFIP) enviados pelas empresas obrigadas à prestação de contas no âmbito do programa Empresa Cidadã, do município de Niterói - RJ.

DESCRIÇÃO

O programa Empresa Cidadã foi instituído pela prefeitura de Niterói como medida de enfrentamento à pandemia da COVID-19. Foi iniciado em Abril de 2020 e, após duas prorrogações, encerrado em Novembro de 2021. 

No âmbito do programa, as empresas poderiam cadastrar um determinado número de funcionários e receberiam um valor especificado para auxílio no custeio ao pagamento dos salários. Em troca, comprometiam-se, ao longo da participação no programa, a não reduzir o número de postos de trabalho apresentado no mês de adesão.

Na prestação de contas (realizada em plataforma própria), as empresas enviam, em regra, dois tipos de documentos: a GFIP, que indica o número de trabalhadores, e o FGTS, que evidencia recolhimento do Fundo de Garantia. Outros documentos podem também constar, como o relatório de suspensões de contrato de trabalho ou de redução de jornada de trabalho. 

O escopo deste projeto engloba a análise de GFIP e FGTS. Na GFIP, deve ser verificado o número de trabalhadores. No FGTS, os recolhimentos mensais.

TAREFAS

1 - Análise das GFIP:

A empresa envia uma GFIP por competência, ou seja, uma para 01/2020, uma para 02/2020, etc, até 11/2021. O máximo será, portanto, de 20 GFIPs.

Em cada uma delas, consta a lista de trabalhadores por categoria. O objetivo é verificar a quantidade de trabalhadores categoria 01 (CAT 01 na GFIP).

1.1 - Questões a considerar:

- Os pdfs enviados possuem várias páginas e, apesar de se repetirem, não seguem um padrão homogêneo. Há arquivos com 2 folhas, outros com 6, 9, etc. Além disso, a lista buscada não estará sempre na mesma página. No código, a solução encontrada foi buscar texto específico da página buscada, que se repete independente da ordem ou quantidade de páginas no documento ("RELAÇÃO DOS TRABALHADORES"). Esse texto, todavia, consta também em outra página, então foi necessário aliar a ele um excludente ("RESUMO DO FECHAMENTO - EMPRESA") a fim de garantir tratar-se da página correta.

2 - Análise do FGTS:


ESTRUTURA DO CÓDIGO

PROBLEMAS A SOLUCIONAR

- PROBLEMAS GFIP
- PROBLEMAS FGTS
- PROBLEMAS GERAIS

SUGESTÕES DE MELHORIA
