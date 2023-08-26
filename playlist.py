import streamlit as st
import os
from pytube import YouTube, Playlist

class YouTubeDownloaderApp:
    def download_single_video(self):
        video_url = st.text_input("Enter the YouTube video URL")

        if st.button("Download Single Video"):
            try:
                yt = YouTube(video_url)
                stream = yt.streams.filter(res="720p").first()  # Filter for 720p resolution
                if stream:
                    st.text(f"Downloading {yt.title}...")
                    save_directory = os.path.join(os.path.expanduser("~"), "Downloads")
                    stream.download(output_path=save_directory)
                    st.text("Download complete!")
                else:
                    st.text(f"No 720p stream available for {yt.title}")
            except Exception as e:
                st.text(f"An error occurred while downloading: {e}")

    def download_playlist(self):
        playlist_url = st.text_input("Enter the YouTube playlist URL")

        if st.button("Download Playlist"):
            try:
                playlist = Playlist(playlist_url)
                total_videos = len(playlist.video_urls)

                with st.progress("Downloading Playlist"):
                    for video_url in playlist.video_urls:
                        try:
                            yt = YouTube(video_url)
                            stream = yt.streams.filter(res="720p").first()
                            if stream:
                                st.text(f"Downloading {yt.title}...")
                                save_directory = os.path.join(os.path.expanduser("~"), "Downloads")
                                stream.download(output_path=save_directory)
                                self.update_playlist_progress(total_videos)
                            else:
                                st.text(f"No 720p stream available for {yt.title}")
                        except Exception as e:
                            st.text(f"An error occurred while downloading: {e}")
                            self.reset_playlist_label()

            except Exception as e:
                st.text(f"An error occurred: {e}")
                self.reset_playlist_label()

    def update_playlist_progress(self, total_videos):
        st.text(f"Downloaded {total_videos}/{total_videos} videos from the playlist!")
    
    def reset_playlist_label(self):
        st.text("")

app = YouTubeDownloaderApp()


st.image("youtube_icon.png", width=100)  # Add your YouTube icon image
st.title("YouTube VIdeo & Playlist Downloader")




with st.expander("Download Single Video"):
    app.download_single_video()

with st.expander("Download Playlist"):
    app.download_playlist()

st.write("Created by MULAMBA JORAM JEFFERSON")  # Your signature
