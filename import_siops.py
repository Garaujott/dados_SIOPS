import os
import pandas as pd


def gerar_caminho_despesas_xlsx(periodo_anos, nomes_categorias, nomes_arquivos):
    caminho_import_despesas = []
    for periodo in range(len(periodo_anos)):
        for categoria in range(len(nomes_categorias)):
            for arquivo in range(len(nomes_arquivos)):
                caminho_import_despesas.append('\\data\\' + periodo_anos[periodo] +
                                               '\\Despesa\\' + nomes_categorias[categoria] +
                                               '\\' + nomes_arquivos[arquivo] + '.xlsx')
    return caminho_import_despesas


def gerar_caminho_despesas_csv(periodo_anos, nomes_categorias, nomes_arquivos):
    caminho_export = []
    for periodo in range(len(periodo_anos)):
        for categoria in range(len(nomes_categorias)):
            for arquivo in range(len(nomes_arquivos)):
                caminho_export.append('\\data\\' + periodo_anos[periodo] +
                                      '\\OutrosFormatos\\csv' + '\\Despesa\\' +
                                      nomes_categorias[categoria] + '\\' + nomes_arquivos[arquivo] + '.csv')

    return caminho_export


def gerar_caminho_receitas_xlsx(periodo_anos, nomes_arquivos):
    caminho_import_receitas = []
    for periodo in range(len(periodo_anos)):
        caminho_import_receitas.append('\\data\\' + periodo_anos[periodo] +
                                       '\\Receita\\' + nomes_arquivos[periodo] + '.xlsx')

    return caminho_import_receitas


def gerar_caminho_receitas_csv(periodo_anos, nomes_arquivos):
    caminho_export_receitas = []
    for periodo in range(len(periodo_anos)):
        caminho_export_receitas.append('\\data\\' + periodo_anos[periodo] +
                                       '\\OutrosFormatos\\csv' + '\\Receita\\' +
                                       nomes_arquivos[periodo] + '.csv')

    return caminho_export_receitas


def gerar_pastas_despesas_csv(periodo_anos, nomes_categorias):
    pastas_despesas_csv = []
    for periodo in range(len(periodo_anos)):
        for categoria in range(len(nomes_categorias)):
            pastas_despesas_csv.append('\\data\\' + periodo_anos[periodo] +
                                       '\\OutrosFormatos\\csv' + '\\Despesa\\'
                                       + nomes_categorias[categoria])

    for pasta in pastas_despesas_csv:
        os.makedirs(os.getcwd() + pasta, mode=0o666, exist_ok=True)

    print('Pastas para a exportação dos arquivos de despesas em .csv foram criadas')


def gerar_pastas_receitas_csv(periodo_anos):
    pastas_export_receitas = []
    for periodo in range(len(periodo_anos)):
        pastas_export_receitas.append('\\data\\' + periodo_anos[periodo] + '\\OutrosFormatos\\csv' + '\\Receita\\')

    for pasta in pastas_export_receitas:
        os.makedirs(os.getcwd() + pasta, mode=0o666, exist_ok=True)

    print('Pastas para a exportação dos arquivos de receitas em .csv foram criadas')


def gerar_pastas_despesas_dta(periodo_anos, nomes_categorias):
    pastas_despesas_dta = []
    for periodo in range(len(periodo_anos)):
        for categoria in range(len(nomes_categorias)):
            pastas_despesas_dta.append('\\data\\' + periodo_anos[periodo] +
                                       '\\OutrosFormatos\\dta' + '\\Despesa\\' + nomes_categorias[categoria])

    for pasta in pastas_despesas_dta:
        os.makedirs(os.getcwd() + pasta, mode=0o666, exist_ok=True)

    print('Pastas para a exportação dos arquivos de despesas em .dta foram criadas')


def gerar_pastas_receitas_dta(periodo_anos):
    pastas_export_receitas_dta = []
    for periodo in range(len(periodo_anos)):
        pastas_export_receitas_dta.append('\\data\\' + periodo_anos[periodo] + '\\OutrosFormatos\\dta' + '\\Receita\\')

    for pasta in pastas_export_receitas_dta:
        os.makedirs(os.getcwd() + pasta, mode=0o666, exist_ok=True)

    print('Pastas para a exportação dos arquivos de receitas em .dta foram criadas')


