#!/usr/bin/env python3
import sys
import os
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QFileDialog, 
                             QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
                             QMenu, QAction, QMessageBox, QFrame, QToolButton,
                             QRubberBand)
from PyQt5.QtCore import Qt, QUrl, QSize, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter, QDesktopServices, QIcon, QPen, QColor, QBrush, QPolygon

# Deteksi dukungan cetak Linux secara aman
try:
    from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
    HAS_PRINT_SUPPORT = True
except ImportError:
    HAS_PRINT_SUPPORT = False


def create_drawn_icon(name, color_hex="#555555", size=32):
    """
    Fungsi pembantu untuk menggambar ikon secara vektor langsung di memori.
    Ini menjamin ikon selalu muncul di Kali Linux tanpa tergantung pada tema eksternal.
    """
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    color = QColor(color_hex)
    pen = QPen(color)
    pen.setWidthF(1.8)
    pen.setCapStyle(Qt.RoundCap)
    pen.setJoinStyle(Qt.RoundJoin)
    painter.setPen(pen)
    
    s = size / 100.0  # Faktor skala 0-100
    
    if name == "file":
        # Ikon Kertas Dokumen
        painter.drawRect(int(25*s), int(15*s), int(50*s), int(70*s))
        painter.drawLine(int(52*s), int(15*s), int(52*s), int(35*s))
        painter.drawLine(int(52*s), int(35*s), int(75*s), int(35*s))
        
    elif name == "print":
        # Ikon Printer
        painter.drawRect(int(25*s), int(42*s), int(50*s), int(25*s))
        painter.drawRect(int(35*s), int(22*s), int(30*s), int(20*s))
        painter.drawRect(int(32*s), int(67*s), int(36*s), int(10*s))
        
    elif name == "email":
        # Ikon Amplop
        painter.drawRect(int(20*s), int(30*s), int(60*s), int(40*s))
        painter.drawLine(int(20*s), int(30*s), int(50*s), int(53*s))
        painter.drawLine(int(80*s), int(30*s), int(50*s), int(53*s))
        
    elif name == "open":
        # Ikon Folder
        painter.drawRect(int(20*s), int(35*s), int(60*s), int(40*s))
        painter.drawRect(int(20*s), int(25*s), int(25*s), int(10*s))
        
    elif name == "zoom-in":
        # Kaca Pembesar +
        painter.drawEllipse(int(25*s), int(25*s), int(40*s), int(40*s))
        painter.drawLine(int(57*s), int(57*s), int(80*s), int(80*s))
        painter.drawLine(int(37*s), int(45*s), int(53*s), int(45*s))
        painter.drawLine(int(45*s), int(37*s), int(45*s), int(53*s))
        
    elif name == "zoom-out":
        # Kaca Pembesar -
        painter.drawEllipse(int(25*s), int(25*s), int(40*s), int(40*s))
        painter.drawLine(int(57*s), int(57*s), int(80*s), int(80*s))
        painter.drawLine(int(37*s), int(45*s), int(53*s), int(45*s))
        
    elif name == "fit":
        # Kotak Ganda (Menyesuaikan Jendela)
        painter.drawRect(int(25*s), int(25*s), int(50*s), int(50*s))
        painter.drawRect(int(35*s), int(35*s), int(30*s), int(30*s))
        
    elif name == "prev":
        # Panah Kiri
        polygon = QPolygon([
            QPoint(int(65*s), int(25*s)),
            QPoint(int(35*s), int(50*s)),
            QPoint(int(65*s), int(75*s))
        ])
        painter.setBrush(QBrush(color))
        painter.drawPolygon(polygon)
        
    elif name == "next":
        # Panah Kanan
        polygon = QPolygon([
            QPoint(int(35*s), int(25*s)),
            QPoint(int(65*s), int(50*s)),
            QPoint(int(35*s), int(75*s))
        ])
        painter.setBrush(QBrush(color))
        painter.drawPolygon(polygon)
        
    elif name == "fullscreen":
        # Monitor Komputer
        painter.drawRect(int(22*s), int(25*s), int(56*s), int(40*s))
        painter.drawLine(int(42*s), int(65*s), int(35*s), int(78*s))
        painter.drawLine(int(58*s), int(65*s), int(65*s), int(78*s))
        painter.drawLine(int(35*s), int(78*s), int(65*s), int(78*s))
        
    elif name == "rotate-left":
        # Putar Kiri
        painter.drawArc(int(25*s), int(25*s), int(50*s), int(50*s), int(30*16), int(270*16))
        painter.drawLine(int(25*s), int(50*s), int(15*s), int(50*s))
        painter.drawLine(int(25*s), int(50*s), int(25*s), int(40*s))
        
    elif name == "rotate-right":
        # Putar Kanan
        painter.drawArc(int(25*s), int(25*s), int(50*s), int(50*s), int(-90*16), int(270*16))
        painter.drawLine(int(75*s), int(50*s), int(85*s), int(50*s))
        painter.drawLine(int(75*s), int(50*s), int(75*s), int(40*s))
        
    elif name == "delete":
        # Silang Hapus (Warna Merah secara default)
        pen.setColor(QColor("#d32f2f" if color_hex == "#555555" else color_hex))
        pen.setWidthF(3.0)
        painter.setPen(pen)
        painter.drawLine(int(30*s), int(30*s), int(70*s), int(70*s))
        painter.drawLine(int(70*s), int(30*s), int(30*s), int(70*s))

    elif name == "crop":
        # Ikon Crop (Dua sudut siku-siku saling tumpang tindih)
        painter.drawRect(int(32*s), int(32*s), int(42*s), int(42*s))
        # Garis horizontal kiri atas menjulur ke luar
        painter.drawLine(int(15*s), int(32*s), int(32*s), int(32*s))
        # Garis vertikal kiri atas menjulur ke luar
        painter.drawLine(int(32*s), int(15*s), int(32*s), int(32*s))
        # Garis horizontal kanan bawah menjulur ke luar
        painter.drawLine(int(74*s), int(74*s), int(85*s), int(74*s))
        # Garis vertikal kanan bawah menjulur ke luar
        painter.drawLine(int(74*s), int(74*s), int(74*s), int(85*s))
        
    painter.end()
    return QIcon(pixmap)


