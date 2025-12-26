#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from bs4 import BeautifulSoup
import unicodedata
import re

def extrair_modulos_com_cursos_do_html(html):
    """Extrai módulos e seus respectivos cursos, mantendo a relação correta"""
    soup = BeautifulSoup(html, 'html.parser')
    modulos_com_cursos = []
    
    # Encontra todos os buttons que são módulos
    buttons = soup.find_all('button', class_='sc-tQeVH foWZJB')
    
    for idx, button in enumerate(buttons):
        # Extrai nome do módulo
        text_parts = []
        for child in button.children:
            if isinstance(child, str):
                text = child.strip()
                if text:
                    text_parts.append(text)
            elif hasattr(child, 'text'):
                if 'sc-jzlYRg' not in child.get('class', []):
                    if 'sc-gCRolh' not in child.get('class', []):
                        if 'sc-jOoWRn' not in child.get('class', []):
                            text = child.text.strip()
                            if text and text != child.text.strip():
                                pass
        
        if not text_parts:
            continue
        
        nome_modulo = text_parts[0]
        nome_modulo = re.sub(r'\d+\s*atividades$', '', nome_modulo).strip()
        
        # Encontra o div com os cursos deste módulo
        # O próximo elemento após o button é um div com classe "sc-gGTSdS"
        cursos_modulo = []
        current = button.find_next_sibling('div', class_='sc-gGTSdS')
        
        if current:
            # Encontra todos os h3 dentro deste div (que são os cursos)
            h3_tags = current.find_all('h3', class_='sc-kvaGlN fgSeyi')
            for h3 in h3_tags:
                titulo = h3.text.strip()
                if titulo:
                    cursos_modulo.append(titulo)
        
        if nome_modulo and cursos_modulo:
            modulos_com_cursos.append({
                'nome': nome_modulo,
                'cursos': cursos_modulo
            })
    
    return modulos_com_cursos

def extrair_modulos_do_html(html):
    """Extrai nomes dos módulos do HTML (compatibilidade)"""
    modulos_data = extrair_modulos_com_cursos_do_html(html)
    return [m['nome'] for m in modulos_data]

def extrair_cursos_do_html(html):
    """Extrai nomes dos cursos do HTML (compatibilidade)"""
    soup = BeautifulSoup(html, 'html.parser')
    cursos = []
    
    # Encontra todos os h3 com class específica (títulos dos cursos)
    h3_tags = soup.find_all('h3', class_='sc-kvaGlN fgSeyi')
    
    for h3 in h3_tags:
        titulo = h3.text.strip()
        if titulo and titulo not in cursos:
            cursos.append(titulo)
    
    return cursos

def criar_slug(texto):
    """Converte texto para slug format (sem acentos, minúsculas, hífens)"""
    # Normaliza o texto (remove acentos)
    texto_nfkd = unicodedata.normalize('NFKD', texto)
    texto_sem_acentos = ''.join([c for c in texto_nfkd if not unicodedata.combining(c)])
    
    # Converte para minúsculas e substitui espaços por hífens
    slug = texto_sem_acentos.lower()
    slug = re.sub(r'[^a-z0-9\s\-]', '', slug)  # Remove caracteres especiais
    slug = re.sub(r'\s+', '-', slug)  # Espaços em hífens
    slug = re.sub(r'-+', '-', slug)   # Hífens múltiplos em um único
    slug = slug.strip('-')             # Remove hífens nas extremidades
    
    return slug

def criar_estrutura_curso(nome_curso, numero, diretorio_base):
    """Cria a estrutura de diretório para um curso"""
    slug_curso = criar_slug(nome_curso)
    nome_dir = f"{numero:02d}-{slug_curso}"
    caminho_curso = Path(diretorio_base) / nome_dir
    
    # Cria o diretório principal
    caminho_curso.mkdir(parents=True, exist_ok=True)
    
    # Cria a pasta src
    (caminho_curso / 'src').mkdir(exist_ok=True)
    
    # Cria .gitkeep em src
    (caminho_curso / 'src' / '.gitkeep').touch()
    
    # Cria README.md
    readme_content = f"""# {nome_curso}

## Descrição

Diretório para armazenar arquivos e recursos do curso **{nome_curso}**.

## Estrutura

```
{nome_dir}/
├── src/          # Código-fonte e recursos
└── README.md     # Este arquivo
```

## Links Úteis

- [DIO - Digital Innovation One](https://www.dio.me)

---

*Criado automaticamente pelo script de estruturação*
"""
    
    (caminho_curso / 'README.md').write_text(readme_content, encoding='utf-8')
    
    return nome_dir

def criar_readme_modulo(modulo_info):
    """Cria README.md com índice de cursos para um módulo específico"""
    nome_modulo = modulo_info['nome']
    cursos = modulo_info['cursos']
    
    readme = f"""# {nome_modulo}

## Índice de Cursos

"""
    
    for idx, curso in enumerate(cursos, 1):
        dir_curso = curso['diretorio']
        nome_curso = curso['nome']
        readme += f"{idx}. [{nome_curso}](./{dir_curso}/)\n"
    
    return readme

