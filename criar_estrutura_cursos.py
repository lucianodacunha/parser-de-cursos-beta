"""
Cria estrutura de diretórios para cursos
"""

import os
import re
import unicodedata
from pathlib import Path
from bs4 import BeautifulSoup


def extrair_modulos_do_html(html):
    """
    Extrai os nomes dos módulos do HTML seguindo o padrão do parser_modulos.py
    """
    soup = BeautifulSoup(html, "html.parser")
    modulos = []
    for buttons in soup.select("div.sc-fJKILO"):
        for button in buttons:
            texto = button.get_text(strip=True)
            # Remove a parte "X atividades" do final usando regex
            import re
            # Remove dígitos seguidos de "atividades" no final
            texto_limpo = re.sub(r'\d+\s*atividades$', '', texto).strip()
            if texto_limpo:
                modulos.append(texto_limpo)
    return modulos


def extrair_cursos_do_html(html):
    """
    Extrai os nomes dos cursos do HTML seguindo o padrão do parser_cursos.py
    """
    soup = BeautifulSoup(html, "html.parser")
    titulos = [
        h3.get_text(strip=True)
        for h3 in soup.select("h3.sc-kvaGlN.fgSeyi")
    ]
    return titulos


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


def main(lista_htmls=None, html_modulos=None):
    """
    Extrai os nomes dos cursos de uma lista de HTMLs e cria a estrutura de diretórios.
    Cada HTML gera seus cursos em uma pasta separada.
    
    Args:
        lista_htmls: Lista de strings HTML com cursos. Se None, usa um HTML de exemplo.
        html_modulos: String HTML com módulos/grupos. Se fornecido, usa os nomes dos módulos
                      como nomes das pastas. Se None, usa "grupo-01", "grupo-02", etc.
    """
    # Se não for fornecida uma lista de HTMLs, usa um exemplo
    if lista_htmls is None:
        lista_htmls = [
            """
            <div class="sc-gGTSdS kovLrV"><button id="btn-track-next-path" color="#E4105D" class="sc-hcFBEE fNJoXp"><div class="sc-jIxBFl cYhStf"><img src="https://assets.dio.me/Kevd3DGFNY-Qa0XR2GjyA9ML57MD5sjOo0s7sbSwTj0/f:webp/h:77/q:80/w:77/L2NvdXJzZXMvYmFkZ2UvYzBhNmNmZDEtMjc2OS00NDYzLTkyOTktOThhNGQ1ODJhNDNkLnBuZw" alt="Imagem do bootcamp Conhecendo e Instalando o Docker" class="sc-xfJVh gcAVju"><div class="sc-cbZHsQ fJXoQu"><span class="sc-kNxgZW iziYID">Curso</span><h3 class="sc-kvaGlN fgSeyi">Conhecendo e Instalando o Docker</h3><div class="sc-hRcwtX bHnmge"><div class="sc-heNFcO ldyhSD"><span class="sc-iYRRFf ecZhbb"><i style="font-size: 15px; color: rgb(228, 16, 93); font-family: MaterialCommunityIcons; font-weight: normal; font-style: normal;"></i> Intermediário</span><span class="sc-iYRRFf ecZhbb"><i style="font-size: 15px; color: rgb(250, 250, 250); font-family: MaterialCommunityIcons; font-weight: normal; font-style: normal;">肋</i>1 hrs</span></div></div></div></div><div class="sc-fWKdJz fOXidg"><div class="sc-jiDjCn eNrccF"><button color="#E4105D" class="sc-iTeOpy hogpuy">Iniciar agora<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 1024 1024" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M869 487.8L491.2 159.9c-2.9-2.5-6.6-3.9-10.5-3.9h-88.5c-7.4 0-10.8 9.2-5.2 14l350.2 304H152c-4.4 0-8 3.6-8 8v60c0 4.4 3.6 8 8 8h585.1L386.9 854c-5.6 4.9-2.2 14 5.2 14h91.5c1.9 0 3.8-.7 5.2-2L869 536.2a32.07 32.07 0 0 0 0-48.4z"></path></svg></button></div></div></button><button id="btn-track-next-path" color="#E4105D" class="sc-hcFBEE fNJoXp"><div class="sc-jIxBFl cYhStf"><img src="https://assets.dio.me/SUw12iq-ZuFgfPvGg0k8OVMqB9GXOSNm_-EJYRKDD5o/f:webp/h:77/q:80/w:77/L2NvdXJzZXMvYmFkZ2UvZjIxYTY5MDgtZmIyNC00OTFmLWE3ZTctMWMwYjJmM2E5ZGE0LnBuZw" alt="Imagem do bootcamp Primeiros Passos com o Docker" class="sc-xfJVh gcAVju"><div class="sc-cbZHsQ fJXoQu"><span class="sc-kNxgZW iziYID">Curso</span><h3 class="sc-kvaGlN fgSeyi">Primeiros Passos com o Docker</h3><div class="sc-hRcwtX bHnmge"><div class="sc-heNFcO ldyhSD"><span class="sc-iYRRFf ecZhbb"><i style="font-size: 15px; color: rgb(228, 16, 93); font-family: MaterialCommunityIcons; font-weight: normal; font-style: normal;"></i> Avançado</span><span class="sc-iYRRFf ecZhbb"><i style="font-size: 15px; color: rgb(250, 250, 250); font-family: MaterialCommunityIcons; font-weight: normal; font-style: normal;">肋</i>1 hrs</span></div></div></div></div><div class="sc-fWKdJz fOXidg"><div class="sc-jiDjCn eNrccF"><button color="#E4105D" class="sc-iTeOpy hogpuy">Iniciar agora<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 1024 1024" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M869 487.8L491.2 159.9c-2.9-2.5-6.6-3.9-10.5-3.9h-88.5c-7.4 0-10.8 9.2-5.2 14l350.2 304H152c-4.4 0-8 3.6-8 8v60c0 4.4 3.6 8 8 8h585.1L386.9 854c-5.6 4.9-2.2 14 5.2 14h91.5c1.9 0 3.8-.7 5.2-2L869 536.2a32.07 32.07 0 0 0 0-48.4z"></path></svg></button></div></div></button><button id="btn-track-next-path" color="#E4105D" class="sc-hcFBEE fNJoXp"><div class="sc-jIxBFl cYhStf"><img src="https://assets.dio.me/O47KYMnlPSa8TUsedminlgCwpBVc2Q7zOu60IpLtLv0/f:webp/h:77/q:80/w:77/L2NvdXJzZXMvYmFkZ2UvYmY2ZmY0NTYtNGI2Ni00YWNiLWE1NDAtOTgxYTM2YjgwMzM1LnBuZw" alt="Imagem do bootcamp Armazenamento de Dados com Docker" class="sc-xfJVh gcAVju"><div class="sc-cbZHsQ fJXoQu"><span class="sc-kNxgZW iziYID">Curso</span><h3 class="sc-kvaGlN fgSeyi">Armazenamento de Dados com Docker</h3><div class="sc-hRcwtX bHnmge"><div class="sc-heNFcO ldyhSD"><span class="sc-iYRRFf ecZhbb"><i style="font-size: 15px; color: rgb(228, 16, 93); font-family: MaterialCommunityIcons; font-weight: normal; font-style: normal;"></i> Avançado</span><span class="sc-iYRRFf ecZhbb"><i style="font-size: 15px; color: rgb(250, 250, 250); font-family: MaterialCommunityIcons; font-weight: normal; font-style: normal;">肋</i>1 hrs</span></div></div></div></div><div class="sc-fWKdJz fOXidg"><div class="sc-jiDjCn eNrccF"><button color="#E4105D" class="sc-iTeOpy hogpuy">Iniciar agora<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 1024 1024" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M869 487.8L491.2 159.9c-2.9-2.5-6.6-3.9-10.5-3.9h-88.5c-7.4 0-10.8 9.2-5.2 14l350.2 304H152c-4.4 0-8 3.6-8 8v60c0 4.4 3.6 8 8 8h585.1L386.9 854c-5.6 4.9-2.2 14 5.2 14h91.5c1.9 0 3.8-.7 5.2-2L869 536.2a32.07 32.07 0 0 0 0-48.4z"></path></svg></button></div></div></button><button id="btn-track-next-path" color="#E4105D" class="sc-hcFBEE fNJoXp"><div class="sc-jIxBFl cYhStf"><img src="https://assets.dio.me/2uSWWaxqCaREGuk_ip_pl5md3ytzdFNXIIlXfqrJqHQ/f:webp/h:77/q:80/w:77/L2NvdXJzZXMvYmFkZ2UvYWVkMzA1YzAtMmZkMi00MDg5LWIxOWEtZGRmYWUxNGY3ZDRhLnBuZw" alt="Imagem do bootcamp Processamento, Logs e Rede com Docker" class="sc-xfJVh gcAVju"><div class="sc-cbZHsQ fJXoQu"><span class="sc-kNxgZW iziYID">Curso</span><h3 class="sc-kvaGlN fgSeyi">Processamento, Logs e Rede com Docker</h3><div class="sc-hRcwtX bHnmge"><div class="sc-heNFcO ldyhSD"><span class="sc-iYRRFf ecZhbb"><i style="font-size: 15px; color: rgb(228, 16, 93); font-family: MaterialCommunityIcons; font-weight: normal; font-style: normal;"></i> Avançado</span><span class="sc-iYRRFf ecZhbb"><i style="font-size: 15px; color: rgb(250, 250, 250); font-family: MaterialCommunityIcons; font-weight: normal; font-style: normal;">肋</i>1 hrs</span></div></div></div></div><div class="sc-fWKdJz fOXidg"><div class="sc-jiDjCn eNrccF"><button color="#E4105D" class="sc-iTeOpy hogpuy">Iniciar agora<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 1024 1024" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M869 487.8L491.2 159.9c-2.9-2.5-6.6-3.9-10.5-3.9h-88.5c-7.4 0-10.8 9.2-5.2 14l350.2 304H152c-4.4 0-8 3.6-8 8v60c0 4.4 3.6 8 8 8h585.1L386.9 854c-5.6 4.9-2.2 14 5.2 14h91.5c1.9 0 3.8-.7 5.2-2L869 536.2a32.07 32.07 0 0 0 0-48.4z"></path></svg></button></div></div></button><button id="btn-track-next-path" color="#E4105D" class="sc-hcFBEE fNJoXp"><div class="sc-jIxBFl cYhStf"><img src="https://assets.dio.me/o3JGdLnzuvnM5mPo-azk9YgWlg-ZyatPFJ2nZyQvSBQ/f:webp/h:77/q:80/w:77/L2NvdXJzZXMvYmFkZ2UvNDlhNDQxMjctMTNhNi00YjMxLWFjOTAtMzA1MzA4ZmM5ZGQzLnBuZw" alt="Imagem do bootcamp Definição e Criação de um Docker File" class="sc-xfJVh gcAVju"><div class="sc-cbZHsQ fJXoQu"><span class="sc-kNxgZW iziYID">Curso</span><h3 class="sc-kvaGlN fgSeyi">Definição e Criação de um Docker File</h3><div class="sc-hRcwtX bHnmge"><div class="sc-heNFcO ldyhSD"><span class="sc-iYRRFf ecZhbb"><i style="font-size: 15px; color: rgb(228, 16, 93); font-family: MaterialCommunityIcons; font-weight: normal; font-style: normal;"></i> Avançado</span><span class="sc-iYRRFf ecZhbb"><i style="font-size: 15px; color: rgb(250, 250, 250); font-family: MaterialCommunityIcons; font-weight: normal; font-style: normal;">肋</i>1 hrs</span></div></div></div></div><div class="sc-fWKdJz fOXidg"><div class="sc-jiDjCn eNrccF"><button color="#E4105D" class="sc-iTeOpy hogpuy">Iniciar agora<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 1024 1024" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M869 487.8L491.2 159.9c-2.9-2.5-6.6-3.9-10.5-3.9h-88.5c-7.4 0-10.8 9.2-5.2 14l350.2 304H152c-4.4 0-8 3.6-8 8v60c0 4.4 3.6 8 8 8h585.1L386.9 854c-5.6 4.9-2.2 14 5.2 14h91.5c1.9 0 3.8-.7 5.2-2L869 536.2a32.07 32.07 0 0 0 0-48.4z"></path></svg></button></div></div></button><button id="btn-track-next-path" color="#E4105D" class="sc-hcFBEE fNJoXp"><div class="sc-jIxBFl cYhStf"><img src="https://assets.dio.me/NVlQDAv761XQURjzyGxj4JkMPujedqxwjKUgqY4GX88/f:webp/h:77/q:80/w:77/L2NvdXJzZXMvYmFkZ2UvYWM3MjhjZDYtOTRhOC00OTlkLTgxYTctNGEwYTgyODdlNGRkLnBuZw" alt="Imagem do bootcamp Trabalhando com Docker Compose" class="sc-xfJVh gcAVju"><div class="sc-cbZHsQ fJXoQu"><span class="sc-kNxgZW iziYID">Curso</span><h3 class="sc-kvaGlN fgSeyi">Trabalhando com Docker Compose</h3><div class="sc-hRcwtX bHnmge"><div class="sc-heNFcO ldyhSD"><span class="sc-iYRRFf ecZhbb"><i style="font-size: 15px; color: rgb(228, 16, 93); font-family: MaterialCommunityIcons; font-weight: normal; font-style: normal;"></i> Avançado</span><span class="sc-iYRRFf ecZhbb"><i style="font-size: 15px; color: rgb(250, 250, 250); font-family: MaterialCommunityIcons; font-weight: normal; font-style: normal;">肋</i>1 hrs</span></div></div></div></div><div class="sc-fWKdJz fOXidg"><div class="sc-jiDjCn eNrccF"><button color="#E4105D" class="sc-iTeOpy hogpuy">Iniciar agora<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 1024 1024" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M869 487.8L491.2 159.9c-2.9-2.5-6.6-3.9-10.5-3.9h-88.5c-7.4 0-10.8 9.2-5.2 14l350.2 304H152c-4.4 0-8 3.6-8 8v60c0 4.4 3.6 8 8 8h585.1L386.9 854c-5.6 4.9-2.2 14 5.2 14h91.5c1.9 0 3.8-.7 5.2-2L869 536.2a32.07 32.07 0 0 0 0-48.4z"></path></svg></button></div></div></button><button id="btn-track-next-path" color="#E4105D" class="sc-hcFBEE fNJoXp"><div class="sc-jIxBFl cYhStf"><img src="https://assets.dio.me/FlKBrsEFLzihrpBdVhLdK_N_MIG4ydVfXjCKkE0Jimc/f:webp/h:77/q:80/w:77/L2xhYl9wcm9qZWN0cy9iYWRnZXMvMTVhNjdiYTItOGExNi00NWI2LTlhMjgtMmRlMGI4NGFiODYyLnBuZw" alt="Imagem do bootcamp Docker: Utilização Prática no Cenário de Microsserviços" class="sc-xfJVh gcAVju"><div class="sc-cbZHsQ fJXoQu"><span class="sc-kNxgZW iziYID">Desafio de projeto</span><h3 class="sc-kvaGlN fgSeyi">Docker: Utilização Prática no Cenário de Microsserviços</h3><div class="sc-hRcwtX bHnmge"><div class="sc-heNFcO ldyhSD"><span class="sc-iYRRFf ecZhbb"><i style="font-size: 15px; color: rgb(228, 16, 93); font-family: MaterialCommunityIcons; font-weight: normal; font-style: normal;"></i> Avançado</span><span class="sc-iYRRFf ecZhbb"><i style="font-size: 15px; color: rgb(250, 250, 250); font-family: MaterialCommunityIcons; font-weight: normal; font-style: normal;">肋</i>1 hrs</span></div></div></div></div><div class="sc-fWKdJz fOXidg"><div class="sc-jiDjCn eNrccF"><button color="#E4105D" class="sc-iTeOpy hogpuy">Iniciar agora<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 1024 1024" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M869 487.8L491.2 159.9c-2.9-2.5-6.6-3.9-10.5-3.9h-88.5c-7.4 0-10.8 9.2-5.2 14l350.2 304H152c-4.4 0-8 3.6-8 8v60c0 4.4 3.6 8 8 8h585.1L386.9 854c-5.6 4.9-2.2 14 5.2 14h91.5c1.9 0 3.8-.7 5.2-2L869 536.2a32.07 32.07 0 0 0 0-48.4z"></path></svg></button></div></div></button></div>
            """
        ]
    
    # Extrai nomes dos módulos se fornecido
    nomes_modulos = []
    if html_modulos:
        nomes_modulos = extrair_modulos_do_html(html_modulos)
        print(f"\n📚 Processando {len(lista_htmls)} HTML(s) com {len(nomes_modulos)} módulo(s) definido(s)\n")
    else:
        print(f"\n📚 Processando {len(lista_htmls)} HTML(s)\n")
    
    print("=" * 60)
    
    # Processa cada HTML separadamente, criando uma pasta para cada grupo
    for idx_grupo, html in enumerate(lista_htmls, 1):
        cursos = extrair_cursos_do_html(html)
        
        if not cursos:
            print(f"\n⚠️  Grupo {idx_grupo}: Nenhum curso encontrado, pulando...")
            continue
        
        # Define o nome do grupo
        if nomes_modulos and idx_grupo <= len(nomes_modulos):
            nome_grupo = criar_slug(nomes_modulos[idx_grupo - 1])
            diretorio_grupo = f"cursos/{idx_grupo:02d}-{nome_grupo}"
            print(f"\n📂 Módulo {idx_grupo}: {nomes_modulos[idx_grupo - 1]}")
        else:
            diretorio_grupo = f"cursos/grupo-{idx_grupo:02d}"
            print(f"\n📂 Grupo {idx_grupo}")
        
        print(f"   {len(cursos)} curso(s) encontrado(s)")
        print("-" * 60)
        
        # Cria a estrutura para cada curso deste grupo
        for i, curso in enumerate(cursos, 1):
            print(f"[{i}/{len(cursos)}] Criando: {curso}")
            criar_estrutura_curso(curso, i, diretorio_base=diretorio_grupo)
    
    print("\n" + "=" * 60)
    print("✅ Estrutura de diretórios criada com sucesso!")
    print(f"📂 Diretório base: cursos/")


if __name__ == "__main__":
    # Exemplo 1: Executar com HTML padrão
    main()
    
    # Exemplo 2: Executar com múltiplos HTMLs
    # html1 = """<seu html aqui>"""
    # html2 = """<outro html aqui>"""
    # main(lista_htmls=[html1, html2])
