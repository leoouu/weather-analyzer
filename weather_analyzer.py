import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import json
import sys
from matplotlib.ticker import MaxNLocator
import argparse

class WeatherDataAnalyzer:
    def __init__(self):
        self.api_key = "sua_chave_api"  # # chave API do OpenWeatherMap 
        self.base_url = "https://api.openweathermap.org/data/2.5/"
        self.data_dir = "dados_climaticos"
        self.ensure_data_directory_exists()
        
    def ensure_data_directory_exists(self):
        """Cria o diretório de dados se não existir."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            print(f"Diretório '{self.data_dir}' criado com sucesso.")
    
    def obter_dados_clima(self, cidade, dias=5):
        """
        Obtém dados climáticos para uma cidade específica pelos próximos dias.
        Se não conseguir obter os dados online, tentará carregar dados locais.
        """
        try:
            # Primeiro tenta obter dados atuais
            params = {
                'q': cidade,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'pt_br'
            }
            
            # simulacao de dados se não tivermos uma API key válida
            if self.api_key == "sua_chave_api":
                print("Usando dados simulados (nenhuma chave API fornecida)...")
                return self.gerar_dados_simulados(cidade, dias)
            
            # Se tiver uma chave API válida, faça a requisição
            response = requests.get(f"{self.base_url}forecast", params=params)
            
            if response.status_code == 200:
                dados = response.json()
                self.salvar_dados(dados, cidade)
                return self.processar_dados_api(dados, dias)
            else:
                print(f"Erro ao obter dados: {response.status_code}. Tentando carregar dados locais...")
                return self.carregar_dados_locais(cidade)
                
        except Exception as e:
            print(f"Erro ao obter dados climáticos: {e}")
            print("Gerando dados simulados como fallback...")
            return self.gerar_dados_simulados(cidade, dias)
    
    def processar_dados_api(self, dados, dias=5):
        """Processa os dados brutos da API em um DataFrame."""
        previsoes = []
        
        for item in dados['list'][:dias * 8]:  # 8 previsões por dia (a cada 3 horas)
            data = datetime.fromtimestamp(item['dt'])
            previsoes.append({
                'data': data,
                'temperatura': item['main']['temp'],
                'sensacao_termica': item['main']['feels_like'],
                'min': item['main']['temp_min'],
                'max': item['main']['temp_max'],
                'pressao': item['main']['pressure'],
                'umidade': item['main']['humidity'],
                'clima': item['weather'][0]['description'],
                'velocidade_vento': item['wind']['speed']
            })
        
        return pd.DataFrame(previsoes)
    
    def gerar_dados_simulados(self, cidade, dias=5):
        """Gera dados climáticos simulados para demonstração."""
        print(f"Gerando dados simulados para {cidade}...")
        inicio = datetime.now()
        previsoes = []
        
        # Parâmetros base para cada cidade
        parametros_cidade = {
            'São Paulo': {'temp_base': 22, 'var_temp': 5, 'umidade_base': 70},
            'Rio de Janeiro': {'temp_base': 28, 'var_temp': 4, 'umidade_base': 75},
            'Brasília': {'temp_base': 25, 'var_temp': 8, 'umidade_base': 55},
            'Curitiba': {'temp_base': 18, 'var_temp': 7, 'umidade_base': 80},
            'Recife': {'temp_base': 30, 'var_temp': 3, 'umidade_base': 85},
        }
        
        # Usar parâmetros padrão se a cidade não estiver na lista
        params = parametros_cidade.get(cidade, {'temp_base': 25, 'var_temp': 5, 'umidade_base': 65})
        
        # Clima possível
        climas = ['céu limpo', 'nuvens dispersas', 'nuvens quebradas', 'céu nublado', 'chuva leve', 'chuva moderada']
        
        # Gerar dados para cada período de 3 horas
        for i in range(dias * 8):
            data = inicio + timedelta(hours=i*3)
            hora = data.hour
            
            # Variação de temperatura com base na hora do dia
            fator_hora = 1.0
            if 6 <= hora <= 12:  # Manhã - subindo
                fator_hora = 1.1
            elif 12 < hora <= 16:  # Tarde - pico
                fator_hora = 1.2
            elif 16 < hora <= 21:  # Final da tarde - caindo
                fator_hora = 0.9
            else:  # Noite - baixa
                fator_hora = 0.8
            
            # Calcular temperatura com variação aleatória
            import random
            temp_base = params['temp_base'] * fator_hora
            variacao = random.uniform(-params['var_temp']/2, params['var_temp']/2)
            temperatura = temp_base + variacao
            
            # Simular outros valores com base na temperatura
            previsoes.append({
                'data': data,
                'temperatura': round(temperatura, 1),
                'sensacao_termica': round(temperatura * random.uniform(0.95, 1.05), 1),
                'min': round(temperatura - random.uniform(0, 2), 1),
                'max': round(temperatura + random.uniform(0, 2), 1),
                'pressao': round(1013 + random.uniform(-10, 10), 1),
                'umidade': round(params['umidade_base'] + random.uniform(-15, 15), 1),
                'clima': random.choice(climas),
                'velocidade_vento': round(random.uniform(1, 10), 1)
            })
        
        return pd.DataFrame(previsoes)
    
    def salvar_dados(self, dados, cidade):
        """Salva os dados brutos em um arquivo JSON."""
        nome_arquivo = os.path.join(self.data_dir, f"{cidade.lower().replace(' ', '_')}_dados.json")
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        print(f"Dados salvos em {nome_arquivo}")
    
    def carregar_dados_locais(self, cidade):
        """Carrega dados salvos anteriormente."""
        nome_arquivo = os.path.join(self.data_dir, f"{cidade.lower().replace(' ', '_')}_dados.json")
        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
            print(f"Dados carregados do arquivo {nome_arquivo}")
            return self.processar_dados_api(dados)
        except FileNotFoundError:
            print(f"Arquivo {nome_arquivo} não encontrado. Gerando dados simulados...")
            return self.gerar_dados_simulados(cidade)
    
    def gerar_grafico_temperatura(self, df, cidade):
        """Gera um gráfico de linha mostrando a temperatura ao longo do tempo."""
        plt.figure(figsize=(12, 6))
        
        # Plotar temperatura, mínima e máxima
        plt.plot(df['data'], df['temperatura'], 'r-', label='Temperatura')
        plt.plot(df['data'], df['min'], 'b--', alpha=0.7, label='Mínima')
        plt.plot(df['data'], df['max'], 'r--', alpha=0.7, label='Máxima')
        
        # Configurações do gráfico
        plt.title(f'Variação de Temperatura em {cidade}')
        plt.xlabel('Data e Hora')
        plt.ylabel('Temperatura (°C)')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        
        # Melhorar a formatação do eixo x
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Salvar o gráfico
        nome_arquivo = os.path.join(self.data_dir, f"{cidade.lower().replace(' ', '_')}_temperatura.png")
        plt.savefig(nome_arquivo)
        print(f"Gráfico de temperatura salvo em {nome_arquivo}")
        
        plt.close()
    
    def gerar_grafico_umidade(self, df, cidade):
        """Gera um gráfico de linha mostrando a umidade ao longo do tempo."""
        plt.figure(figsize=(12, 6))
        
        # Criar uma área preenchida para a umidade
        plt.fill_between(df['data'], df['umidade'], color='skyblue', alpha=0.4)
        plt.plot(df['data'], df['umidade'], 'b-', label='Umidade')
        
        # Configurações do gráfico
        plt.title(f'Variação de Umidade em {cidade}')
        plt.xlabel('Data e Hora')
        plt.ylabel('Umidade (%)')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.ylim(0, 100)  # A umidade varia de 0 a 100%
        
        # Melhorar a formatação do eixo x
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Salvar o gráfico
        nome_arquivo = os.path.join(self.data_dir, f"{cidade.lower().replace(' ', '_')}_umidade.png")
        plt.savefig(nome_arquivo)
        print(f"Gráfico de umidade salvo em {nome_arquivo}")
        
        plt.close()
    
    def gerar_grafico_clima(self, df, cidade):
        """Gera um gráfico de barras mostrando a frequência dos tipos de clima."""
        contagem_clima = df['clima'].value_counts()
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(contagem_clima.index, contagem_clima.values, color='skyblue')
        
        # Adicionar rótulos em cada barra
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    str(int(height)), ha='center', va='bottom')
        
        # Configurações do gráfico
        plt.title(f'Frequência dos Tipos de Clima em {cidade}')
        plt.xlabel('Tipo de Clima')
        plt.ylabel('Frequência')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Salvar o gráfico
        nome_arquivo = os.path.join(self.data_dir, f"{cidade.lower().replace(' ', '_')}_frequencia_clima.png")
        plt.savefig(nome_arquivo)
        print(f"Gráfico de frequência de clima salvo em {nome_arquivo}")
        
        plt.close()
    
    def gerar_relatorio(self, df, cidade):
        """Gera um relatório estatístico dos dados climáticos."""
        # Criar um relatório básico
        relatorio = {
            'cidade': cidade,
            'periodo': {
                'inicio': df['data'].min().strftime('%d/%m/%Y %H:%M'),
                'fim': df['data'].max().strftime('%d/%m/%Y %H:%M')
            },
            'temperatura': {
                'media': round(df['temperatura'].mean(), 1),
                'minima': round(df['min'].min(), 1),
                'maxima': round(df['max'].max(), 1),
                'variacao': round(df['max'].max() - df['min'].min(), 1)
            },
            'umidade': {
                'media': round(df['umidade'].mean(), 1),
                'minima': round(df['umidade'].min(), 1),
                'maxima': round(df['umidade'].max(), 1)
            },
            'clima_predominante': df['clima'].mode()[0],
            'vento': {
                'velocidade_media': round(df['velocidade_vento'].mean(), 1),
                'maxima': round(df['velocidade_vento'].max(), 1)
            }
        }
        
        # Salvar relatório 
        nome_arquivo = os.path.join(self.data_dir, f"{cidade.lower().replace(' ', '_')}_relatorio.json")
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(relatorio, arquivo, ensure_ascii=False, indent=4)
        print(f"Relatório salvo em {nome_arquivo}")
        
        # Imprimir relatório formatado no console
        print("\n" + "="*50)
        print(f"RELATÓRIO CLIMÁTICO: {cidade.upper()}")
        print("="*50)
        print(f"Período: {relatorio['periodo']['inicio']} a {relatorio['periodo']['fim']}")
        print("\nTEMPERATURA:")
        print(f"  Média: {relatorio['temperatura']['media']}°C")
        print(f"  Mínima: {relatorio['temperatura']['minima']}°C")
        print(f"  Máxima: {relatorio['temperatura']['maxima']}°C")
        print(f"  Variação: {relatorio['temperatura']['variacao']}°C")
        print("\nUMIDADE:")
        print(f"  Média: {relatorio['umidade']['media']}%")
        print(f"  Mínima: {relatorio['umidade']['minima']}%")
        print(f"  Máxima: {relatorio['umidade']['maxima']}%")
        print(f"\nClima predominante: {relatorio['clima_predominante']}")
        print(f"\nVento:")
        print(f"  Velocidade média: {relatorio['vento']['velocidade_media']} km/h")
        print(f"  Velocidade máxima: {relatorio['vento']['maxima']} km/h")
        print("="*50)
        
        return relatorio
    
    def analisar_dados(self, cidade, dias=5, mostrar_graficos=True):
        """Realiza a análise completa dos dados da cidade."""
        print(f"\nAnalisando dados climáticos para {cidade}...")
        
        # Obter os dados
        df = self.obter_dados_clima(cidade, dias)
        
        # Gerar gráficos
        if mostrar_graficos:
            self.gerar_grafico_temperatura(df, cidade)
            self.gerar_grafico_umidade(df, cidade)
            self.gerar_grafico_clima(df, cidade)
        
        # Gerar relatório
        relatorio = self.gerar_relatorio(df, cidade)
        
        return df, relatorio

def main():
    parser = argparse.ArgumentParser(description='Analisador de Dados Climáticos')
    parser.add_argument('cidade', type=str, nargs='?', default='São Paulo', 
                        help='Nome da cidade para análise (padrão: São Paulo)')
    parser.add_argument('--dias', type=int, default=5, 
                        help='Número de dias para analisar (padrão: 5)')
    parser.add_argument('--sem-graficos', action='store_true',
                        help='Não gerar gráficos')
    
    args = parser.parse_args()
    
    # Criar o analisador e executar a análise
    analisador = WeatherDataAnalyzer()
    df, relatorio = analisador.analisar_dados(
        args.cidade, 
        args.dias, 
        not args.sem_graficos
    )
    
    print(f"\nAnálise climática de {args.cidade} concluída com sucesso!")
    print(f"Os arquivos foram salvos no diretório '{analisador.data_dir}'")

if __name__ == "__main__":
    main()