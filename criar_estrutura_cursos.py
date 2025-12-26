"""
Cria estrutura de diretórios para cursos
"""

import os
import re
import unicodedata
from pathlib import Path


def criar_slug(texto):
    """
    Converte texto para formato slug (sem acentos, minúsculas, hífens)
    """
    # Remove acentos
    texto = unicodedata.normalize('NFKD', texto)
    texto = texto.encode('ASCII', 'ignore').decode('ASCII')
    
    # Converte para minúsculas
    texto = texto.lower()
    
    # Remove caracteres especiais e substitui espaços por hífens
    texto = re.sub(r'[^\w\s-]', '', texto)
    texto = re.sub(r'[-\s]+', '-', texto)
    
    # Remove hífens do início e fim
    texto = texto.strip('-')
    
    return texto


def criar_estrutura_curso(nome_curso, numero, diretorio_base='cursos'):
    """
    Cria a estrutura de diretórios para um curso
    """
    slug = criar_slug(nome_curso)
    
    # Caminho base do curso com número sequencial
    curso_path = Path(diretorio_base) / f"{numero:02d}-{slug}"
    
    # Cria diretório do curso
    curso_path.mkdir(parents=True, exist_ok=True)
    print(f"✓ Criado: {curso_path}")
    
    # Cria pasta src
    src_path = curso_path / 'src'
    src_path.mkdir(exist_ok=True)
    print(f"  ✓ Criado: {src_path}")
    
    # Cria .gitkeep dentro de src
    gitkeep_path = src_path / '.gitkeep'
    gitkeep_path.touch()
    print(f"    ✓ Criado: {gitkeep_path}")
    
    # Cria README.md
    readme_path = curso_path / 'README.md'
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(f"# {nome_curso}\n\n")
        f.write("## Descrição\n\n")
        f.write("<!-- Adicione aqui a descrição do curso -->\n\n")
        f.write("## Conteúdo\n\n")
        f.write("<!-- Adicione aqui o conteúdo do curso -->\n")
    print(f"  ✓ Criado: {readme_path}")


def main():
    """
    Extrai os nomes dos cursos e cria a estrutura de diretórios
    """
    # Lista de cursos extraídos do HTML
    cursos = [
        "Conhecendo e Instalando o Docker",
        "Primeiros Passos com o Docker",
        "Armazenamento de Dados com Docker",
        "Processamento, Logs e Rede com Docker",
        "Definição e Criação de um Docker File",
        "Trabalhando com Docker Compose",
        "Docker: Utilização Prática no Cenário de Microsserviços"
    ]
    
    print(f"\n📚 Encontrados {len(cursos)} cursos\n")
    print("=" * 60)
    
    # Cria a estrutura para cada curso
    for i, curso in enumerate(cursos, 1):
        print(f"\n[{i}/{len(cursos)}] Criando estrutura para: {curso}")
        print("-" * 60)
        criar_estrutura_curso(curso, i)
    
    print("\n" + "=" * 60)
    print("✅ Estrutura de diretórios criada com sucesso!")
    print(f"📂 Diretório base: cursos/")


if __name__ == "__main__":
    main()
