import streamlit as os
import streamlit as st
import yt_dlp
import os
import glob

st.set_page_config(page_title="YT Audio Downloader", page_icon="🎵", layout="centered")

st.title("🎵 YouTube Audio Downloader")
st.write("Pega el enlace de YouTube para extraer el audio en formato MP3.")

# Campo de texto para la URL
url = st.text_input("Enlace del video de YouTube:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    if "youtube.com" in url or "youtu.be" in url:
        st.info("Procesando el enlace... Espera un momento.")
        
        # Carpeta temporal para guardar la descarga antes de pasarla al usuario
        output_dir = "downloads"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Configuración de yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True
        }
        
        try:
            # Descargar y convertir en el servidor
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                # Cambiar la extensión en el nombre del archivo esperado a mp3
                mp3_filename = os.path.splitext(filename)[0] + ".mp3"
            
            # Verificar que el archivo realmente existe
            if os.path.exists(mp3_filename):
                st.success(f"¡Listo! Audio procesado: **{info.get('title')}**")
                
                # Leer el archivo en memoria para el botón de descarga de Streamlit
                with open(mp3_filename, "rb") as file:
                    audio_bytes = file.read()
                
                # Botón nativo de descarga de Streamlit
                st.download_button(
                    label="📥 Guardar MP3 en mi equipo",
                    data=audio_bytes,
                    file_name=os.path.basename(mp3_filename),
                    mime="audio/mp3"
                )
                
                # Limpieza: Borrar el archivo del servidor local después de prepararlo
                os.remove(mp3_filename)
                
        except Exception as e:
            st.error(f"Ocurrió un error al procesar el video: {e}")
    else:
        st.error("Por favor, ingresa una URL válida de YouTube.")
