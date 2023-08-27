import os
import streamlit as st
from pytube import YouTube, Playlist

class YouTubeDownloaderApp:
    def __init__(self):
        self.quality_options = ["1080p", "720p", "480p"]  # Available quality options

    def download_single_video(self):
        st.subheader("Download Single Video")
        video_url = st.text_input("Enter the YouTube video URL")

        quality = st.selectbox("Select Video Quality:", self.quality_options, key="single_quality")

        if st.button("Download Single Video", key="single_download"):
            try:
                yt = YouTube(video_url)
                stream = yt.streams.filter(res=quality).first()
                if stream:
                    st.text(f"Downloading {yt.title}...")
                    save_directory = os.path.join(os.path.expanduser("~"), "Downloads")
                    stream.download(output_path=save_directory)
                    st.success("Download complete!")
                else:
                    st.error(f"No {quality} stream available for {yt.title}")
            except Exception as e:
                st.error(f"An error occurred while downloading: {e}")

    def download_playlist(self):
        st.subheader("Download Playlist")
        playlist_url = st.text_input("Enter the YouTube playlist URL")

        quality = st.selectbox("Select Video Quality:", self.quality_options, key="playlist_quality")

        if st.button("Download Playlist", key="playlist_download"):
            try:
                playlist = Playlist(playlist_url)
                total_videos = len(playlist.video_urls)

                with st.progress("Downloading Playlist"):
                    for video_url in playlist.video_urls:
                        try:
                            yt = YouTube(video_url)
                            stream = yt.streams.filter(res=quality).first()
                            if stream:
                                st.text(f"Downloading {yt.title}...")
                                save_directory = os.path.join(os.path.expanduser("~"), "Downloads")
                                stream.download(output_path=save_directory)
                                self.update_playlist_progress(total_videos)
                            else:
                                st.warning(f"No {quality} stream available for {yt.title}")
                        except Exception as e:
                            st.error(f"An error occurred while downloading: {e}")
                            self.reset_playlist_label()

            except Exception as e:
                st.error(f"An error occurred: {e}")
                self.reset_playlist_label()

    def update_playlist_progress(self, total_videos):
        st.text(f"Downloaded {total_videos}/{total_videos} videos from the playlist!")
    
    def reset_playlist_label(self):
        st.text("")

app = YouTubeDownloaderApp()

# App layout
st.image("youtube_icon.png", width=100)  # Add your YouTube icon image
st.title("YouTube Video & Playlist Downloader")
st.subheader("Download YouTube videos and playlists for free.#Strictly for Education purposes")
st.write("Created by MULAMBA JORAM JEFFERSON")  # Your signature

with st.expander("Download Single Video"):
    app.download_single_video()

with st.expander("Download Playlist"):
    app.download_playlist()
