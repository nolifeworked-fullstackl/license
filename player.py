import sys
import os

# =================================================================================
# НАСТРОЙКИ ПУТЕЙ VLC
# =================================================================================
# Мы просто указываем Python-у, где искать установленный DLL, 
# так как C++ установщик гарантированно поставит VLC в стандартную папку.

IS_64_BIT_PYTHON = sys.maxsize > 2**32

if IS_64_BIT_PYTHON:
    VLC_INSTALL_DIR = r"C:\Program Files\VideoLAN\VLC"
else:
    VLC_INSTALL_DIR = r"C:\Program Files (x86)\VideoLAN\VLC"

# Добавляем путь к DLL VLC, чтобы модуль 'vlc' мог его найти
os.environ['PATH'] = VLC_INSTALL_DIR + ";" + os.environ['PATH']
if hasattr(os, 'add_dll_directory'):
    try:
        os.add_dll_directory(VLC_INSTALL_DIR)
    except:
        pass

# =================================================================================
# ЗАПУСК ПЛЕЕРА
# =================================================================================

try:
    import vlc
    from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame
    from PyQt5.QtCore import Qt, QTimer
except ImportError as e:
    # В скомпилированном EXE этого произойти не должно
    sys.exit()

class KioskPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        # Список файлов. Они должны лежать РЯДОМ с player.exe
        self.playlist = ["1.mp4", "2.mp4", "3.mp4", "4.mp4", "5.mp4"]
        self.current_index = 0
        
        # Определение папки запуска (работает и для .py, и для .exe)
        if getattr(sys, 'frozen', False):
            self.base_dir = os.path.dirname(sys.executable)
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))

        self.setWindowTitle("Kiosk")
        # Настройки окна: поверх всех окон, без рамок
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.showFullScreen()
        
        # Черный фон и скрытие курсора
        self.setStyleSheet("background-color: black;") 
        self.setCursor(Qt.BlankCursor) 

        self.video_frame = QFrame(self)
        self.setCentralWidget(self.video_frame)

        # Настройки VLC: повтор, на весь экран, скрыть мышь, тихо
        self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen', '--mouse-hide-timeout=0', '--quiet', '--no-video-title-show')
        self.player = self.instance.media_player_new()
        self.player.set_hwnd(self.video_frame.winId())

        self.events = self.player.event_manager()
        self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.on_end)
        self.events.event_attach(vlc.EventType.MediaPlayerEncounteredError, self.on_error)

        self.play_video()

    def play_video(self):
        if not self.playlist: return
        if self.current_index >= len(self.playlist): self.current_index = 0

        path = os.path.join(self.base_dir, self.playlist[self.current_index])
        
        if os.path.exists(path):
            media = self.instance.media_new(path)
            self.player.set_media(media)
            self.player.play()
        else:
            # Если файла нет, пробуем следующий
            self.current_index += 1
            QTimer.singleShot(100, self.play_video)

    def on_end(self, event):
        self.current_index += 1
        QTimer.singleShot(10, self.play_video)

    def on_error(self, event):
        self.current_index += 1
        QTimer.singleShot(500, self.play_video)

    # Аварийный выход по F6 (можно убрать для полной блокировки)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F6:
            sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KioskPlayer()
    window.show()
    sys.exit(app.exec_())