import pandas as pd
from unidecode import unidecode

# treinos = {
#     'Treino A': {
#         'Pulley Frente': {
#             'id': 1,
#             'imagem': 'local/Pulley_Frente.png',
#             'concluido': False,
#             'area_do_corpo': 'Costas'
#         },
#         'Remada Articulada Pronada': {
#             'id': 2,
#             'imagem': 'local/Remada_Articulada_Pronada.png',
#             'concluido': False,
#             'area_do_corpo': 'Costas'
#         },
#         'Remada Cavalinho': {
#             'id': 3,
#             'imagem': 'local/Remada_Cavalinho.png',
#             'concluido': False,
#             'area_do_corpo': 'Costas'
#         },
#         'Pull Down': {
#             'id': 4,
#             'imagem': 'local/Pull_Down.png',
#             'concluido': False,
#             'area_do_corpo': 'Costas'
#         },
#         'Rosca Direta com Barra W': {
#             'id': 5,
#             'imagem': 'local/Rosca_Direta_Bar_W.png',
#             'concluido': False,
#             'area_do_corpo': 'Bíceps'
#         },
#         'Rosca Alternada': {
#             'id': 6,
#             'imagem': 'local/Rosca_Alternada.png',
#             'concluido': False,
#             'area_do_corpo': 'Bíceps'
#         },
#         'Rosca Inversa com Barra W': {
#             'id': 7,
#             'imagem': 'local/Rosca_Inversa_Bar_W.png',
#             'concluido': False,
#             'area_do_corpo': 'Antebraço'
#         },
#         'Abdominal Remador': {
#             'id': 8,
#             'imagem': 'local/Abdominal_Remador.png',
#             'concluido': False,
#             'area_do_corpo': 'Abdominais'
#         }
#     },
#     'Treino B': {
#         'Pulley Frente': {
#             'id': 1,
#             'imagem': 'local/Pulley_Frente.png',
#             'concluido': False,
#             'area_do_corpo': 'Costas'
#         }
#     }
# }


def transformar_excel_em_dicionario():
    caminho_arquivo = 'academia_app/base/treinos.xlsx'
    # Carregar a planilha do Excel
    df = pd.read_excel(caminho_arquivo)

    # Inicializar o dicionário de treinos
    treinos = {}

    # Preencher o dicionário com os dados dos exercícios
    for linha in range(df.shape[0]):
        treino = df.loc[linha, 'Treino']
        exercicio = df.loc[linha, 'Exercicio']
        imagem = unidecode(df.loc[linha, 'Imagem'])
        gif = unidecode(df.loc[linha, 'Imagem_Gif'])

        # Verificar se o treino já existe no dicionário, se não, inicializar
        if treino not in treinos:
            treinos[treino] = {}

        # Adicionar o exercício ao treino correspondente
        treinos[treino][exercicio] = {
            'id': int(df.loc[linha, 'ID']),
            'imagem': imagem,
            'gif': gif,
            'concluido': False,
            'area_do_corpo': df.loc[linha, 'Área do Corpo'],
        }

    return treinos

print(transformar_excel_em_dicionario())