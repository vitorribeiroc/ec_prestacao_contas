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

- Os pdfs enviados possuem várias páginas e, apesar de se repetirem, não seguem um padrão. Há arquivos com 2 folhas, outros com 6, 9, etc. Além disso, a lista buscada não estará sempre na mesma página. No código, a solução encontrada foi buscar texto específico da página buscada, que se repete independente da ordem ou quantidade de páginas no documento ("RELAÇÃO DOS TRABALHADORES"). Esse texto, todavia, consta também em outra página, então foi necessário aliar a ele um excludente ("RESUMO DO FECHAMENTO - EMPRESA") a fim de garantir tratar-se da página correta.

### 2 - Análise do FGTS (ec_fgts(pdf)):

A empresa envia um FGTS para cada trabalhador cadastrado no programa, limitada ao máximo de 9 funcionários (e, consequentemente, 9 documentos).

O documento, ao menos no modelo mais enviado, o EXTRATO ANALÍTICO DO TRABALHADOR (EAT), lista os meses em que houve recolhimento do FGTS (os meses nos quais não houve recolhimento não aparecem na lista).

#### 2.1 - Questões a considerar:

- Ainda que a maioria das empresas envie o EAT, há diversos outros modelos, o que dificulta a identificação pelo sistema de que aquele documento é um FGTS. No código, optou-se por criar uma lista que congrega textos específicos encontrados no modelo: ['Extrato de Conta do Fundo de Garantia', 'FGTS - EXTRATO ANALITICO DO TRABALHADOR', 'Para uso da Caixa:']. Conforme novos modelos forem aparecendo, a ideia é incluir na lista as novas possibilidades.
- Identificado o documento como FGTS, surge outra questão: os modelos variam muito entre si: alguns vêm como 'COMPETÊNCIA/2020', outros 'COMPETÊNCIA 2020', '115-COMPETÊNCIA/ 2020'. Então, encontrar as competências em cada um gera uma proliferação de ifs, elifs e elses. Possível que isso seja resolvido com o uso de REGEX.
- Há um modelo próprio de documento que não exibe nenhum recolhimento, mas sim as competências em atraso. Nesse caso, as demais podem ser consideradas recolhidas. Quando não há competências em atraso, o documento exibe um texto próprio, tipo 'não há recolhimentos em atraso'. A função que analisa os FGTS também precisa comportar essa possibilidade.


### 3 - Definir o tipo de documento (ec_tipo_dct(pdf)):
Aqui, o sistema lê o pdf e busca por uma string específica no texto para, a partir dela, definir se é um FGTS ou uma GFIP.

Após a verificação, ele chama a função adequada, ec_fgts(pdf) ou ec_gfip(pdf).

Caso não seja possível identificar o tipo de documento, ele retorna a string "Não sei que documento é esse".

### 4 - Abrir todos os arquivos da pasta e escrever o arquivo .txt com o resumo (ec_pasta(caminho)):
Essa função abre, um por um, todos os arquivos da pasta indicada em 'caminho', e chama a função acima, ec_tipo_dct(pdf), com cada um deles como argumento.

Os resultados obtidos são escritos em um documento .txt, que será o 'produto final' do sistema.

#### 4.1 - Questões a considerar:
A forma utilizada para manipular os resultados é diferente por tipo de documento.

Toda GFIP vai trazer um único resultado: uma string do tipo "GFIP: 2021: COMP: 01/2021 / Funcionários: 1". Haverá sempre múltiplas GFIPs. 
Assim, optou-se por salvar o resultado de cada um em uma lista e, com um for loop, escrever resultado por resultado no documento .txt.

Já para os FGTSs, a situação é diferente. Pode haver de 1 a 9 FGTS, e cada um deles trará vários resultados, strings como 'JANEIRO/2020: OK', 'FEVEREIRO/2020: OK', etc.
Aqui, a solução foi criar um DataFrame, com o nome do arquivo como coluna, os resultados como linhas, e, por fim, escrever esse DataFrame no documento .txt.
Há ainda o caso limite do FGTS com resultado único "não há recolhimentos em atraso". No momento, o sistema não traz solução para a questão.

### 5 - Informar os dados iniciais (ec_input_dados()):
Essa função é a inicial e, em teoria, a única com que o usuário sem conhecimentos em programação deverá lidar.

