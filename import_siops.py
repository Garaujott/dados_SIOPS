import os
import pandas as pd

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
                '\\data\\' + anos[i] + '\\csv' + '\\Despesa\\' + pastas[j] + '\\' + arquivos[k] + '.csv')

pastas_export = []
for i in range(len(anos)):
    for j in range(len(pastas)):
        for k in range(len(arquivos)):
            pastas_export.append('\\data\\' + anos[i] + '\\csv' + '\\Despesa\\' + pastas[j])

for i in pastas_export:
    os.makedirs(os.getcwd() + i, mode=0o666, exist_ok=True)


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
    lst_slices = [dados.iloc[1:, 3:338], dados.iloc[1:, 338:673], dados.iloc[1:, 673:1008],
                  dados.iloc[1:, 1008:1343], dados.iloc[1:, 1343:1678], dados.iloc[1:, 1678:2013],
                  dados.iloc[1:, 2013:]]

    dados_final = pd.DataFrame()

    for k, i, j in zip(lst_cat_var, lst_categorias, lst_slices):
        k = []
        k = pd.concat(objs=[cols_ident, j], axis=1)
        k.columns = colunas
        k['Categoria'] = i
        cols = ['Categoria'] + colunas
        k = k[cols]
        k['COD. ESTADO'] = k['COD. ESTADO'].astype(int).astype(str)
        k[colunas_valores] = k[colunas_valores].astype(float)
        k.reset_index(drop=True, inplace=True)
        dados_final = pd.concat([dados_final, k], axis=0)

    dados_final.to_csv(path_or_buf=os.getcwd() + arquivo_export, index=False, encoding='iso-8859-1')
    print(f'{arquivo_export} exportado')

for i in range(len(caminho_import)):
    imp_exp_siops_despesas(caminho_import[i], caminho_export[i])