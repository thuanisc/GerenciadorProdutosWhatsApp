# utils.py
# Este módulo está reservado para funções auxiliares futuras.
# No momento, não há funções reutilizadas fora de produtos/orçamento,
# mas pode-se mover, por exemplo, formatação de valores ou helpers aqui futuramente.

def formatar_moeda(valor):
    return f"R${valor:.2f}".replace('.', ',')
