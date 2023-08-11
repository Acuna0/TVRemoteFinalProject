import pathlib
from TVRemoteProjectPyFile import *
from PyQt6.QtWidgets import *


class TVremote(QMainWindow, MainUiWindow):
    """
    Class representing values and allowable functions for an TV Remote object.
    """
    MIN_VOLUME = 0
    MAX_VOLUME = 100
    MIN_CHANNEL = 0
    MAX_CHANNEL = 9

    def __init__(self) -> None:
        """
        Method to set default values and assign functions to buttons for TV Remote object.
        """
        super().__init__()
        self.setup_ui(self)
        self.__status = False
        self.__muted = False
        self.__volume: int = TVremote.MIN_VOLUME
        self.__channel: int = TVremote.MIN_CHANNEL
        self.__previousChannel: int = self.__channel

        self.pushButton_channelUp.clicked.connect(lambda: self.channel_up())
        self.pushButton_channelDown.clicked.connect(lambda: self.channel_down())
        self.pushButton_volumeUp.clicked.connect(lambda: self.volume_up())
        self.pushButton_volumeDown.clicked.connect(lambda: self.volume_down())

        self.pushButton_power.clicked.connect(lambda: self.power())
        self.pushButton_backButton.clicked.connect(lambda: self.undo())
        self.pushButton_playPause.clicked.connect(lambda: self.play_pause())
        self.pushButton_muteButton.clicked.connect(lambda: self.mute())

        self.pushButton_digit0.clicked.connect(lambda: self.change_channel(0))
        self.pushButton_digit1.clicked.connect(lambda: self.change_channel(1))
        self.pushButton_digit2.clicked.connect(lambda: self.change_channel(2))
        self.pushButton_digit3.clicked.connect(lambda: self.change_channel(3))
        self.pushButton_digit4.clicked.connect(lambda: self.change_channel(4))
        self.pushButton_digit5.clicked.connect(lambda: self.change_channel(5))
        self.pushButton_digit6.clicked.connect(lambda: self.change_channel(6))
        self.pushButton_digit7.clicked.connect(lambda: self.change_channel(7))
        self.pushButton_digit8.clicked.connect(lambda: self.change_channel(8))
        self.pushButton_digit9.clicked.connect(lambda: self.change_channel(9))
        # Add just a single ChangeChannel function call and add parameter of the button clicked to change channel
        # to that to simplify

        self.image_display.hide()
        self.video_widget.hide()
        self.progressBar_volumeBar.hide()
        self.lcdNumber_channelNum.hide()

    def power(self) -> None:
        """
        Method that modifies value of power button. (True = On, False = Off)
        """
        try:
            self.__status: bool = not self.__status
        except TypeError:
            self.lcdNumber_channelNum.display("Error")
            print("Power function error.")
        except RuntimeWarning or RuntimeError:
            print("Runtime Error: power function")
        else:
            if self.__status:
                self.lcdNumber_channelNum.show()
                self.progressBar_volumeBar.show()
                self.current_view()
            else:
                self.lcdNumber_channelNum.hide()
                self.progressBar_volumeBar.hide()
                self.image_display.hide()
                self.video_widget.setGeometry(QtCore.QRect(1, 1, 0, 0))

    def volume_up(self) -> None:
        """
        Method that modifies value of volume +1.
        """
        try:
            if self.__status:
                if not self.__muted:
                    if self.__volume < TVremote.MAX_VOLUME:
                        self.__volume += 2
                    else:
                        self.__volume = TVremote.MAX_VOLUME
        except ValueError:
            self.lcdNumber_channelNum.display("Error")
            print("Value Error: volume_up function")
        else:
            self.progressBar_volumeBar.setValue(self.__volume)

    def volume_down(self) -> None:
        """
        Method that modifies value of volume -1.
        """
        try:
            if self.__status:
                if not self.__muted:
                    if self.__volume > TVremote.MIN_VOLUME:
                        self.__volume -= 2
                    else:
                        self.__volume = TVremote.MIN_VOLUME
        except ValueError:
            self.lcdNumber_channelNum.display("Error")
            print("Value Error: volume_down function")
        else:
            self.progressBar_volumeBar.setValue(self.__volume)

    def channel_up(self) -> None:
        """
        Method that modifies value of channel +1.
        """
        try:
            if self.__status:
                if self.__channel < TVremote.MAX_CHANNEL:
                    self.lcdNumber_channelNum.raise_()
                    self.__channel += 1
                    self.__previousChannel = self.__channel - 1
                    self.current_view()
                else:
                    self.__channel = TVremote.MIN_CHANNEL
                    self.__previousChannel = TVremote.MAX_CHANNEL
                    self.current_view()
        except ValueError:
            self.lcdNumber_channelNum.display("Error")
            print("Value Error: channel_up function")
        else:
            self.lcdNumber_channelNum.display(self.__channel)

    def channel_down(self) -> None:
        """
        Method that modifies value of channel -11.
        """
        try:
            if self.__status:
                if self.__channel > TVremote.MIN_CHANNEL:
                    self.lcdNumber_channelNum.raise_()
                    self.__channel -= 1
                    self.__previousChannel = self.__channel + 1
                    self.current_view()
                else:
                    self.__channel = TVremote.MAX_CHANNEL
                    self.__previousChannel = TVremote.MIN_CHANNEL
                    self.current_view()
        except ValueError:
            self.lcdNumber_channelNum.display("Error")
            print("Value Error: channel_down function")
        else:
            self.lcdNumber_channelNum.display(self.__channel)

    def mute(self) -> None:
        """
        Method that modifies value of mute button and volume status.
        """
        try:
            if self.__status:
                self.__muted: bool = not self.__muted
                if self.__muted:
                    self.progressBar_volumeBar.hide()
                else:
                    self.progressBar_volumeBar.show()
        except TypeError:
            self.lcdNumber_channelNum.display("Error")
            print("Type Error: mute function.")

    def undo(self) -> None:
        """
        Method that goes back to the previous channel (undoing channel change).
        """
        try:
            if self.__status:
                self.__channel = self.__previousChannel
                self.lcdNumber_channelNum.display(self.__channel)
                self.current_view()
        except ValueError:
            self.lcdNumber_channelNum.display("Error")
            print("Value Error: undo function.")

    def play_pause(self) -> None:
        """
        Method that checks if media player is playing and to pause if not and play if paused.
        """
        try:
            if self.__status:
                if self.__channel == 0:
                    if self.media_player.isPlaying():
                        self.media_player.pause()
                    else:
                        self.media_player.play()
        except ValueError:
            self.lcdNumber_channelNum.display("Error")
            print("Value Error: play_pause function.")

    def change_channel(self, num: int) -> None:
        """
        Method that modifies value of LCD number that displays current channel number.
        """
        try:
            if self.__status:
                self.__previousChannel = self.__channel
                self.__channel = num
                self.lcdNumber_channelNum.display(self.__channel)
                self.current_view()
        except TypeError:
            self.lcdNumber_channelNum.display("Error")
            print("Type Error: change_channel function")
        except ValueError:
            self.lcdNumber_channelNum.display("Error")
            print("Value Error: change_channel function")

    def hide_media_player(self) -> None:
        """
        Method that pauses and places video widget out of sight while displaying another image.
        """
        try:
            self.media_player.pause()
            self.video_widget.setGeometry(QtCore.QRect(1, 1, 0, 0))
            self.image_display.show()
        except MemoryError:
            print("Memory Error: hide_media_player function.")

    def current_view(self) -> None:
        """
        Method that modifies the look of the screen depending on channel selected.
        """
        try:
            if self.__channel == 0:
                self.image_display.hide()
                self.video_widget.setGeometry(QtCore.QRect(20, 20, 361, 201))
                self.video_widget.show()
                self.media_player.play()
            elif self.__channel == 1:
                self.hide_media_player()
                self.image_display.setPixmap(QtGui.QPixmap("Channels/AngryBirds_1216.webp"))
            elif self.__channel == 2:
                self.hide_media_player()
                self.image_display.setPixmap(QtGui.QPixmap("Channels/Screenshot-2022-03-02-at-19.31.04.png"))
            elif self.__channel == 3:
                self.hide_media_player()
                self.image_display.setPixmap(QtGui.QPixmap("Channels/Sidemen_Charity_Football_Match_2018.png"))
            elif self.__channel == 4:
                self.hide_media_player()
                self.image_display.setPixmap(
                    QtGui.QPixmap("Channels/a_looney_tunes_show_scene_redrawn_in_40s_lt_style_by_"
                                  "eme2222_dfx1jx1-fullview.png"))
            elif self.__channel == 5:
                self.hide_media_player()
                self.image_display.setPixmap(QtGui.QPixmap("Channels/friends_rachel_vestita_da_sposa-1.png.webp"))
            elif self.__channel == 6:
                self.hide_media_player()
                self.image_display.setPixmap(QtGui.QPixmap("Channels/mcu-trailers-avengers-wakand.png"))
            elif self.__channel == 7:
                self.hide_media_player()
                self.image_display.setPixmap(
                    QtGui.QPixmap("Channels/png-transparent-anakin-skywalker-grand-moff-tarkin-"
                                  "r2-d2-star-wars-film-darth-vader-fashion-performance-"
                                  "scene.png"))
            elif self.__channel == 8:
                self.hide_media_player()
                self.image_display.setPixmap(QtGui.QPixmap("Channels/screen-shot-2019-11-22-at-8.37.59-am.png.webp"))
            elif self.__channel == 9:
                self.hide_media_player()
                self.image_display.setPixmap(QtGui.QPixmap("Channels/spongebob_and_patrick_png_3_by_riomadagascarkfp1_"
                                                           "dfxxrlu-fullview.jpg"))
        except ValueError:
            print("Value Error: current_view function.")
        except TypeError:
            print("Type Error: current_view function")
        except FileNotFoundError:
            self.image_display.setPixmap()  # To display an empty image if image searched for is not found.
            print("File Not Found Error: No such image exists.")
