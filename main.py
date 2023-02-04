import sys
import librosa
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QLabel, QPushButton)
from PyQt5.QtCore import Qt

class BPMKeyDetector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("BPM and Key Detector")
        self.setGeometry(100, 100, 300, 100)
        
        self.openFileButton = QPushButton("Open File", self)
        self.openFileButton.clicked.connect(self.openFile)
        self.openFileButton.resize(self.openFileButton.sizeHint())
        self.openFileButton.move(100, 20)
        
        self.bpmLabel = QLabel("BPM:", self)
        self.bpmLabel.move(20, 60)
        self.bpmLabel.resize(100, 20)
        
        self.keyLabel = QLabel("Key:", self)
        self.keyLabel.move(160, 60)
        self.keyLabel.resize(100, 20)
        
        self.show()
        
    def openFile(self, event):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Wav Files (*.wav);;All Files (*)", options=options)
        if fileName:
            y, sr = librosa.load(fileName)

            tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
            self.bpmLabel.setText("BPM: {:.2f}".format(tempo))

            chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
            key = librosa.pitch_tuning(chroma)
            self.keyLabel.setText("Key: {:.2f}".format(key))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BPMKeyDetector()
    sys.exit(app.exec_())