class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet("background-color: #eef3fa; border: none;")
        
        # Mengaktifkan mode seret genggam (drag-to-pan) bawaan Qt
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.pixmap_item = None

        # Variabel pendukung cropping
        self.crop_mode = False
        self.rubber_band = None
        self.origin = QPoint()

    def setImage(self, pixmap):
        self.scene.clear()
        self.resetTransform()
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.pixmap_item.setTransformationMode(Qt.SmoothTransformation)
        self.scene.addItem(self.pixmap_item)
        self.setSceneRect(self.pixmap_item.boundingRect())
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

    def set_crop_mode(self, enabled):
        """Mengatur mode pemotongan gambar."""
        self.crop_mode = enabled
        if enabled:
            # Matikan fungsi geser (pan) saat sedang menggambar seleksi crop
            self.setDragMode(QGraphicsView.NoDrag)
            self.setCursor(Qt.CrossCursor)
        else:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.setCursor(Qt.ArrowCursor)
            if self.rubber_band:
                self.rubber_band.hide()

    def mousePressEvent(self, event):
        if self.crop_mode and event.button() == Qt.LeftButton:
            self.origin = event.pos()
            if not self.rubber_band:
                self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
            self.rubber_band.setGeometry(QRect(self.origin, QSize()))
            self.rubber_band.show()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.crop_mode and self.rubber_band and (event.buttons() & Qt.LeftButton):
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.crop_mode and self.rubber_band and event.button() == Qt.LeftButton:
            rect = self.rubber_band.geometry()
            self.rubber_band.hide()
            
            # Berikan waktu jeda sebentar agar visual rubber band menghilang
            if rect.width() > 10 and rect.height() > 10:
                parent_window = self.window()
                if hasattr(parent_window, "confirm_crop"):
                    parent_window.confirm_crop(rect)
        else:
            super().mouseReleaseEvent(event)

    def get_cropped_pixmap(self, view_rect):
        """Memotong QPixmap asli berdasarkan area koordinat view."""
        if not self.pixmap_item:
            return None

        # Konversi koordinat tampilan (view) ke koordinat scene
        scene_polygon = self.mapToScene(view_rect)
        scene_rect = scene_polygon.boundingRect()

        # Konversi koordinat scene ke koordinat lokal elemen gambar (pixmap_item)
        local_rect = self.pixmap_item.mapFromScene(scene_rect).boundingRect()

        original_pixmap = self.pixmap_item.pixmap()
        pixmap_rect = original_pixmap.rect()

        # Batasi area crop agar tidak keluar dari dimensi asli gambar
        final_rect = local_rect.toRect().intersected(pixmap_rect)

        if final_rect.isEmpty() or final_rect.width() < 5 or final_rect.height() < 5:
            return None

        return original_pixmap.copy(final_rect)

    def wheelEvent(self, event):
        zoom_factor = 1.15
        if event.angleDelta().y() < 0:
            zoom_factor = 1.0 / zoom_factor
        self.scale(zoom_factor, zoom_factor)

    def resizeEvent(self, event):
        if self.pixmap_item:
            self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)
        super().resizeEvent(event)