def imp_exp_siops_despesas(arquivo_import, arquivo_export):
    dados = pd.read_excel(os.getcwd() + arquivo_import)
    dados.set_index(keys='UF', drop=False, inplace=True)

    cols_ident = dados.iloc[1:, 0:3]
    cols_ident.columns = ['COD. ESTADO', 'UF', 'ESTADO']

    colunas = ['COD. ESTADO', 'UF', 'ESTADO'] + ['c' + x for x in dados.iloc[0, 3:338].tolist()]
    colunas_valores = ['c' + x for x in dados.iloc[0, 3:338].tolist()]

    lst_cat_var = ['dot_inicial', 'dot_atualizada', 'despesas_empenhadas',
                   'despesas_liquidadas', 'despesas_pagas', 'restos_a_pagar',
                   'despesas_orcadas']

    lst_categorias = ['Dotação Inicial', 'Dotação Atualizada', 'Despesas Empenhadas',
                      'Despesas Liquidadas', 'Despesas Pagas', 'Inscritas em Restos a Pagar não Processados',
                      'Despesas Orçadas']

    lst_categorias_num = ['1', '2', '3', '4', '5', '6', '7', ]

    lst_slices = [dados.iloc[1:, 3:338], dados.iloc[1:, 338:673], dados.iloc[1:, 673:1008],
                  dados.iloc[1:, 1008:1343], dados.iloc[1:, 1343:1678], dados.iloc[1:, 1678:2013],
                  dados.iloc[1:, 2013:]]

    dados_final = pd.DataFrame()

    for cat, categoria, cat_num, fatia in zip(lst_cat_var, lst_categorias, lst_categorias_num, lst_slices):
        cat = pd.concat(objs=[cols_ident, fatia], axis=1)
        cat.columns = colunas
        cat['Categoria'] = categoria
        cat['Categoria_num'] = cat_num
        cols = ['Categoria'] + ['Categoria_num'] + colunas
        cat = cat[cols]

        cat['ESTADO'] = cat['ESTADO'].str.strip()
        cat['COD. ESTADO'] = cat['COD. ESTADO'].astype(int).astype(str)
        cat[colunas_valores] = cat[colunas_valores].astype(float)
        cat.reset_index(drop=True, inplace=True)

        dados_final = pd.concat([dados_final, cat], axis=0)

    dados_final.to_csv(path_or_buf=os.getcwd() + arquivo_export, index=False, encoding='iso-8859-1')
    print(f'{arquivo_export} exportado')


def imp_exp_siops_receitas(arquivo_import, arquivo_export):
    dados = pd.read_excel(os.getcwd() + arquivo_import)
    dados.set_index(keys='UF', drop=False, inplace=True)

    cols_ident = dados.iloc[1:, 0:3]
    cols_ident.columns = ['COD. ESTADO', 'ESTADO', 'UF']

    colunas = ['COD. ESTADO', 'ESTADO', 'UF'] + ['c' + x for x in dados.iloc[0, 3:396].tolist()]
    colunas_valores = ['c' + x for x in dados.iloc[0, 3:396].tolist()]

    lst_cat_var = ['prev_inicial_receitas_brutas', 'deducao_trans_b', 'prev_atualizada_receitas_brutas',
                   'deducao_trans_d', 'receitas_realizadas_brutas', 'deducao_receitas_f',
                   'deducao_trans_g', 'receitas_base_calculo_ASPS',
                   'deducao_fundeb', 'total_receitas_liquidas_realizadas', 'receitas_orcadas']

    lst_categorias = ['Previsão Inicial das Receitas Brutas (a)',
                      'Dedução de Transferências Const. e Legais a Municípios (b)',
                      'Previsão Atualizada das Receitas Brutas (c)',
                      'Dedução de Transferências Const. e Legais a Municípios (d)',
                      'Receitas Realizadas Brutas (e)', 'Deduções das Receitas (f)',
                      'Dedução de Transferências Const. e Legais a Municípios (g)',
                      'Receitas Realizadas da base para cálculo do percentual de aplicacao em ASPS (h) = (e-f-g)',
                      'Dedução Para Formação do FUNDEB (i)',
                      'Total Geral das Receitas Liquidas Realizadas (j) = (e-f-g-i)',
                      'Receitas Orçadas']

    lst_categorias_num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']

    lst_slices = [dados.iloc[1:, 3:396], dados.iloc[1:, 396:789], dados.iloc[1:, 789:1182],
                  dados.iloc[1:, 1182:1575], dados.iloc[1:, 1575:1968], dados.iloc[1:, 1968:2361],
                  dados.iloc[1:, 2361:2754], dados.iloc[1:, 2754:3147], dados.iloc[1:, 3147:3540],
                  dados.iloc[1:, 3540:3933], dados.iloc[1:, 3933:]]

    dados_final = pd.DataFrame()

    for cat, categoria, cat_num, fatia in zip(lst_cat_var, lst_categorias, lst_categorias_num, lst_slices):
        cat = pd.DataFrame()
        cat = pd.concat(objs=[cols_ident, fatia], axis=1)
        cat.columns = colunas
        cat['Categoria'] = categoria
        cat['Categoria_num'] = cat_num
        cols = ['Categoria'] + ['Categoria_num'] + colunas
        cat = cat[cols]

        cat['ESTADO'] = cat['ESTADO'].str.strip()
        cat['COD. ESTADO'] = cat['COD. ESTADO'].astype(int).astype(str)
        cat[colunas_valores] = cat[colunas_valores].astype(float)
        cat.reset_index(drop=True, inplace=True)

        dados_final = pd.concat([dados_final, cat], axis=0)

    dados_final.to_csv(path_or_buf=os.getcwd() + arquivo_export, index=False, encoding='iso-8859-1')
    print(f'{arquivo_export} exportado')


