import pandas as pd

# def transformar_excel_em_dicionario(caminho_arquivo):
#     # Carregar a planilha do Excel
#     df = pd.read_excel(caminho_arquivo)

#     # Inicializar o dicionário de treinos
#     treinos = {}

#     # Preencher o dicionário com os dados dos exercícios
#     for linha in range(df.shape[0]):
#         treino = df.loc[linha, 'Treino']
#         exercicio = df.loc[linha, 'Exercicio']
        
#         # Verificar se o treino já existe no dicionário, se não, inicializar
#         if treino not in treinos:
#             treinos[treino] = {}
        
#         # Adicionar o exercício ao treino correspondente
#         treinos[treino][exercicio] = {
#             'id': df.loc[linha, 'ID'],
#             'imagem': df.loc[linha, 'Imagem'],
#             'concluido': False,
#             'area_do_corpo': df.loc[linha, 'Área do Corpo']
#         }

#     return treinos

# # Exemplo de uso da função:
# caminho_arquivo = 'academia_app/base/treinos.xlsx'
# treinos = transformar_excel_em_dicionario(caminho_arquivo)
# print('---------------')
# print(treinos)
# # print(type(treinos['Treino A']['Pulley Frente']['concluido']))
# print('-----------')
# print(treinos2)
# print(type(treinos2['Treino A']['Pulley Frente']['concluido']))
