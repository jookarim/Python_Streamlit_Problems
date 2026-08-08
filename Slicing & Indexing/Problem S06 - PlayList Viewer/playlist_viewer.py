import streamlit as st


class PlaylistViewer:
    def __init__(self):
        self.__songs = []
        self.__generate_songs()

    def __generate_songs(self):
        for i in range(20):
            self.__songs.append(f"Song: {i + 1}")

    def __get_songs_data(self):
        return (
            self.__songs[:5],
            self.__songs[len(self.__songs) - 5:],
            self.__songs[
                len(self.__songs) // 2 - 2:
                len(self.__songs) // 2 + 3
            ],
            
            self.__songs[::-1],
            self.__songs[1::2]
        )

    def display_data(self):
        songs_data = self.__get_songs_data()

        st.write(f"First 5 songs: {songs_data[0]}")
        st.write(f"Last 5 songs: {songs_data[1]}")
        st.write(f"Middle 5 songs: {songs_data[2]}")
        st.write(f"Playlist Reverse order: {songs_data[3]}")
        st.write(f"Every other song: {songs_data[4]}")


playlist_viewer = PlaylistViewer()
playlist_viewer.display_data()