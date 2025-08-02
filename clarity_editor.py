
import streamlit as st
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip

st.set_page_config(page_title="Clarity Editor MVP", layout="centered")
st.title("🎬 Clarity Editor MVP")

st.markdown("""
Upload your clarity content, add voice/music, overlay text or avatars, and export for any social platform.
""")

video_file = st.file_uploader("Upload your main video (mp4)", type=["mp4"])
audio_file = st.file_uploader("Upload background music or voiceover (mp3)", type=["mp3"])
subtitle_text = st.text_area("Enter subtitle or clarity quote (optional)")
avatar_image = st.file_uploader("Upload avatar image overlay (png/jpg, optional)", type=["png", "jpg"])

preset = st.radio("Choose export preset:", [
    "TikTok (9:16)", "Instagram Reel", "YouTube (16:9)", "WhatsApp Status", "Clarity Kit (.zip)"
])

if st.button("🚀 Generate Export"):
    if not video_file:
        st.warning("Please upload a video file first.")
    else:
        with st.spinner("Processing video..."):
            video_path = "temp_video.mp4"
            with open(video_path, "wb") as f:
                f.write(video_file.read())

            video_clip = VideoFileClip(video_path)

            if preset in ["TikTok (9:16)", "Instagram Reel", "WhatsApp Status"]:
                final_clip = video_clip.resize(height=1920).crop(x_center=video_clip.w/2, width=1080)
            elif preset == "YouTube (16:9)":
                final_clip = video_clip.resize(width=1920)
            else:
                final_clip = video_clip

            if audio_file:
                audio_path = "temp_audio.mp3"
                with open(audio_path, "wb") as f:
                    f.write(audio_file.read())
                audio_clip = AudioFileClip(audio_path).set_duration(final_clip.duration)
                final_clip = final_clip.set_audio(audio_clip)

            if subtitle_text:
                txt_clip = TextClip(subtitle_text, fontsize=48, color='white', bg_color='black')
                txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(final_clip.duration)
                final_clip = CompositeVideoClip([final_clip, txt_clip])

            export_path = "exported_video.mp4"
            final_clip.write_videofile(export_path, codec="libx264")

            with open(export_path, "rb") as f:
                st.download_button("⬇️ Download Final Video", f, file_name="Clarity_Video.mp4")

            st.success("Export complete!")
