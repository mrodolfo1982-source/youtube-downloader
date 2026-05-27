import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YT Downloader", page_icon="🎬", layout="centered")

st.title("🎬 YouTube Video & Audio Downloader")
st.write("Pega el enlace de YouTube y selecciona el formato que prefieras.")

# Campo de texto para la URL
url = st.text_input("Enlace de YouTube:", placeholder="https://www.youtube.com/watch?v=...")

# Selector de formato
formato = st.radio(
    "¿Qué deseas descargar?",
    ["🎵 Solo Audio (MP3)", "📺 Video Completo (MP4)"],
    index=0,
    horizontal=True
)

if url:
    if "youtube.com" in url or "youtu.be" in url:
        st.info("Procesando el enlace... Esto puede tomar unos segundos.")
        
        output_dir = "downloads"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Configuración base de yt-dlp
        if "🎵 Solo Audio" in formato:
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
            extension_final = ".mp3"
            mime_type = "audio/mp3"
        else:
            # Configuración para descargar Video en MP4 (combinando video y audio)
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
                'quiet': True
            }
            extension_final = ".mp4"
            mime_type = "video/mp4"
        
        try:
            # Descargar y procesar en el servidor de Streamlit
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                # Asegurar el nombre correcto con la extensión final esperada
                archivo_final = os.path.splitext(filename)[0] + extension_final
            
            # Verificar que el archivo se generó correctamente
            if os.path.exists(archivo_final):
                st.success(f"¡Procesado con éxito!: **{info.get('title')}**")
                
                # Leer el archivo para habilitar la descarga en el navegador del usuario
                with open(archivo_final, "rb") as file:
                    bytes_data = file.read()
                
                st.download_button(
                    label=f"📥 Guardar archivo {extension_final.upper()}",
                    data=bytes_data,
                    file_name=os.path.basename(archivo_final),
                    mime=mime_type
                )
                
                # Limpiar el servidor borrando el archivo temporal
                os.remove(archivo_final)
                
        except Exception as e:
            st.error(f"Ocurrió un error al procesar el archivo: {e}")
    else:
        st.error("Por favor, ingresa una URL válida de YouTube.")
