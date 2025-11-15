# 🦟 Geo-Perfis de Dengue (Geographic Profiling)

Este projeto é uma aplicação web interativa construída com **Streamlit** para realizar o perfilamento geográfico (Geographic Profiling) de casos de dengue. Ele utiliza o método **Kernel Density Estimation (KDE)** para identificar as áreas de maior concentração e risco de foco da doença a partir de dados de latitude e longitude.

## 🌟 Funcionalidades

*   **Upload de Dados:** Permite o upload de um arquivo CSV contendo os registros de casos.
*   **Análise KDE:** Aplica o Kernel Density Estimation para calcular a densidade de casos.
*   **Ajuste Interativo:** Slider para ajustar o parâmetro **Bandwidth** do KDE, permitindo refinar a suavização e a precisão dos focos.
*   **Geocodificação Reversa:** Utiliza o Nominatim (OpenStreetMap) para buscar o endereço aproximado dos 5 focos de maior densidade.
*   **Visualização Interativa:** Exibe os casos confirmados e os 5 focos prováveis em um mapa interativo (Folium).

## 🚀 Como Rodar Localmente

Para rodar esta aplicação em sua máquina local, siga os passos abaixo:

### 1. Pré-requisitos

Certifique-se de ter o Python instalado (versão 3.8+).

### 2. Instalação das Dependências

Crie um ambiente virtual (opcional, mas recomendado) e instale as bibliotecas necessárias usando o arquivo `requirements.txt`:

# Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # No Linux/macOS
# venv\Scripts\activate   # No Windows

# Instale as dependências
pip install -r requirements.txt

### 3. Execução da Aplicação

Execute o script principal usando o Streamlit:

streamlit run app.py

A aplicação será aberta automaticamente no seu navegador padrão.

## ☁️ Implantação no Streamlit Cloud

O projeto está pronto para ser implantado diretamente no Streamlit Cloud.

1.  **Crie um Repositório Git:** Adicione os arquivos `app.py` e `requirements.txt` a um repositório no GitHub.
2.  **Acesse o Streamlit Cloud:** Conecte sua conta e clique em **"New app"**.
3.  **Configure a Implantação:**
    *   **Repository:** Selecione o repositório criado.
    *   **Branch:** Selecione o branch principal (ex: `main`).
    *   **Main file path:** `app.py`
4.  Clique em **"Deploy!"**.

O Streamlit Cloud irá instalar as dependências listadas em `requirements.txt` e iniciar a aplicação.

## 💾 Formato do Arquivo de Entrada

A aplicação espera um arquivo CSV com, no mínimo, as seguintes colunas:

| Coluna | Tipo de Dado | Descrição |
| :--- | :--- | :--- |
| `latitude` | Float | Latitude do caso de dengue. |
| `longitude` | Float | Longitude do caso de dengue. |
| `id` (Opcional) | Qualquer | Identificador único do caso. |

**Exemplo de `casos_dengue.csv`:**

id,latitude,longitude
1, -23.5505, -46.6333
2, -23.5510, -46.6340
3, -23.5550, -46.6300
...

## 📦 Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt`:

streamlit
pandas
numpy
folium
geopy
scikit-learn
streamlit-folium

## 📌 Observações
Este projeto é voltado para análise espacial e prevenção, não substitui medidas oficiais de saúde pública.

Recomenda-se uso com datasets pequenos ou médios devido às limitações da API do Nominatim.

## 📄 Licença
Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para mais informações.