###########################################################
# definindo listas
###########################################################
anos = ['2018', '2019', '2020']

categorias_despesas = ['1 - Recursos Ordinários - Fonte Livre',
                       '2 - Receitas de Impostos e Transferencias de Impostos',
                       '3 - Transferência Fundo a Fundo de Recursos do SUS Provenientes do Governo Federal',
                       '4 -Transferência Fundo a Fundo de Recursos do SUS Provenientes do Governo Estadual',
                       '5 - Transferência de Convênios ou de Contratos de Repasse Vinculados à Saúde',
                       '6 - Operações de Crédito Vinculadas à Saúde',
                       '7 - Royalties de Petróleo Vinculadas à Saúde',
                       '8 - Outros Recursos Vinculados à Saúde']

arquivos_despesas = ['301 - Atenção Basica', '302 - Assistência Hospitalar Ambulatorial',
                     '303 - Suporte Profilático Terapêutico', '304 - Vigilância Sanitária',
                     '305 - Vigilância Epidemiológica', '306 - Alimentação e Nutrição',
                     'Administrativas', 'Informações Complementares']

arquivos_receitas = ['Estadual - Receitas de 2018', 'Estadual - Receitas de 2019', 'Estadual - Receitas de 2020']

caminho_despesas_xlsx = gerar_caminho_despesas_xlsx(periodo_anos=anos,
                                                    nomes_categorias=categorias_despesas,
                                                    nomes_arquivos=arquivos_despesas)

caminho_despesas_csv = gerar_caminho_despesas_csv(periodo_anos=anos,
                                                  nomes_categorias=categorias_despesas,
                                                  nomes_arquivos=arquivos_despesas)

caminho_receitas_xlsx = gerar_caminho_receitas_xlsx(periodo_anos=anos,
                                                    nomes_arquivos=arquivos_receitas)

caminho_receitas_csv = gerar_caminho_receitas_csv(periodo_anos=anos,
                                                  nomes_arquivos=arquivos_receitas)

gerar_pastas_despesas_csv(periodo_anos=anos,
                          nomes_categorias=categorias_despesas)

gerar_pastas_receitas_csv(periodo_anos=anos)

# exportando os arquivos .csv de despesas
for item in range(len(caminho_despesas_xlsx)):
    imp_exp_siops_despesas(caminho_despesas_xlsx[item], caminho_despesas_csv[item])

# exportando os arquivos .csv de receitas
for item in range(len(caminho_receitas_xlsx)):
    imp_exp_siops_receitas(caminho_receitas_xlsx[item], caminho_receitas_csv[item])

# aqui acaba a parte de estruturação das bases e conversão das mesmas em .xlsx para .csv;
# começa a criacão de pastas .dta

gerar_pastas_despesas_dta(periodo_anos=anos,
                          nomes_categorias=categorias_despesas)

gerar_pastas_receitas_dta(periodo_anos=anos)