Ela solicita input do usuário para os dados básicos da análise (Nome/CNPJ/Protocolo) e os escreve como cabeçalho no mesmo documento .txt usado pela função acima, ec_pasta(caminho).
Pede também input do caminho e, com ele, chama ec_pasta(caminho), que é quem, de fato, dispara a análise toda.

## ESTRUTURA DO CÓDIGO E CONSIDERAÇÕES
A estrutura lógica segue descrita no fluxograma abaixo:

![ec_flowchart](https://user-images.githubusercontent.com/97795826/196517370-4e61a23a-4759-4d23-acda-11194f42d8aa.jpg)

Como mencionado, a maior parte dos usuários do sistema será de não programadores. É fundamental, portanto, que ele seja o mais acessível possível, e solicite deles o mínimo de participação.

Os documentos são disponibilizados em um site próprio (com o qual não se pretende realizar integração). Dele, um zip é baixado, e os arquivos, salvos em uma pasta (a variável 'caminho' no input solicitado em ec_input_dados()).

O arquivo .txt é previamente criado. Para fins de centralização, e também de forma a facilitar aos usuários, a ideia é que todas as análises constem no mesmo arquivo, daí ter se usado o .write com append.

Na análise dos documentos, foi usada o módulo Fitz, da bibloteca PyMuPDF, para converter os pdfs em strings, uma em cada linha.

## PROBLEMAS A SOLUCIONAR

- O problema primordial é que, com o FITZ, ele faz uma varredura do pdf que não parece ideal. Não há qualquer vinculação, por exemplo, da entrada 'NOME:' e o 'NOMEDOFUNCIONÁRIO', que vem logo ao lado. Fica tudo bem solta e, em alguns casos, quase inviabiliza as buscas. Não sei se isso é culpa do pdf ou do módulo. Será possível, com o FITZ, 'ler' o pdf de outra forma? Ou o melhor seria descartá-lo e começar do zero com outra biblioteca/módulo de varredura?
- Outro problema relevante é que alguns documentos, apesar de no formato .pdf, são, na verdade, imagens. O FITZ não consegue ler nada neles. No código, há uma função, ocr_checker(pdf), cujo intuito seria de verificar se o documento é selecionável ou não e, em caso negativo, fazer o OCR dele. Encontrei algumas possíveis soluções de como fazer isso, mas a maioria demandando instalação de aplicativos externos, o que complicaria no caso de usuários sem experiência. Há alguma forma 'simples' de fazer isso?
- Há casos em que a GFIP dobra as entradas de 'CAT 01' para determinados funcionários (por exemplo, quando ele sai ou volta de licença-médica). Como a função soma cada '01' encontrado na página selecionada, a conta sai errada. Como evitar que isso aconteça?
- Ainda na GFIP, utilizei "return f'GFIP: {competência[9:13]}: {competência} / Funcionários: {funcionários}'" para ordenar o resultado a partir do ano da competência, o que facilita a visualização no documento final. O ano seria o slice competência[9:13]. O problema é que isso só se sustenta quando o pdf vem com a orientação de paisagem. Se estiver como retrato, os indexes mudam, e ele não encontra mais o ano. O que poderia ser feito?
- Em alguns casos, a empresa enviou um único arquivo de FGTS para todos os funcionários. Como separar funcionário por funcionário, e aí então realizar a análise?
- Como mencionado, o DataFrame que congrega os resultados de ec_fgts(pdf) usa como coluna o nome dos arquivos. Isso, para os usuários, é bem pouco intuitivo. O mais adequado seria que as colunas fossem o nome do funcionário analisado. De que forma pegar esse nome no pdf (o que, provavelmente, também solucionaria o problema anterior)?

## SUGESTÕES DE MELHORIA
Esse é o primeiro projeto que desenvolvo, então tenho total consciência que ele não está nada "pythonico". 

Por isso mesmo, aceito qualquer sugestão de melhoria, seja em questão de eficiência, repetição (tem if, elif, else, for, etc pra cacete e gostaria MUITO de me livrar deles), estrutura lógica, legibilidade ou o que for.

Também gostaria muito de ajuda quanto à possibilidade de deixá-lo mais orientado a objetos.

Enfim, a ajuda que vier, aceito feliz!
