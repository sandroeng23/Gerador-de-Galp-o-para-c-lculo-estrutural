# Gerador de Galpão Wireframe

Script Python para gerar um modelo wireframe de galpões com pórticos, terças e vigas de fechamento. O programa suporta 10 vãos por galpão e múltiplos pavilhões lado a lado.

## Requisitos

- Python 3.13
- `cadquery==2.7.0`
- `cadquery-ocp==7.8.1.1.post1`
- `cadquery_vtk==9.3.1`
- `numpy==2.4.6`

## Instalação

```powershell
cd "c:\Users\aless\OneDrive\Documentos\Projetos VSCODE\cad"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install cadquery==2.7.0 cadquery-ocp==7.8.1.1.post1 cadquery_vtk==9.3.1 numpy==2.4.6
```

## Uso

```powershell
python galpao.py
```

O arquivo gerado será `galpao_wireframe.stp`.

## Parâmetros do projeto

- `L`: vão do galpão
- `B`: espaçamento entre pórticos
- `H`: altura da coluna
- `inclinacao`: inclinação do telhado
- `n_vaos`: número de vãos do pórtico
- `n_pavilhoes`: número de pavilhões lado a lado

## Observações

- O script gera um modelo em wireframe, ideal para visualização ou exportação para CAD.
- Use o ambiente virtual para manter as dependências isoladas.

