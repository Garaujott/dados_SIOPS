import os
import pandas as pd

###########################################################
# Importação das tabelas de DESPESAS
###########################################################


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

    for k, i, l, j in zip(lst_cat_var, lst_categorias, lst_categorias_num, lst_slices):
        k = []
        k = pd.concat(objs=[cols_ident, j], axis=1)
        k.columns = colunas
        k['Categoria'] = i
        k['Categoria_num'] = l
        cols = ['Categoria'] + ['Categoria_num'] + colunas
        k = k[cols]

        k['ESTADO'] = k['ESTADO'].str.strip()
        k['COD. ESTADO'] = k['COD. ESTADO'].astype(int).astype(str)
        k[colunas_valores] = k[colunas_valores].astype(float)
        k.reset_index(drop=True, inplace=True)

        dados_final = pd.concat([dados_final, k], axis=0)

    dados_final.to_csv(path_or_buf=os.getcwd() + arquivo_export, index=False, encoding='iso-8859-1')
    print(f'{arquivo_export} exportado')

# Preparando os caminhos para importar e exportar os arquivos


anos = ['2018', '2019', '2020']

pastas = ['1 - Recursos Ordinários - Fonte Livre',
          '2 - Receitas de Impostos e Transferencias de Impostos',
          '3 - Transferência Fundo a Fundo de Recursos do SUS Provenientes do Governo Federal',
          '4 -Transferência Fundo a Fundo de Recursos do SUS Provenientes do Governo Estadual',
          '5 - Transferência de Convênios ou de Contratos de Repasse Vinculados à Saúde',
          '6 - Operações de Crédito Vinculadas à Saúde',
          '7 - Royalties de Petróleo Vinculadas à Saúde',
          '8 - Outros Recursos Vinculados à Saúde']

arquivos = ['301 - Atenção Basica', '302 - Assistência Hospitalar Ambulatorial',
            '303 - Suporte Profilático Terapêutico', '304 - Vigilância Sanitária',
            '305 - Vigilância Epidemiológica', '306 - Alimentação e Nutrição',
            'Administrativas', 'Informações Complementares']

caminho_import = []

for i in range(len(anos)):
    for j in range(len(pastas)):
        for k in range(len(arquivos)):
            caminho_import.append('\\data\\' + anos[i] + '\\Despesa\\' + pastas[j] + '\\' + arquivos[k] + '.xlsx')

caminho_export = []

for i in range(len(anos)):
    for j in range(len(pastas)):
        for k in range(len(arquivos)):
            caminho_export.append(
                '\\data\\' + anos[i] + '\\OutrosFormatos\\csv' + '\\Despesa\\' + pastas[j] + '\\' + arquivos[k] + '.csv')

pastas_export = []
for i in range(len(anos)):
    for j in range(len(pastas)):
            pastas_export.append('\\data\\' + anos[i] + '\\OutrosFormatos\\csv' + '\\Despesa\\' + pastas[j])

for i in pastas_export:
    os.makedirs(os.getcwd() + i, mode=0o666, exist_ok=True)

# exportando os arquivos .csv de receitas
for i in range(len(caminho_import)):
    imp_exp_siops_despesas(caminho_import[i], caminho_export[i])

###########################################################
# Importação das tabelas de RECEITAS
###########################################################

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

    for k, i, l, j in zip(lst_cat_var, lst_categorias, lst_categorias_num, lst_slices):
        k = []
        k = pd.concat(objs=[cols_ident, j], axis=1)
        k.columns = colunas
        k['Categoria'] = i
        k['Categoria_num'] = l
        cols = ['Categoria'] + ['Categoria_num'] + colunas
        k = k[cols]

        k['ESTADO'] = k['ESTADO'].str.strip()
        k['COD. ESTADO'] = k['COD. ESTADO'].astype(int).astype(str)
        k[colunas_valores] = k[colunas_valores].astype(float)
        k.reset_index(drop=True, inplace=True)

        dados_final = pd.concat([dados_final, k], axis=0)

    dados_final.to_csv(path_or_buf=os.getcwd() + arquivo_export, index=False, encoding='iso-8859-1')
    print(f'{arquivo_export} exportado')

# Preparando os caminhos para importar e exportar os arquivos


anos = ['2018', '2019', '2020']
receitas = ['Estadual - Receitas de 2018', 'Estadual - Receitas de 2019', 'Estadual - Receitas de 2020']

caminho_import_receitas = []
for k in range(len(anos)):
    caminho_import_receitas.append('\\data\\' + anos[k] + '\\Receita\\' + receitas[k] + '.xlsx')

caminho_export_receitas = []
for k in range(len(anos)):
    caminho_export_receitas.append('\\data\\' + anos[k] + '\\OutrosFormatos\\csv' + '\\Receita\\' + receitas[k] + '.csv')

pastas_export_receitas = []
for k in range(len(anos)):
    pastas_export_receitas.append('\\data\\' + anos[k] + '\\OutrosFormatos\\csv' + '\\Receita\\')

for i in pastas_export_receitas:
    os.makedirs(os.getcwd() + i, mode=0o666, exist_ok=True)

# exportando os arquivos .csv de receitas
for i in range(len(caminho_import_receitas)):
    imp_exp_siops_receitas(caminho_import_receitas[i], caminho_export_receitas[i])


#############################################################
# Criação das pastas para a exportação dos arquivos .dta (STATA)
#############################################################

anos = ['2018', '2019', '2020']

pastas = ['1 - Recursos Ordinários - Fonte Livre',
          '2 - Receitas de Impostos e Transferencias de Impostos',
          '3 - Transferência Fundo a Fundo de Recursos do SUS Provenientes do Governo Federal',
          '4 -Transferência Fundo a Fundo de Recursos do SUS Provenientes do Governo Estadual',
          '5 - Transferência de Convênios ou de Contratos de Repasse Vinculados à Saúde',
          '6 - Operações de Crédito Vinculadas à Saúde',
          '7 - Royalties de Petróleo Vinculadas à Saúde',
          '8 - Outros Recursos Vinculados à Saúde']

pastas_export_dta = []
for i in range(len(anos)):
    for j in range(len(pastas)):
            pastas_export.append('\\data\\' + anos[i] + '\\OutrosFormatos\\dta' + '\\Despesa\\' + pastas[j])

for i in pastas_export:
    os.makedirs(os.getcwd() + i, mode=0o666, exist_ok=True)

#############################################################
anos = ['2018', '2019', '2020']
receitas = ['Estadual - Receitas de 2018', 'Estadual - Receitas de 2019', 'Estadual - Receitas de 2020']

pastas_export_receitas_dta = []
for k in range(len(anos)):
    pastas_export_receitas_dta.append('\\data\\' + anos[k] + '\\OutrosFormatos\\dta' + '\\Receita\\')

for i in pastas_export_receitas_dta:
    os.makedirs(os.getcwd() + i, mode=0o666, exist_ok=True)