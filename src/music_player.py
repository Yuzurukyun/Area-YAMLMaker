# Danganronpa Online Area List Maker by Yuzuru #
# Please contact the following if you encounter any bugs
# Discord: Yuzuru#2897, Gmail: <yuzuru.aceattorneyonline@gmail.com>


from src.constant import Constant

from PyQt5.QtWidgets import QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtCore import QUrl


class MusicPlayer(QWidget):
    def __init__(self, main_window):
        super(MusicPlayer, self).__init__()
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.music_file = Constant.get_music()
        self.main_window = main_window
        self.setVisible(False)

    def setup_player(self) -> None:
        import os

        full_file_path = os.path.join(os.getcwd(), self.music_file)
        url = QUrl.fromLocalFile(full_file_path)
        content = QMediaContent(url)

        self.playlist.addMedia(content)
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

        self.player.setPlaylist(self.playlist)
        self.player.setVolume(30)

    def play_player(self) -> None:
        self.setup_player()
        if self.player.isMuted():
            self.main_window.log_send("Music Player Unmuted.")
            self.mute_player()

        self.main_window.log_send()
        self.player.play()

    def mute_player(self) -> None:
        self.main_window.log_send("Music Player Muted.")
        self.player.setMuted((not self.player.isMuted()))
