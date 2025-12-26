# Gerador de Estrutura de Cursos

Script Python para extrair módulos e cursos de arquivos HTML da plataforma DIO e gerar automaticamente uma estrutura organizada de diretórios.

## 📋 Descrição

Este projeto analisa o HTML de cursos da plataforma DIO (Digital Innovation One) e cria uma estrutura de diretórios organizada por módulos, com numeração sequencial e nomes convertidos para formato slug (sem acentos, minúsculas, com hífens).

## ✨ Funcionalidades

- ✅ **Parser HTML**: Extrai módulos e cursos do HTML da DIO
- ✅ **Estrutura Modular**: Organiza cursos dentro de seus respectivos módulos
- ✅ **Slug Conversion**: Converte nomes para formato URL-friendly
- ✅ **Numeração Automática**: Numera sequencialmente (01-, 02-, etc.)
- ✅ **README.md Automático**: Gera índice navegável com links
- ✅ **Estrutura Git-Ready**: Inclui .gitkeep para pastas vazias

## 🔧 Pré-requisitos

- Python 3.7 ou superior
- BeautifulSoup4

### Instalação das Dependências

```bash
# Criar ambiente virtual (recomendado)
python -m venv .venv

# Ativar ambiente virtual
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Instalar dependências
pip install beautifulsoup4
```

## 🚀 Como Usar

### 1. Obter o HTML dos Cursos

1. Acesse a página de um bootcamp/trilha na DIO
2. Abra as ferramentas de desenvolvedor (F12)
3. Na aba Elements/Elementos, localize o elemento que contém todos os módulos e cursos
4. Clique com botão direito no elemento → Copy → Copy outerHTML
5. Salve o conteúdo em um arquivo chamado `html_geral.html` na raiz do projeto

### 2. Executar o Script

```bash
# Com ambiente virtual ativado
python processar_html_geral.py

# Ou diretamente com o interpretador do venv
.venv/bin/python processar_html_geral.py
```

### 3. Resultado

O script irá:
1. Analisar o HTML
2. Extrair módulos e cursos
3. Criar a estrutura de diretórios em `cursos/`
4. Gerar READMEs com índices navegáveis

## 📂 Estrutura Gerada

```
cursos/
├── README.md                                    # Índice principal com todos os módulos
├── 01-inteligencia-artificial-sua-aliada.../   # Módulo 1
│   ├── 01-primeiros-passos-da-sua-jornada/
│   │   ├── README.md                           # Descrição do curso
│   │   └── src/                                # Código-fonte
│   │       └── .gitkeep
│   ├── 02-introducao-a-inteligencia-artificial/
│   │   ├── README.md
│   │   └── src/
│   └── ...
├── 02-fundamentos-essenciais-do-java/          # Módulo 2
│   ├── 01-introducao-ao-java-e-seu-ambiente/
│   └── ...
└── ...
```

## 📖 Exemplo de Saída

```
📚 Módulos encontrados: 6
   1. Inteligência Artificial: Sua Aliada na Jornada Java e Cloud (5 cursos)
   2. Fundamentos Essenciais do Desenvolvimento Java (3 cursos)
   3. Programação Orientada a Objetos e Boas Práticas em Java (8 cursos)
   4. Desenvolvimento de APIs REST com Java e Spring Boot (6 cursos)
   5. Preparando Aplicações para a Nuvem com Docker (7 cursos)
   6. Desbravando a Nuvem com AWS (6 cursos)

📖 Total de cursos: 35

🎯 Criando estrutura com 6 módulo(s)...

📁 Módulo 1: Inteligência Artificial: Sua Aliada na Jornada Java e Cloud
   Diretório: 01-inteligencia-artificial-sua-aliada-na-jornada-java-e-cloud
   Total de cursos: 5
   ✓ 1. Primeiros Passos da sua Jornada com Java e Cloud
   ✓ 2. Introdução à Inteligência Artificial
   ...

✅ Estrutura criada com sucesso em: /path/to/cursos
📄 README.md gerado com índice dos módulos/cursos
```

## ⚙️ Personalização

### Alterar Diretório de Saída

Edite a variável `base_dir` na função `main()`:

```python
# Linha ~158 em processar_html_geral.py
base_dir = Path('~/miscelania/cursos')
```

### Alterar Caminho do HTML

Edite a variável `html_file` na função `main()`:

```python
# Linha ~149 em processar_html_geral.py
html_file = Path('~/miscelania/html_geral.html')
```

### Customizar Template do README

Edite a função `criar_estrutura_curso()` (linha ~102) para alterar o template do README.md de cada curso.

## 🔍 Como Funciona

### 1. Parser de Módulos
- Busca buttons com classe `sc-tQeVH foWZJB` (títulos dos módulos)
- Remove sufixo "X atividades"
- Extrai o nome limpo do módulo

### 2. Parser de Cursos
- Para cada módulo, encontra o div seguinte (`sc-gGTSdS`)
- Extrai todos os `h3` com classe `sc-kvaGlN fgSeyi` (títulos dos cursos)
- Associa os cursos ao módulo correto

### 3. Conversão para Slug
- Remove acentos: `Inteligência` → `Inteligencia`
- Converte para minúsculas
- Substitui espaços por hífens
- Remove caracteres especiais
- Resultado: `inteligencia-artificial-sua-aliada-na-jornada-java-e-cloud`

### 4. Geração de Estrutura
- Cria diretórios numerados (01-, 02-, etc.)
- Gera pasta `src/` em cada curso
- Cria `.gitkeep` para versionar pastas vazias
- Gera README.md com descrição e links

## 📝 Arquivos do Projeto

```
.
├── processar_html_geral.py     # Script principal
├── html_geral.html              # HTML de entrada (você cria)
├── README.md                    # Este arquivo
├── parsers/                     # Parsers de referência
│   ├── parser_cursos.py
│   ├── parser_modulos.py
│   └── parser_videos.py
└── cursos/                      # Estrutura gerada (criada pelo script)
    └── README.md
```

## 🐛 Troubleshooting

### Erro: "No module named 'bs4'"
```bash
pip install beautifulsoup4
```

### Erro: "❌ Arquivo html_geral.html não encontrado"
Certifique-se de ter copiado o HTML e salvado como `html_geral.html` na raiz do projeto.

### Estrutura vazia ou incorreta
Verifique se você copiou o HTML correto. O HTML deve conter:
- Buttons com classe `sc-tQeVH foWZJB` (módulos)
- Divs com classe `sc-gGTSdS` (grupos de cursos)
- H3 com classe `sc-kvaGlN fgSeyi` (nomes dos cursos)

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Melhorar a documentação
- Enviar pull requests

## 📄 Licença

Este projeto é de código aberto e está disponível para uso livre.

## 🔗 Links Úteis (e o que estudei)

- [DIO - Digital Innovation One](https://www.dio.me)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Python pathlib](https://docs.python.org/3/library/pathlib.html)

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique a seção de Troubleshooting
2. Revise os exemplos de saída
3. Confirme que as dependências estão instaladas

---

**Desenvolvido com Python e Github Copilot para facilitar a organização de cursos da DIO**