class PhotoViewerApp(QMainWindow):
    def __init__(self, image_path=None):
        super().__init__()
        self.setWindowTitle("Windows Photo Viewer (Linux)")
        self.resize(1000, 650)
        self.current_image_path = ""
        self.image_files = [] 
        self.initUI()
        
        # Otomatis buka gambar jika ada argumen file dari klik dua kali
        if image_path:
            self.load_image(image_path)

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # -----------------------------------------------------------------
        # TOP BAR
        # -----------------------------------------------------------------
        self.top_bar = QWidget()
        self.top_bar.setStyleSheet("""
            QWidget {
                background-color: #f5f6f7; 
                border-bottom: 1px solid #dadbde;
            }
            QPushButton, QToolButton {
                background-color: transparent;
                border: none;
                padding: 6px 12px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 12px;
                color: #333333;
            }
            QPushButton:hover, QToolButton:hover {
                background-color: #e5e5e5;
                border-radius: 2px;
            }
        """)
        top_layout = QHBoxLayout(self.top_bar)
        top_layout.setContentsMargins(10, 5, 10, 5)
        top_layout.setSpacing(5)

        # Tombol File & Ikon custom
        btn_file = QPushButton(" File ▼")
        btn_file.setIcon(create_drawn_icon("file", "#555555"))
        btn_file.setIconSize(QSize(16, 16))
        
        file_menu = QMenu(btn_file)
        action_open = QAction("Open Photo...", self)
        action_open.setIcon(create_drawn_icon("open", "#555555"))
        action_open.triggered.connect(self.choose_and_open_image)
        file_menu.addAction(action_open)
        btn_file.setMenu(file_menu)

        # Tombol Print & Ikon custom
        btn_print = QPushButton(" Print ▼")
        btn_print.setIcon(create_drawn_icon("print", "#555555"))
        btn_print.setIconSize(QSize(16, 16))
        
        print_menu = QMenu(btn_print)
        action_print = QAction("Print...", self)
        action_print.setIcon(create_drawn_icon("print", "#555555"))
        action_print.triggered.connect(self.print_photo)
        print_menu.addAction(action_print)
        btn_print.setMenu(print_menu)

        # Tombol E-mail & Ikon custom
        btn_email = QPushButton(" E-mail")
        btn_email.setIcon(create_drawn_icon("email", "#555555"))
        btn_email.setIconSize(QSize(16, 16))
        btn_email.clicked.connect(self.send_email)

        # Tombol Crop Baru & Ikon custom
        self.btn_crop = QPushButton(" Crop")
        self.btn_crop.setIcon(create_drawn_icon("crop", "#555555"))
        self.btn_crop.setIconSize(QSize(16, 16))
        self.btn_crop.clicked.connect(self.toggle_crop_mode)

        # Tombol Open (Requirement 6) & Ikon custom
        btn_open = QToolButton()
        btn_open.setText(" Open ▼")
        btn_open.setIcon(create_drawn_icon("open", "#555555"))
        btn_open.setIconSize(QSize(16, 16))
        btn_open.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        btn_open.setPopupMode(QToolButton.InstantPopup)
        
        open_menu = QMenu(btn_open)
        action_open_main = QAction("Open File...", self)
        action_open_main.setIcon(create_drawn_icon("open", "#555555"))
        action_open_main.triggered.connect(self.choose_and_open_image)
        open_menu.addAction(action_open_main)
        open_menu.addSeparator()

        self.open_with_menu = QMenu("Open with", self)
        self.open_with_menu.setIcon(create_drawn_icon("file", "#555555"))
        
        apps = [
            ("GIMP Image Editor", "gimp"),
            ("Ristretto Image Viewer", "ristretto"),
            ("Firefox Web Browser", "firefox"),
            ("System Default (xdg-open)", "xdg-open")
        ]
        for name, cmd in apps:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, c=cmd: self.open_with(c))
            self.open_with_menu.addAction(action)

        open_menu.addMenu(self.open_with_menu)
        btn_open.setMenu(open_menu)

        top_layout.addWidget(btn_file)
        top_layout.addWidget(btn_print)
        top_layout.addWidget(btn_email)
        top_layout.addWidget(self.btn_crop) # Ditambahkan ke layout top bar
        top_layout.addWidget(btn_open)
        top_layout.addStretch()
        main_layout.addWidget(self.top_bar)

        # -----------------------------------------------------------------
        # MAIN VIEW
        # -----------------------------------------------------------------
        self.view = ZoomableGraphicsView()
        main_layout.addWidget(self.view)

        # -----------------------------------------------------------------
        # BOTTOM BAR
        # -----------------------------------------------------------------
        self.bottom_bar_container = QWidget()
        self.bottom_bar_container.setStyleSheet("background-color: #eef3fa;")
        bottom_layout = QHBoxLayout(self.bottom_bar_container)
        bottom_layout.setContentsMargins(0, 10, 0, 15)

        capsule_frame = QFrame()
        capsule_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #e2ecf7);
                border: 1px solid #a3b8cc;
                border-radius: 20px;
            }
            QPushButton {
                background: transparent;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgba(59, 90, 130, 0.1);
                border-radius: 12px;
            }
        """)
        capsule_layout = QHBoxLayout(capsule_frame)
        capsule_layout.setContentsMargins(15, 4, 15, 4)
        capsule_layout.setSpacing(12)

        # Navigasi bawah menggunakan ikon custom (Bebas ketergantungan OS)
        btn_zoom_in = QPushButton()
        btn_zoom_in.setIcon(create_drawn_icon("zoom-in", "#3b5a82"))
        btn_zoom_in.setIconSize(QSize(16, 16))
        btn_zoom_in.setToolTip("Zoom In")
        btn_zoom_in.clicked.connect(self.zoom_in)

        btn_zoom_out = QPushButton()
        btn_zoom_out.setIcon(create_drawn_icon("zoom-out", "#3b5a82"))
        btn_zoom_out.setIconSize(QSize(16, 16))
        btn_zoom_out.setToolTip("Zoom Out")
        btn_zoom_out.clicked.connect(self.zoom_out)

        btn_fit = QPushButton()
        btn_fit.setIcon(create_drawn_icon("fit", "#3b5a82"))
        btn_fit.setIconSize(QSize(16, 16))
        btn_fit.setToolTip("Fit Window")
        btn_fit.clicked.connect(self.fit_to_window)

        btn_prev = QPushButton()
        btn_prev.setIcon(create_drawn_icon("prev", "#3b5a82"))
        btn_prev.setIconSize(QSize(16, 16))
        btn_prev.setToolTip("Previous Image")
        btn_prev.clicked.connect(self.show_prev_image)
        
        # Requirement 2: Tombol Fullscreen (Tengah, lingkaran biru) dengan ikon Putih
        self.btn_fullscreen = QPushButton() 
        self.btn_fullscreen.setObjectName("btnFullscreen")
        self.btn_fullscreen.setIcon(create_drawn_icon("fullscreen", "#ffffff", 20))
        self.btn_fullscreen.setIconSize(QSize(20, 20))
        self.btn_fullscreen.setToolTip("Fullscreen")
        self.btn_fullscreen.setStyleSheet("""
            QPushButton#btnFullscreen {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5ca5e6, stop:1 #246ba6);
                border: 1px solid #1c5585;
                border-radius: 18px;
                min-width: 36px;
                max-width: 36px;
                min-height: 36px;
                max-height: 36px;
            }
            QPushButton#btnFullscreen:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #79bbf7, stop:1 #3582cc);
            }
        """)
        self.btn_fullscreen.clicked.connect(self.toggle_fullscreen)

        btn_next = QPushButton()
        btn_next.setIcon(create_drawn_icon("next", "#3b5a82"))
        btn_next.setIconSize(QSize(16, 16))
        btn_next.setToolTip("Next Image")
        btn_next.clicked.connect(self.show_next_image)

        btn_rot_left = QPushButton()
        btn_rot_left.setIcon(create_drawn_icon("rotate-left", "#3b5a82"))
        btn_rot_left.setIconSize(QSize(16, 16))
        btn_rot_left.setToolTip("Rotate Left")
        btn_rot_left.clicked.connect(self.rotate_left)

        btn_rot_right = QPushButton()
        btn_rot_right.setIcon(create_drawn_icon("rotate-right", "#3b5a82"))
        btn_rot_right.setIconSize(QSize(16, 16))
        btn_rot_right.setToolTip("Rotate Right")
        btn_rot_right.clicked.connect(self.rotate_right)
        
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #a3b8cc; max-width: 1px; margin: 4px 0;")

        # Requirement 3: Tombol Delete (X Merah)
        self.btn_delete = QPushButton()
        self.btn_delete.setObjectName("btnDelete")
        self.btn_delete.setIcon(create_drawn_icon("delete", "#d32f2f"))
        self.btn_delete.setIconSize(QSize(16, 16))
        self.btn_delete.setToolTip("Delete Photo")
        self.btn_delete.setStyleSheet("""
            QPushButton#btnDelete:hover {
                background-color: rgba(255, 23, 68, 0.15);
                border-radius: 12px;
            }
        """)
        self.btn_delete.clicked.connect(self.delete_photo)

        # Menyusun tombol ke dalam capsule
        capsule_layout.addWidget(btn_zoom_in)
        capsule_layout.addWidget(btn_zoom_out)
        capsule_layout.addWidget(btn_fit)
        capsule_layout.addWidget(btn_prev)
        capsule_layout.addWidget(self.btn_fullscreen)
        capsule_layout.addWidget(btn_next)
        capsule_layout.addWidget(btn_rot_left)
        capsule_layout.addWidget(btn_rot_right)
        capsule_layout.addWidget(line)
        capsule_layout.addWidget(self.btn_delete)

        bottom_layout.addStretch()
        bottom_layout.addWidget(capsule_frame)
        bottom_layout.addStretch()
        
        main_layout.addWidget(self.bottom_bar_container)

    # -----------------------------------------------------------------
    # LOGIKA & FUNGSI OPERASIONAL
    # -----------------------------------------------------------------

    def choose_and_open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp)"
        )
        if file_path:
            self.load_image(file_path)

    def load_image(self, path):
        self.current_image_path = path
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            self.view.setImage(pixmap)
            self.setWindowTitle(f"{os.path.basename(path)} - Windows Photo Viewer")
            self.update_image_list() 
        else:
            QMessageBox.critical(self, "Error", "Gagal memuat gambar.")

    def update_image_list(self):
        if not self.current_image_path:
            self.image_files = []
            return
        
        dir_path = os.path.dirname(self.current_image_path)
        supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')
        try:
            files = os.listdir(dir_path)
            self.image_files = [
                os.path.join(dir_path, f) for f in files 
                if f.lower().endswith(supported_formats)
            ]
            self.image_files.sort()
        except Exception:
            self.image_files = []

    def show_prev_image(self):
        if not self.current_image_path or not self.image_files:
            return
        try:
            idx = self.image_files.index(self.current_image_path)
            prev_idx = (idx - 1) % len(self.image_files)
            self.load_image(self.image_files[prev_idx])
        except ValueError:
            self.update_image_list()

    def show_next_image(self):
        if not self.current_image_path or not self.image_files:
            return
        try:
            idx = self.image_files.index(self.current_image_path)
            next_idx = (idx + 1) % len(self.image_files)
            self.load_image(self.image_files[next_idx])
        except ValueError:
            self.update_image_list()

    def zoom_in(self):
        self.view.scale(1.15, 1.15)

    def zoom_out(self):
        self.view.scale(1.0 / 1.15, 1.0 / 1.15)

    def fit_to_window(self):
        if self.view.pixmap_item:
            self.view.fitInView(self.view.sceneRect(), Qt.KeepAspectRatio)

    def rotate_left(self):
        self.view.rotate(-90)

    def rotate_right(self):
        self.view.rotate(90)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.exit_fullscreen()
        else:
            self.showFullScreen()
            self.top_bar.hide()
            self.bottom_bar_container.hide()

    def exit_fullscreen(self):
        self.showNormal()
        self.top_bar.show()
        self.bottom_bar_container.show()

    def toggle_crop_mode(self):
        """Mengaktifkan/menonaktifkan mode pemotongan foto."""
        if not self.current_image_path:
            QMessageBox.warning(self, "Peringatan", "Buka foto terlebih dahulu sebelum dipotong.")
            return

        is_active = not self.view.crop_mode
        self.view.set_crop_mode(is_active)

        if is_active:
            self.btn_crop.setText(" Cancel Crop")
            self.btn_crop.setStyleSheet("background-color: #fce4ec; color: #c2185b; font-weight: bold; border-radius: 2px;")
            QMessageBox.information(
                self, 
                "Mode Crop Aktif", 
                "Tarik klik kiri mouse pada gambar untuk memilih area yang ingin dipotong."
            )
        else:
            self.btn_crop.setText(" Crop")
            self.btn_crop.setStyleSheet("")

    def confirm_crop(self, rect):
        """Memproses hasil pemotongan gambar."""
        cropped_pixmap = self.view.get_cropped_pixmap(rect)
        if cropped_pixmap is None or cropped_pixmap.isNull():
            QMessageBox.warning(self, "Peringatan", "Gagal mengambil seleksi potongan foto.")
            return

        # Matikan mode crop dan kembalikan visual tombol ke semula
        self.view.set_crop_mode(False)
        self.btn_crop.setText(" Crop")
        self.btn_crop.setStyleSheet("")

        # Dialog Konfirmasi Penyimpanan
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Simpan Hasil Potongan")
        msg_box.setText("Apakah Anda ingin memotong foto ke area seleksi ini?")
        btn_overwrite = msg_box.addButton("Simpan & Timpa", QMessageBox.YesRole)
        btn_save_as = msg_box.addButton("Simpan Sebagai...", QMessageBox.NoRole)
        btn_cancel = msg_box.addButton("Batal", QMessageBox.RejectRole)

        msg_box.exec_()

        if msg_box.clickedButton() == btn_overwrite:
            try:
                success = cropped_pixmap.save(self.current_image_path)
                if success:
                    self.load_image(self.current_image_path)
                    QMessageBox.information(self, "Sukses", "Foto berhasil dipotong dan disimpan.")
                else:
                    QMessageBox.critical(self, "Error", "Gagal menimpa berkas asli.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal menyimpan berkas:\n{str(e)}")

        elif msg_box.clickedButton() == btn_save_as:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Simpan Foto Baru", self.current_image_path, "Images (*.png *.jpg *.jpeg *.bmp)"
            )
            if file_path:
                try:
                    success = cropped_pixmap.save(file_path)
                    if success:
                        self.load_image(file_path)
                        QMessageBox.information(self, "Sukses", "Foto berhasil disimpan ke berkas baru.")
                    else:
                        QMessageBox.critical(self, "Error", "Gagal menyimpan berkas baru.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Gagal menyimpan berkas:\n{str(e)}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if self.isFullScreen():
                self.exit_fullscreen()
        elif event.key() == Qt.Key_Left:
            self.show_prev_image()
        elif event.key() == Qt.Key_Right:
            self.show_next_image()
            
        super().keyPressEvent(event)

    def print_photo(self):
        if not self.current_image_path:
            QMessageBox.warning(self, "Peringatan", "Silakan buka foto terlebih dahulu sebelum mencetak.")
            return

        if not HAS_PRINT_SUPPORT:
            QMessageBox.warning(self, "Peringatan", "Sistem print PyQt5 tidak terdeteksi pada Python Anda.")
            return

        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter(printer)
            pixmap = self.view.pixmap_item.pixmap()
            
            rect = painter.viewport()
            size = pixmap.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(pixmap.rect())
            
            painter.drawPixmap(0, 0, pixmap)
            painter.end()

    def send_email(self):
        if not self.current_image_path:
            QMessageBox.warning(self, "Peringatan", "Buka foto terlebih dahulu untuk dikirim via E-mail.")
            return

        try:
            subprocess.Popen(["xdg-email", "--attach", self.current_image_path])
        except Exception:
            url = QUrl(f"mailto:?subject=Kirim Foto&body=Terlampir berkas gambar.")
            QDesktopServices.openUrl(url)

    def delete_photo(self):
        if not self.current_image_path:
            QMessageBox.warning(self, "Peringatan", "Tidak ada foto yang sedang dibuka.")
            return

        confirm = QMessageBox.question(
            self, 
            "Konfirmasi Hapus", 
            f"Apakah Anda yakin ingin menghapus file ini secara permanen?\n\n{os.path.basename(self.current_image_path)}",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                file_to_delete = self.current_image_path
                self.show_next_image()
                
                if self.current_image_path == file_to_delete:
                    self.view.scene.clear()
                    self.current_image_path = ""
                    self.setWindowTitle("Windows Photo Viewer (Linux)")
                
                os.remove(file_to_delete)
                self.update_image_list()
                QMessageBox.information(self, "Sukses", "Foto telah dihapus dari komputer.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal menghapus file:\n{str(e)}")

    def open_with(self, app_command):
        if not self.current_image_path:
            QMessageBox.warning(self, "Peringatan", "Silakan buka foto terlebih dahulu.")
            return
        try:
            subprocess.Popen([app_command, self.current_image_path])
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", f"Aplikasi '{app_command}' tidak ditemukan pada sistem Kali Linux Anda.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Memaksa sistem untuk selalu menggambar ikon menu
    app.setAttribute(Qt.AA_DontShowIconsInMenus, False)
    
    # Membaca argumen baris perintah jika aplikasi dibuka lewat double-click berkas
    image_to_open = sys.argv[1] if len(sys.argv) > 1 else None
    
    viewer = PhotoViewerApp(image_to_open)
    viewer.show()
    sys.exit(app.exec_())