def main():
    """Função principal"""
    # Lê o arquivo HTML
    html_file = Path('/home/luciano/workspace/programacao/miscelania/html_geral.html')
    
    if not html_file.exists():
        print(f"❌ Arquivo {html_file} não encontrado")
        return
    
    html_content = html_file.read_text(encoding='utf-8')
    
    # Extrai módulos com seus respectivos cursos
    modulos_com_cursos = extrair_modulos_com_cursos_do_html(html_content)
    
    total_cursos = sum(len(m['cursos']) for m in modulos_com_cursos)
    
    print(f"\n📚 Módulos encontrados: {len(modulos_com_cursos)}")
    for i, mod in enumerate(modulos_com_cursos, 1):
        print(f"   {i}. {mod['nome']} ({len(mod['cursos'])} cursos)")
    
    print(f"\n📖 Total de cursos: {total_cursos}")
    
    # Define o diretório base para os cursos
    base_dir = Path('/home/luciano/workspace/programacao/miscelania/cursos')
    
    # Limpa o diretório anterior
    if base_dir.exists():
        import shutil
        shutil.rmtree(base_dir)
    
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # Se há módulos, organiza cursos por módulo
    if modulos_com_cursos:
        print(f"\n🎯 Criando estrutura com {len(modulos_com_cursos)} módulo(s)...\n")
        
        indice_modulo_readme = []
        
        for idx_modulo, modulo_info in enumerate(modulos_com_cursos, 1):
            nome_modulo = modulo_info['nome']
            cursos_modulo = modulo_info['cursos']
            
            # Cria slug do módulo para usar no diretório
            slug_modulo = criar_slug(nome_modulo)
            diretorio_modulo = base_dir / f"{idx_modulo:02d}-{slug_modulo}"
            diretorio_modulo.mkdir(parents=True, exist_ok=True)
            
            print(f"\n📁 Módulo {idx_modulo}: {nome_modulo}")
            print(f"   Diretório: {diretorio_modulo.name}")
            print(f"   Total de cursos: {len(cursos_modulo)}")
            
            # Armazena para o README
            info_modulo = {
                'numero': idx_modulo,
                'nome': nome_modulo,
                'slug': slug_modulo,
                'cursos': []
            }
            
            # Cria estrutura para cada curso do módulo
            for num_curso, nome_curso in enumerate(cursos_modulo, 1):
                nome_dir_curso = criar_estrutura_curso(nome_curso, num_curso, diretorio_modulo)
                print(f"   ✓ {num_curso}. {nome_curso}")
                
                info_modulo['cursos'].append({
                    'numero': num_curso,
                    'nome': nome_curso,
                    'diretorio': nome_dir_curso
                })
            
            # Cria README.md com índice de cursos para o módulo
            readme_modulo = criar_readme_modulo(info_modulo)
            (diretorio_modulo / 'README.md').write_text(readme_modulo, encoding='utf-8')
            
            indice_modulo_readme.append(info_modulo)
        
        # Cria README.md principal com índice dos módulos
        readme_principal = criar_readme_modulos(indice_modulo_readme)
    else:
        # Se não há módulos, cria cursos diretamente
        cursos = extrair_cursos_do_html(html_content)
        print(f"\n🎯 Criando estrutura com {len(cursos)} curso(s)...\n")
        
        for idx, nome_curso in enumerate(cursos, 1):
            nome_dir_curso = criar_estrutura_curso(nome_curso, idx, base_dir)
            print(f"   ✓ {idx}. {nome_curso}")
        
        readme_principal = criar_readme_cursos(cursos)
    
    (base_dir / 'README.md').write_text(readme_principal, encoding='utf-8')
    
    print(f"\n✅ Estrutura criada com sucesso em: {base_dir}")
    print(f"📄 README.md gerado com índice dos módulos/cursos")

def criar_readme_modulos(modulos_info):
    """Cria README.md com índice dos módulos"""
    readme = """# Índice de Cursos - Estrutura Modular

## 📚 Módulos Disponíveis

"""
    
    for modulo in modulos_info:
        slug = modulo['slug']
        num = modulo['numero']
        nome = modulo['nome']
        num_cursos = len(modulo['cursos'])
        
        readme += f"### {num}. [{nome}](./{num:02d}-{slug}/)\n\n"
        readme += f"**Total de cursos:** {num_cursos}\n\n"
        readme += "#### Cursos:\n\n"
        
        for curso in modulo['cursos']:
            dir_curso = curso['diretorio']
            nome_curso = curso['nome']
            readme += f"- [{nome_curso}](./{num:02d}-{slug}/{dir_curso}/)\n"
        
        readme += "\n---\n\n"
    
    readme += """
## 📖 Como Usar Esta Estrutura

1. **Navegação**: Cada módulo possui um diretório próprio numerado (01-, 02-, etc.)
2. **Organização**: Os cursos estão organizados dentro dos seus respectivos módulos
3. **Recursos**: Cada curso possui:
   - Pasta `src/` para código-fonte e recursos
   - Arquivo `README.md` com descrição específica
   - Arquivo `.gitkeep` para manter a pasta no Git

## 🔗 Links Úteis

- [DIO - Digital Innovation One](https://www.dio.me)

---

*Índice gerado automaticamente*
"""
    
    return readme

def criar_readme_cursos(cursos):
    """Cria README.md simples com lista de cursos"""
    readme = """# Índice de Cursos

## 📖 Cursos Disponíveis

"""
    
    for idx, curso in enumerate(cursos, 1):
        slug = criar_slug(curso)
        readme += f"{idx}. [{curso}](./{idx:02d}-{slug}/)\n"
    
    readme += """

## 📂 Estrutura

Cada curso possui:
- Pasta `src/` para código-fonte e recursos
- Arquivo `README.md` com descrição
- Arquivo `.gitkeep` para manter a pasta no Git

## 🔗 Links Úteis

- [DIO - Digital Innovation One](https://www.dio.me)

---

*Índice gerado automaticamente*
"""
    
    return readme

if __name__ == '__main__':
    main()
