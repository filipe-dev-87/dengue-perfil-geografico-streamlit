import streamlit as st
import pandas as pd
import numpy as np
import folium
from sklearn.neighbors import KernelDensity
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium

# Configuração da página
st.set_page_config(
    page_title="Geo-Perfis de Dengue (KDE)",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🦟 Geo-Perfis de Dengue (Geographic Profiling)")
st.markdown("""
Esta aplicação utiliza o **Kernel Density Estimation (KDE)** para identificar as áreas de maior concentração de casos de dengue a partir de um arquivo CSV.
""")

# ------------------------------------------------
# 1. UPLOAD DO ARQUIVO CSV
# ------------------------------------------------
uploaded_file = st.file_uploader(
    "**1. Faça o upload do arquivo 'casos_dengue.csv'**",
    type="csv",
    help="O arquivo deve conter as colunas 'latitude' e 'longitude'."
)

if uploaded_file is not None:
    try:
        # Lê o arquivo enviado
        df = pd.read_csv(uploaded_file)
        st.success(f"Arquivo '{uploaded_file.name}' carregado com sucesso! {len(df)} registros encontrados.")
        
        # Validação das colunas
        required_cols = ['latitude', 'longitude']
        if not all(col in df.columns for col in required_cols):
            st.error(f"O arquivo CSV deve conter as colunas: {', '.join(required_cols)}")
            st.stop()

        # Limpeza e preparação dos dados
        df = df.dropna(subset=required_cols)
        coords = df[['latitude', 'longitude']].to_numpy()

        if len(coords) < 2:
            st.warning("É necessário pelo menos 2 pontos de dados válidos para a análise.")
            st.stop()

        st.subheader("Prévia dos Dados")
        st.dataframe(df.head())

        # ------------------------------------------------
        # 2. AJUSTE DO KERNEL DENSITY ESTIMATION (KDE)
        # ------------------------------------------------
        st.subheader("2. Análise de Densidade (KDE)")
        
        # Parâmetro de banda (Bandwidth) ajustável pelo usuário
        bandwidth = st.slider(
            "Ajuste a Banda (Bandwidth) do KDE:",
            min_value=0.0005,
            max_value=0.01,
            value=0.002,
            step=0.0005,
            format="%.4f",
            help="Controla o nível de suavização. Valores menores resultam em focos mais pontuais."
        )

        @st.cache_data(show_spinner="Calculando KDE e focos prováveis...")
        def calculate_kde(coords, bandwidth):
            """Calcula o KDE e identifica os 5 focos de maior densidade."""
            kde = KernelDensity(bandwidth=bandwidth, kernel='gaussian')
            kde.fit(coords)
            
            # Gera uma grade de pontos na região dos casos
            lat_min, lat_max = coords[:,0].min() - 0.005, coords[:,0].max() + 0.005
            lon_min, lon_max = coords[:,1].min() - 0.005, coords[:,1].max() + 0.005
            
            # Grade de 100x100 pontos
            grid_lat, grid_lon = np.mgrid[lat_min:lat_max:100j, lon_min:lon_max:100j]
            grid_points = np.vstack([grid_lat.ravel(), grid_lon.ravel()]).T
            
            # Calcula densidade de probabilidade
            log_dens = kde.score_samples(grid_points)
            dens = np.exp(log_dens)
            
            # Top 5 focos mais prováveis
            indices_top5 = np.argsort(dens)[-5:][::-1]
            top5_coords = grid_points[indices_top5]
            
            return top5_coords, coords

        top5_coords, coords = calculate_kde(coords, bandwidth)

        # ------------------------------------------------
        # 3. BUSCA DE ENDEREÇOS (GEOCODIFICAÇÃO REVERSA)
        # ------------------------------------------------
        st.subheader("3. Geocodificação Reversa dos Focos")

        @st.cache_data(show_spinner="Buscando endereços dos focos (pode levar alguns segundos)...")
        def reverse_geocode(top5_coords):
            """Realiza a geocodificação reversa para os 5 focos."""
            geolocator = Nominatim(user_agent="geo_dengue_model_streamlit")
            enderecos = []
            for lat, lon in top5_coords:
                try:
                    # Adiciona um timeout para evitar travamentos
                    location = geolocator.reverse((lat, lon), timeout=10)
                    endereco = location.address if location else "Endereço não encontrado"
                except Exception as e:
                    endereco = f"Erro na geocodificação: {e}"
                enderecos.append(endereco)
            return enderecos

        enderecos = reverse_geocode(top5_coords)

        # Mostra ranking
        st.markdown("**Top 5 locais mais prováveis de foco:**")
        focos_data = []
        for i, (lat, lon, end) in enumerate(zip(top5_coords[:,0], top5_coords[:,1], enderecos), 1):
            focos_data.append({
                "Foco": i,
                "Latitude": f"{lat:.6f}",
                "Longitude": f"{lon:.6f}",
                "Endereço Aproximado": end
            })
        
        st.table(pd.DataFrame(focos_data).set_index("Foco"))

        # ------------------------------------------------
        # 4. GERA MAPA INTERATIVO COM FOLIUM
        # ------------------------------------------------
        st.subheader("4. Visualização no Mapa Interativo")

        # Ponto central do mapa
        map_center = [coords[:,0].mean(), coords[:,1].mean()]
        m = folium.Map(location=map_center, zoom_start=14)

        # Marcadores dos casos confirmados
        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=3, color='red', fill=True, fill_opacity=0.6,
                tooltip=f"Caso confirmado"
            ).add_to(m)

        # Marcadores dos focos prováveis
        for i, (lat, lon, end) in enumerate(zip(top5_coords[:,0], top5_coords[:,1], enderecos), 1):
            folium.Marker(
                [lat, lon],
                popup=f"Foco {i}: {end}",
                tooltip=f"Foco {i}",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)

        # Exibe o mapa no Streamlit
        st_folium(m, width=1200, height=600)

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
        st.stop()

else:
    st.info("Aguardando o upload do arquivo CSV para iniciar a análise.")
