import cadquery as cq
import math

# ==========================================
# Entrada manual de parâmetros
# ==========================================

def input_float(prompt, default):
    value = input(f"{prompt} [{default}]: ").strip()
    if not value:
        return default
    try:
        return float(value.replace(',', '.'))
    except ValueError:
        print(f"Valor inválido. Usando padrão: {default}")
        return default


def input_int(prompt, default, minimum=1):
    value = input(f"{prompt} [{default}]: ").strip()
    if not value:
        return default
    try:
        iv = int(value)
        if iv < minimum:
            print(f"Valor menor que {minimum}. Usando padrão: {default}")
            return default
        return iv
    except ValueError:
        print(f"Valor inválido. Usando padrão: {default}")
        return default


print("Informe os parâmetros do galpão. Pressione Enter para aceitar o valor padrão.")
L = input_float("Vão do galpão L (mm)", 15000.0)
B = input_float("Espaçamento entre pórticos B (mm)", 6000.0)
H = input_float("Altura da coluna H (mm)", 6000.0)
inclinacao = input_float("Inclinação do telhado (%)", 0.10)
n_vaos = input_int("Número de vãos n_vaos", 10, minimum=1)
n_pavilhoes = input_int("Número de pavilhões n_pavilhoes", 2, minimum=1)
espacamento_pavilhao = input_float("Espaçamento entre pavilhões (mm)", 0.0)

# Altura da cumeeira
Hcum = H + (L/2) * inclinacao

# Comprimento total ao longo do eixo Y
comprimento = B * n_vaos

# Posições dos pórticos
y_positions = [i * B for i in range(n_vaos + 1)]

# Posições dos pavilhões ao longo do eixo X
x_positions = [i * (L + espacamento_pavilhao) for i in range(n_pavilhoes)]

# ==========================================
# Função para criar um pórtico em um dado Y
# ==========================================
def criar_portico(y, x_offset=0.0):
    """Retorna um compound de arestas do pórtico localizado em Y = y, deslocado em X."""
    pontos = []
    # Coluna esquerda (base ao topo)
    pontos.append( (-L/2 + x_offset, y, 0) )
    pontos.append( (-L/2 + x_offset, y, H) )
    # Viga esquerda (topo da coluna até cumeeira)
    pontos.append( (-L/2 + x_offset, y, H) )
    pontos.append( (0 + x_offset, y, Hcum) )
    # Viga direita (cumeeira até topo da coluna direita)
    pontos.append( (0 + x_offset, y, Hcum) )
    pontos.append( (L/2 + x_offset, y, H) )
    # Coluna direita (topo à base)
    pontos.append( (L/2 + x_offset, y, H) )
    pontos.append( (L/2 + x_offset, y, 0) )
    # Linha de base (opcional, para rigidez)
    pontos.append( (L/2 + x_offset, y, 0) )
    pontos.append( (-L/2 + x_offset, y, 0) )

    # Criar as arestas
    edges = []
    for i in range(0, len(pontos), 2):
        p1 = pontos[i]
        p2 = pontos[i+1]
        edges.append(cq.Edge.makeLine(cq.Vector(p1[0], p1[1], p1[2]),
                                      cq.Vector(p2[0], p2[1], p2[2])))
    return cq.Compound.makeCompound(edges)

# ==========================================
# Criar os pavilhões lado a lado
# ==========================================
elementos = []
for x_offset in x_positions:
    for y in y_positions:
        elementos.append(criar_portico(y, x_offset))

# ==========================================
# Adicionar terças (longitudinais) na cobertura
# ==========================================
# Número de terças por água (espaçamento máximo 2,5 m, conforme manual)
n_tercas = max(2, int(L / 2500) + 1)   # ao longo do vão
for x_offset in x_positions:
    for i in range(n_tercas):
        x = -L/2 + i * (L / (n_tercas - 1))
        # Altura da terça na posição x (linha reta do telhado)
        if x <= 0:
            z = H + (Hcum - H) * (x + L/2) / (L/2)
        else:
            z = H + (Hcum - H) * (L/2 - x) / (L/2)
        # Linha de y inicial a y final
        linha = cq.Edge.makeLine(cq.Vector(x + x_offset, y_positions[0], z), cq.Vector(x + x_offset, y_positions[-1], z))
        elementos.append(linha)

# ==========================================
# Adicionar vigas de fechamento lateral (opcional)
# ==========================================
# Três níveis: base, intermediário (opcional) e topo
for x_offset in x_positions:
    for y in y_positions:
        for z in [0, H/2, H]:
            linha_base = cq.Edge.makeLine(cq.Vector(-L/2 + x_offset, y, z), cq.Vector(L/2 + x_offset, y, z))
            elementos.append(linha_base)

estrutura = cq.Compound.makeCompound(elementos)

# ==========================================
# Exportar para STEP
# ==========================================
arquivo = "galpao_wireframe.stp"
cq.exporters.export(estrutura, arquivo, exportType='STEP')
print(f"Arquivo gerado: {arquivo}")
print(f"O modelo contém {len(estrutura.Edges())} arestas (linhas) para {n_pavilhoes} pavilhão(ões).")