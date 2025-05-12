# 🌦️ Analisador de Dados Climáticos

Um aplicativo Python para coleta, visualização e análise de dados climáticos de diferentes cidades. Este projeto demonstra habilidades em processamento de dados, visualização e desenvolvimento de aplicativos de linha de comando em Python.

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Requisitos](#-requisitos)
- [Instalação e Uso](#-instalação-e-uso)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Como Contribuir](#-como-contribuir)

## ✨ Funcionalidades

- **🌐 Coleta de Dados**
  - Integração com a API OpenWeatherMap
  - Geração de dados simulados para demonstração
  - Armazenamento local dos dados em formato JSON

- **📊 Visualização de Dados**
  - Gráficos de temperatura (atual, mínima e máxima)
  - Gráficos de umidade
  - Análise de frequência das condições climáticas

- **📝 Análise Estatística**
  - Cálculo de médias, mínimas e máximas
  - Geração de relatórios detalhados
  - Identificação de padrões climáticos

- **⚙️ Recursos Adicionais**
  - Interface de linha de comando intuitiva
  - Tratamento robusto de erros
  - Sistema de cache para reduzir chamadas à API


## 🛠️ Tecnologias Utilizadas

- **Python 3.8+** - Linguagem de programação principal
- **Pandas** - Manipulação e análise de dados
- **Matplotlib** - Criação de visualizações e gráficos
- **Requests** - Integração com APIs
- **JSON** - Armazenamento e manipulação de dados

## 📋 Requisitos

- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)
- Bibliotecas necessárias listadas em `requirements.txt`

## 🚀 Instalação e Uso

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/analisador-clima.git
cd analisador-clima
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure a API (opcional)
Para usar dados reais ao invés de simulados, obtenha uma chave de API gratuita no [OpenWeatherMap](https://openweathermap.org/api) e substitua o valor de `api_key` no arquivo `weather_analyzer.py`.

### 4. Execute o programa
```bash
python weather_analyzer.py "São Paulo"
```

### Argumentos disponíveis:
- **cidade**: Nome da cidade para análise (padrão: São Paulo)
- **--dias**: Número de dias para analisar (padrão: 5)
- **--sem-graficos**: Não gerar gráficos

### Exemplos:
```bash
# Analisar o clima de Recife pelos próximos 3 dias
python weather_analyzer.py "Recife" --dias 3

# Analisar o clima do Rio de Janeiro sem gerar gráficos
python weather_analyzer.py "Rio de Janeiro" --sem-graficos
```

## 📁 Estrutura do Projeto

```
analisador-clima/
├── weather_analyzer.py   # Arquivo principal do programa
├── requirements.txt      # Dependências do projeto
├── dados_climaticos/     # Diretório com dados e gráficos gerados
└── README.md             # Este arquivo
```

## 📝 Como Contribuir

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das suas alterações (`git commit -am 'Adiciona nova funcionalidade'`)
4. Faça push para a branch (`git push origin feature/nova-funcionalidade`)
5. Crie um novo Pull Request

### Ideias para contribuição:
- Interface gráfica com Tkinter, PyQt ou Flask
- Mais tipos de visualizações e análises
- Suporte para mais APIs de clima
- Implementação de algoritmos de machine learning para previsão


---

Desenvolvido por Leonardo (https://github.com/leoouu)
