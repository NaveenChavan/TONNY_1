import sys
import math
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QGraphicsOpacityEffect,QMenu)
from PyQt5.QtCore import (QTimer, Qt, QPointF, QRectF, QPropertyAnimation, QSize, 
                         QEasingCurve, QParallelAnimationGroup, QSequentialAnimationGroup)
from PyQt5.QtGui import (QPainter, QPen, QBrush, QColor, QFont, QFontMetrics,
                         QLinearGradient, QRadialGradient, QPainterPath)

# Import your existing modules
from agent import entrypoint
from livekit.rtc import VideoBufferType
import socket
import time
from datetime import datetime
from livekit import rtc
import asyncio
import threading
import logging

logging.getLogger('asyncio').setLevel(logging.WARNING)

import sys
import math
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QGraphicsOpacityEffect,QMenu)
from PyQt5.QtCore import (QTimer, Qt, QPointF, QRectF, QPropertyAnimation, QSize, 
                         QEasingCurve, QParallelAnimationGroup, QSequentialAnimationGroup)
from PyQt5.QtGui import (QPainter, QPen, QBrush, QColor, QFont, QFontMetrics,
                         QLinearGradient, QRadialGradient, QPainterPath)

import os
import sys
import json
import subprocess
import traceback
from PyQt5.QtWidgets import QApplication, QMessageBox, QInputDialog, QPushButton
from PyQt5.QtCore import Qt
import firebase_admin
from firebase_admin import credentials, db

import time
import socket
from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog, QVBoxLayout, QLabel, QProgressBar, QPushButton, QDialogButtonBox
from PyQt5.QtCore import QTimer, Qt

class ScanningAnimation(QWidget):
    """ULTRA PREMIUM scanning animation for MJ AI - FULL SCREEN"""
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Get screen dimensions for full screen
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        self.setGeometry(screen_geometry)
        
        # Animation state
        self.scan_position = 0
        self.opacity = 1.0
        self.pulse_phase = 0.0
        self.glow_intensity = 0.0
        self.particle_phase = 0.0
        self.hologram_phase = 0.0
        
        # Setup animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # 60 FPS
        
        # Auto-close after 3 seconds
        QTimer.singleShot(3000, self.fade_out)
        
    def update_animation(self):
        self.scan_position = (self.scan_position + 8) % (self.height() + 400)
        self.pulse_phase += 0.12
        self.particle_phase += 0.15
        self.hologram_phase += 0.08
        self.glow_intensity = 0.6 + 0.4 * math.sin(self.pulse_phase * 2)
        self.update()
        
    def fade_out(self):
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(800)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.finished.connect(self.close)
        self.anim.start()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Premium dark background with deep space gradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(8, 8, 25, 255))
        gradient.setColorAt(0.3, QColor(5, 5, 18, 250))
        gradient.setColorAt(0.7, QColor(3, 3, 12, 245))
        gradient.setColorAt(1, QColor(1, 1, 8, 250))
        painter.fillRect(self.rect(), QBrush(gradient))
        
        # Draw premium effects
        self.draw_nebula_effect(painter)
        self.draw_scanning_effect(painter)
        self.draw_hologram_grid(painter)
        self.draw_nova_text_premium(painter)
        self.draw_particles_premium(painter)
        self.draw_circuit_pattern(painter)
        
    def draw_nebula_effect(self, painter):
        """Draw nebula-like background effect"""
        for i in range(3):
            radius = 300 + i * 150
            center_x = self.width() * (0.3 + i * 0.2)
            center_y = self.height() * (0.4 + math.sin(self.pulse_phase + i) * 0.1)
            
            gradient = QRadialGradient(center_x, center_y, radius)
            gradient.setColorAt(0, QColor(255, 182, 193, 30))  # Light Pink
            gradient.setColorAt(0.5, QColor(255, 215, 0, 20))   # Gold
            gradient.setColorAt(1, QColor(255, 182, 193, 0))    # Light Pink
            
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(center_x, center_y), radius, radius)

    def draw_scanning_effect(self, painter):
        """ULTRA PREMIUM scanning lines with holographic effect"""
        for i in range(7):
            scan_y = (self.scan_position + i * 60) % (self.height() + 400)
            scan_height = 120 - i * 12
            
            # Multi-layer gradient for premium look
            gradient = QLinearGradient(0, scan_y, 0, scan_y + scan_height)
            alpha = 150 - i * 15
            gradient.setColorAt(0, QColor(255, 182, 193, 0))    # Light Pink
            gradient.setColorAt(0.1, QColor(255, 182, 255, int(alpha)//2))  # Pink
            gradient.setColorAt(0.3, QColor(255, 182, 193, int(alpha)))     # Light Pink
            gradient.setColorAt(0.5, QColor(255, 255, 182, int(alpha)))     # Light Gold
            gradient.setColorAt(0.7, QColor(255, 215, 0, int(alpha)))       # Gold
            gradient.setColorAt(0.9, QColor(255, 182, 255, int(alpha)//2))  # Pink
            gradient.setColorAt(1, QColor(255, 182, 193, 0))
            
            # Add glow effect
            glow_gradient = QLinearGradient(0, scan_y - 10, 0, scan_y + scan_height + 10)
            glow_gradient.setColorAt(0, QColor(255, 182, 193, 30))  # Light Pink
            glow_gradient.setColorAt(0.5, QColor(255, 215, 0, 60))   # Gold
            glow_gradient.setColorAt(1, QColor(255, 182, 193, 30))   # Light Pink
            
            painter.fillRect(0, scan_y - 10, self.width(), scan_height + 20, QBrush(glow_gradient))
            painter.fillRect(0, scan_y, self.width(), scan_height, QBrush(gradient))
            
    def draw_hologram_grid(self, painter):
        """Premium holographic grid effect"""
        
        # Vertical lines
        for x in range(0, self.width(), 40):
            alpha = 30 + 20 * math.sin(self.hologram_phase + x * 0.01)
            # CHANGE: float alpha ko int me convert karo
            painter.setPen(QPen(QColor(255, 215, 0, int(alpha)), 1))
            painter.drawLine(x, 0, x, self.height())
            
        # Horizontal lines
        for y in range(0, self.height(), 40):
            alpha = 30 + 20 * math.sin(self.hologram_phase + y * 0.01)
            # CHANGE: yahan bhi float alpha ko int me convert karo
            painter.setPen(QPen(QColor(255, 182, 193, int(alpha)), 1))  # Light Pink
            painter.drawLine(0, y, self.width(), y)
            
    def draw_nova_text_premium(self, painter):
        """ULTRA PREMIUM text with holographic effects"""
        # Main MJ AI text
        font = QFont("Segoe UI", 56, QFont.Black)
        painter.setFont(font)
        
        text = "MJ AI"
        metrics = QFontMetrics(font)
        text_width = metrics.horizontalAdvance(text)
        
        text_x = (self.width() - text_width) // 2
        text_y = self.height() // 2 - 60
        
        # Enhanced multi-layer glow effect
        glow_size = 20 + 12 * self.glow_intensity
        for i in range(int(glow_size), 0, -2):
            alpha = 50 - i * 1.5
            color = QColor(255, 192, 203,int(alpha))
            if i % 3 == 0:
                color = QColor(255, 182, 193, int(alpha))  # Light Pink glow
            
            painter.setPen(QPen(color, i))
            painter.drawText(text_x, text_y, text)
        
        # Main text with ULTRA PREMIUM gradient
        text_gradient = QLinearGradient(text_x, text_y, text_x + text_width, text_y + 60)
        text_gradient.setColorAt(0, QColor(255, 182, 193))    # Light Pink
        text_gradient.setColorAt(0.2, QColor(255, 200, 220))  # Pink
        text_gradient.setColorAt(0.4, QColor(255, 255, 255))  # White
        text_gradient.setColorAt(0.6, QColor(255, 240, 220))  # Light Gold
        text_gradient.setColorAt(0.8, QColor(255, 215, 0))    # Gold
        text_gradient.setColorAt(1, QColor(255, 182, 193))    # Light Pink
        
        painter.setPen(QPen(QBrush(text_gradient), 4))
        painter.drawText(text_x, text_y, text)
        
        # Premium subtitle with enhanced effects
        sub_font = QFont("Segoe UI", 20, QFont.DemiBold)
        painter.setFont(sub_font)
        sub_text = "LOVELY INITIALIZATION"
        sub_width = QFontMetrics(sub_font).horizontalAdvance(sub_text)
        sub_x = (self.width() - sub_width) // 2
        sub_y = text_y + 85
        
        # Subtitle glow
        for i in range(8, 0, -1):
            alpha = 40 - i * 3
            painter.setPen(QPen(QColor(100, 255, 255,int(alpha)), i))
            painter.drawText(sub_x, sub_y, sub_text)
        
        # Subtitle main text
        sub_gradient = QLinearGradient(sub_x, sub_y, sub_x + sub_width, sub_y + 10)
        sub_gradient.setColorAt(0, QColor(255, 240, 245))  # Very Light Pink
        sub_gradient.setColorAt(1, QColor(255, 215, 0))    # Gold
        painter.setPen(QPen(QBrush(sub_gradient), 2))
        painter.drawText(sub_x, sub_y, sub_text)
        
        # Enhanced loading animation
        dots = "." * (int(self.pulse_phase * 3) % 4)
        loading_text = f"SYSTEM BOOTING{dots}"
        loading_font = QFont("Segoe UI", 16, QFont.Normal)
        painter.setFont(loading_font)
        loading_width = QFontMetrics(loading_font).horizontalAdvance(loading_text)
        loading_x = (self.width() - loading_width) // 2
        loading_y = sub_y + 45
        
        sub_gradient.setColorAt(0, QColor(255, 240, 245))  # Very Light Pink
        painter.drawText(loading_x, loading_y, loading_text)
        
        # Progress bar
        bar_width = 300
        bar_height = 6
        bar_x = (self.width() - bar_width) // 2
        bar_y = loading_y + 30
        
        # Progress bar background
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(255, 182, 193, 100)))  # Light Pink
        painter.drawRoundedRect(bar_x, bar_y, bar_width, bar_height, 3, 3)
        
        # Animated progress
        progress = (self.pulse_phase * 50) % bar_width
        progress_gradient = QLinearGradient(bar_x, bar_y, bar_x + progress, bar_y + bar_height)
        progress_gradient.setColorAt(0, QColor(0, 255, 255))
        progress_gradient.setColorAt(1, QColor(0, 200, 255))
        painter.setBrush(QBrush(progress_gradient))
        painter.drawRoundedRect(bar_x, bar_y, int(progress), bar_height, 3, 3)
        
    def draw_particles_premium(self, painter):
        """ULTRA PREMIUM particle system"""
        for i in range(300):
            x = (i * 67 + self.particle_phase * 50) % self.width()
            y = (i * 43 + self.scan_position * 0.4) % self.height()
            size = 2 + math.sin(self.pulse_phase + i * 0.5) * 2
            alpha = 80 + int(50 * math.sin(self.particle_phase + i * 0.3))
            
            # Multi-color premium particles
            if i % 7 == 0:
                color = QColor(255, 182, 193, int(alpha))  # Light Pink
            elif i % 5 == 0:
                color = QColor(255, 215, 0, int(alpha))    # Gold
            elif i % 3 == 0:
                color = QColor(255, 105, 180, int(alpha))  # Hot Pink
            else:
                color = QColor(255, 228, 196, int(alpha))  # Bisque
                
            painter.setPen(QPen(color, size))
            painter.drawPoint(int(x), int(y))
            
            # Some particles as small circles
            if i % 13 == 0:
                painter.setBrush(QBrush(color))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QPointF(x, y), size/2, size/2)

    def draw_circuit_pattern(self, painter):
        """Premium circuit board pattern effect"""
        painter.setPen(QPen(QColor(255, 192, 203, 25), 1))
        
        # Circuit lines
        for i in range(0, self.width(), 60):
            for j in range(0, self.height(), 60):
                if (i + j) % 120 == 0:
                    alpha = 20 + 15 * math.sin(self.hologram_phase + i * 0.02 + j * 0.02)
                    painter.setPen(QPen(QColor(255, 182, 193, int(alpha)), 1))  # Light Pink
                    
                    # Draw small circuit connections
                    if i < self.width() - 60 and j < self.height() - 60:
                        painter.drawLine(i, j, i + 30, j)
                        painter.drawLine(i + 30, j, i + 30, j + 30)
                        painter.drawLine(i + 30, j + 30, i + 60, j + 30)

class ModernFloatingWindow(QMainWindow):
    """ULTRA PREMIUM floating window with LOVELY glassmorphism effects"""
    
    def __init__(self):
        super().__init__()
        print("🎯 ModernFloatingWindow INITIALIZED")
        self.setup_window()
        self.init_ui()
        self.setup_animations()
        
        # State management
        self.mic_active = False
        self.is_hovered = False
        
        # Connect buttons after UI is initialized
        self.floating_widget.connect_buttons(self)
        
        # Add protection against accidental closure
        self.setAttribute(Qt.WA_DeleteOnClose, False)
        
        print("🎯 Starting background agent...")
        # Start all your original background processes
        self._start_agent_background()
        print("🎯 ModernFloatingWindow FULLY LOADED")

    def closeEvent(self, event):
        """Handle window close event"""
        print("🛑 Close event triggered - Shutting down...")
        self.close_application()
        event.accept()
        
    def setup_window(self):
        """Configure ULTRA PREMIUM window properties"""
        self.setWindowTitle("MJ AI")
        self.setFixedSize(120, 120)  # Slightly larger for premium look
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # IMPROVED POSITIONING - Ensures window stays on screen
        screen_geo = QApplication.primaryScreen().availableGeometry()
        
        # Calculate safe position (not too close to edges)
        x_pos = max(60, min(screen_geo.width() - 180, screen_geo.width() // 2 - 60))
        y_pos = max(60, min(screen_geo.height() - 180, 100))
        
        print(f"🖥️ Screen size: {screen_geo.width()}x{screen_geo.height()}")
        print(f"📍 Premium window position: ({x_pos}, {y_pos})")
        
        self.move(int(x_pos), int(y_pos))
        
    def init_ui(self):
        """Initialize ULTRA PREMIUM user interface"""
        central_widget = QWidget()
        central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create ULTRA PREMIUM floating widget
        self.floating_widget = PremiumFloatingWidget()
        layout.addWidget(self.floating_widget)
        
        # Connect buttons after widget is created
        self.floating_widget.connect_buttons(self)

    def showEvent(self, event):
        """Debug method to ensure window is visible"""
        super().showEvent(event)
        print("🎯 Premium floating window shown - should be visible now!")
        print(f"📌 Window geometry: {self.geometry()}")
        print(f"👀 Window visible: {self.isVisible()}")
        
    def setup_animations(self):
        """Setup optimized animations"""
        # Gentle floating animation
        self.float_anim = QPropertyAnimation(self.floating_widget, b"pos")
        self.float_anim.setDuration(8000)
        self.float_anim.setLoopCount(-1)
        self.float_anim.setEasingCurve(QEasingCurve.InOutSine)
        self.start_floating_animation()
        
    def start_floating_animation(self):
        """Start smooth floating animation"""
        current_pos = self.floating_widget.pos()
        self.float_anim.setStartValue(current_pos)
        self.float_anim.setKeyValueAt(0.3, current_pos + QPointF(3, -4))
        self.float_anim.setKeyValueAt(0.7, current_pos + QPointF(-3, 3))
        self.float_anim.setEndValue(current_pos)
        self.float_anim.start()
        
    def enterEvent(self, event):
        """Handle mouse enter - show premium buttons"""
        self.is_hovered = True
        
        
    def leaveEvent(self, event):
        """Handle mouse leave - hide premium buttons"""
        self.is_hovered = False
        # Only hide if mouse truly left the entire window
        if not self.rect().contains(self.mapFromGlobal(QApplication.desktop().cursor().pos())):
            self.floating_widget.hide_option_buttons()
            
    def toggle_mic(self):
        """Toggle microphone state - YOUR ORIGINAL LOGIC"""
        self.mic_active = not self.mic_active
        if self.mic_active:
            print("🎤 Microphone activated - Listening...")
            # Add your original mic activation logic here
        else:
            print("🔇 Microphone deactivated")
            # Add your original mic deactivation logic here
        
    def show_settings(self):
        """Show settings - YOUR ORIGINAL LOGIC"""
        print("⚙️ Opening Premium Settings...")
        # Add your original settings logic here
        
    def show_help(self):
        """Show help - YOUR ORIGINAL LOGIC"""
        print("❓ Opening Premium Help...")
        # Add your original help logic here
            
    def close_application(self):
        """Close application COMPLETELY"""
        print("🔄 Shutting down MJ AI...")
        
        # Stop all animations
        if hasattr(self, 'float_anim'):
            self.float_anim.stop()
        
        # Cleanup floating widget
        if hasattr(self, 'floating_widget'):
            self.floating_widget.cleanup_animations()
        
        # Force quit the application
        QApplication.quit()
        
    def _start_agent_background(self):
        def run_agent():
            try:
                # Use asyncio in background thread with PROPER isolation
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                print("🟡 Starting MJ agent in background thread...")
                
                # IMPORTANT: Add delay to ensure main window is stable
                time.sleep(2)
                
                from livekit.agents.cli import run_app
                from livekit.agents import WorkerOptions
                print("🔧 Initializing LiveKit agent...")
                run_app(WorkerOptions(entrypoint_fnc=entrypoint))
                
            except Exception as e:
                print(f"❌ Agent error: {e}")
                import traceback
                traceback.print_exc()
                    
        # Start agent with lower priority to not interfere with UI
        self.agent_thread = threading.Thread(target=run_agent, daemon=True)
        self.agent_thread.name = "MJ-Agent-Background"
        self.agent_thread.start()
        print(f"🔧 Agent thread started: {self.agent_thread.name}")
        
    def mousePressEvent(self, event):
        """Allow window dragging"""
        if event.button() == Qt.LeftButton:
            self.drag_start = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        """Handle window dragging"""
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_start'):
            self.move(event.globalPos() - self.drag_start)
            event.accept()

    def contextMenuEvent(self, event):
        """Right-click context menu to close the application"""
        menu = QMenu(self)
        
        # Add close action
        close_action = menu.addAction("❌ Close MJ AI")
        close_action.triggered.connect(self.close_application)
        
        # Show menu at cursor position
        menu.exec_(event.globalPos())

class PremiumFloatingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(120, 120)  # Larger for premium look
        
        # Animation state
        self.animation_group = None
        self.is_animating = False
        self.pulse_phase = 0.0
        
        # 🔥 CRITICAL FIX: Initialize buttons list FIRST
        self.buttons = []
        
        # UPDATED: Premium button positions for larger widget
        self.button_target_positions = [
            QPointF(50, -45),   # Top button
            QPointF(120, 50),   # Right button  
            QPointF(50, 120),   # Bottom button
        ]
        
        self.button_colors = [
            QColor(255, 182, 193, 230),  # Light Pink (mic button)
            QColor(255, 215, 0, 230),    # Gold (settings button)
            QColor(255, 105, 180, 230)   # Hot Pink (help button)
        ]
        self.button_icons = ["🎤", "⚙️", "❓"]
        self.button_tooltips = ["LOVELY Voice", "Premium Settings", "AI Help"]
        
        self.setup_buttons()
        
        # Pulse animation timer
        self.pulse_timer = QTimer()
        self.pulse_timer.timeout.connect(self.update_pulse)
        self.pulse_timer.start(50)
        
    def update_pulse(self):
        """Update pulse animation for premium effects"""
        self.pulse_phase += 0.1
        self.update()
        
    def setup_buttons(self):
        """Create and setup ULTRA PREMIUM option buttons"""
        for i in range(3):
            button = QPushButton(self.button_icons[i], self)
            button.setFixedSize(65, 65)  # Larger buttons
            button.setToolTip(self.button_tooltips[i])
            button.hide()
            
            # Add opacity effect for fade animations
            opacity_effect = QGraphicsOpacityEffect(button)
            opacity_effect.setOpacity(0.0)
            button.setGraphicsEffect(opacity_effect)
            
            # Center button initially (hidden)
            button.move(55, 55)
            
            # ULTRA PREMIUM STYLESHEET
            button.setStyleSheet(f"""
                QPushButton {{
                    background: qradialgradient(cx:0.4, cy:0.4, radius: 1.8,
                        stop:0 rgba({self.button_colors[i].red()}, {self.button_colors[i].green()}, {self.button_colors[i].blue()}, 250),
                        stop:0.6 rgba({self.button_colors[i].red()}, {self.button_colors[i].green()}, {self.button_colors[i].blue()}, 180),
                        stop:0.9 rgba({self.button_colors[i].red()}, {self.button_colors[i].green()}, {self.button_colors[i].blue()}, 120),
                        stop:1.0 rgba({self.button_colors[i].red()}, {self.button_colors[i].green()}, {self.button_colors[i].blue()}, 80));
                    border: 3px solid rgba(255, 255, 255, 200);
                    border-radius: 30px;
                    color: white;
                    font-size: 20px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background: qradialgradient(cx:0.4, cy:0.4, radius: 1.8,
                        stop:0 rgba(255, 255, 255, 250),
                        stop:0.6 rgba({self.button_colors[i].red()}, {self.button_colors[i].green()}, {self.button_colors[i].blue()}, 220),
                        stop:1.0 rgba({self.button_colors[i].red()}, {self.button_colors[i].green()}, {self.button_colors[i].blue()}, 150));
                    border: 3px solid rgba(255, 255, 255, 255);
                }}
            """)
            
            self.buttons.append(button)
            
    def connect_buttons(self, main_window):
        """Connect buttons to main window functions"""
        for i, button in enumerate(self.buttons):
            if i == 0:  # Mic button
                button.clicked.connect(main_window.toggle_mic)
            elif i == 1:  # Settings button
                button.clicked.connect(main_window.show_settings)
            elif i == 2:  # Help button
                button.clicked.connect(main_window.show_help)
            
    def show_option_buttons(self):
        """Show buttons with ULTRA PREMIUM LOVELY animation"""
        try:
            if self.is_animating:
                return
                
            self.is_animating = True
            
            # Cancel any ongoing hide animations
            if self.animation_group and self.animation_group.state() == QPropertyAnimation.Running:
                self.animation_group.stop()
                self.animation_group.deleteLater()
                
            self.animation_group = QParallelAnimationGroup()
            
            for i, button in enumerate(self.buttons):
                button.show()
                button.raise_()
                
                # Start from center with small size
                button.setFixedSize(15, 15)
                button.move(52, 52)
                
                # Create parallel animation for each button
                button_group = QParallelAnimationGroup()
                
                # Position animation with premium easing
                pos_anim = QPropertyAnimation(button, b"pos")
                pos_anim.setDuration(600)
                pos_anim.setEasingCurve(QEasingCurve.OutBack)
                pos_anim.setStartValue(QPointF(52, 52))
                pos_anim.setEndValue(self.button_target_positions[i])
                
                # Scale animation with premium easing
                scale_anim = QPropertyAnimation(button, b"size")
                scale_anim.setDuration(600)
                scale_anim.setEasingCurve(QEasingCurve.OutBack)
                scale_anim.setStartValue(QSize(15, 15))
                scale_anim.setEndValue(QSize(65, 65))
                
                # Opacity fade-in animation
                opacity_effect = button.graphicsEffect()
                opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
                opacity_anim.setDuration(500)
                opacity_anim.setStartValue(0.0)
                opacity_anim.setEndValue(1.0)
                opacity_anim.setEasingCurve(QEasingCurve.OutCubic)
                
                button_group.addAnimation(pos_anim)
                button_group.addAnimation(scale_anim)
                button_group.addAnimation(opacity_anim)
                
                # Add LOVELY delay between each button
                delayed_group = QSequentialAnimationGroup()
                delayed_group.addPause(i * 150)  # 150ms delay for premium feel
                delayed_group.addAnimation(button_group)
                
                self.animation_group.addAnimation(delayed_group)
            
            self.animation_group.finished.connect(lambda: setattr(self, 'is_animating', False))
            self.animation_group.start()

        except Exception as e:
            print(f"Premium animation error: {e}")
            self.is_animating = False
        
    def hide_option_buttons(self):
        """Hide buttons with smooth LOVELY collapse"""
        try:
            if self.is_animating:
                return
                
            self.is_animating = True
            
            # Cancel any ongoing show animations
            if self.animation_group and self.animation_group.state() == QPropertyAnimation.Running:
                self.animation_group.stop()
                self.animation_group.deleteLater()
                
            self.animation_group = QParallelAnimationGroup()
            
            for i, button in enumerate(self.buttons):
                # Create parallel animation for each button
                button_group = QParallelAnimationGroup()
                
                # Scale down animation
                scale_anim = QPropertyAnimation(button, b"size")
                scale_anim.setDuration(400)
                scale_anim.setEasingCurve(QEasingCurve.InCubic)
                scale_anim.setStartValue(QSize(65, 65))
                scale_anim.setEndValue(QSize(15, 15))
                
                # Move back to center
                pos_anim = QPropertyAnimation(button, b"pos")
                pos_anim.setDuration(400)
                pos_anim.setEasingCurve(QEasingCurve.InCubic)
                pos_anim.setStartValue(self.button_target_positions[i])
                pos_anim.setEndValue(QPointF(52, 52))
                
                # Opacity fade-out animation
                opacity_effect = button.graphicsEffect()
                opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
                opacity_anim.setDuration(350)
                opacity_anim.setStartValue(1.0)
                opacity_anim.setEndValue(0.0)
                opacity_anim.setEasingCurve(QEasingCurve.InCubic)
                
                button_group.addAnimation(scale_anim)
                button_group.addAnimation(pos_anim)
                button_group.addAnimation(opacity_anim)
                
                # Hide button after animation completes
                button_group.finished.connect(button.hide)
                
                self.animation_group.addAnimation(button_group)
            
            self.animation_group.finished.connect(lambda: setattr(self, 'is_animating', False))
            self.animation_group.start()
            
        except Exception as e:
            print(f"Premium hide animation error: {e}")
            self.is_animating = False
            # Force hide all buttons
            for button in self.buttons:
                button.hide()
            
    def paintEvent(self, event):
        """Paint the ULTRA PREMIUM LOVELY glassmorphism widget"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw LOVELY glow effect
        self.draw_VADRYK_glow(painter)
        
        # Main circle with LOVELY glassmorphism
        self.draw_VADRYK_main_circle(painter)
        
        # Animated orbiting particles
        self.draw_orbiting_particles(painter)
        
        # Center "M" icon with holographic effect
        self.draw_center_icon(painter)

    def draw_VADRYK_glow(self, painter):
        """Draw LOVELY glow effect behind main circle"""
        glow_path = QPainterPath()
        glow_path.addEllipse(2, 2, 116, 116)
        
        # Multi-layer LOVELY glow
        for i in range(3):
            radius = 58 - i * 5
            gradient = QRadialGradient(60, 60, radius)
            
            if i == 0:
                gradient.setColorAt(0, QColor(255, 182, 193, 120))  # Light Pink
                gradient.setColorAt(0.7, QColor(255, 140, 160, 80))  # Medium Pink
                gradient.setColorAt(1, QColor(255, 105, 180, 0))    # Hot Pink
            elif i == 1:
                gradient.setColorAt(0, QColor(255, 215, 0, 60))     # Gold
                gradient.setColorAt(0.5, QColor(255, 182, 193, 40)) # Light Pink
                gradient.setColorAt(1, QColor(255, 192, 203, 0))    # Pink
            else:
                pulse_alpha = 30 + 20 * math.sin(self.pulse_phase)
                gradient.setColorAt(0, QColor(255, 255, 255, int(pulse_alpha)))
                gradient.setColorAt(1, QColor(255, 255, 255, 0))
            
            painter.fillPath(glow_path, QBrush(gradient))

    def draw_VADRYK_main_circle(self, painter):
        """Draw main circle with LOVELY glassmorphism"""
        main_path = QPainterPath()
        main_path.addEllipse(10, 10, 100, 100)
        
        # LOVELY glassmorphism gradient
        gradient = QRadialGradient(60, 60, 50)
        gradient.setColorAt(0, QColor(255, 255, 255, 180))
        gradient.setColorAt(0.2, QColor(255, 240, 245, 120))   # Very Light Pink
        gradient.setColorAt(0.4, QColor(255, 228, 225, 80))    # Misty Rose
        gradient.setColorAt(0.7, QColor(255, 192, 203, 50))    # Pink
        gradient.setColorAt(1, QColor(255, 182, 193, 30))
        
        painter.fillPath(main_path, QBrush(gradient))
        
        # LOVELY border with animated pulse
        pulse_width = 3 + math.sin(self.pulse_phase) * 1
        pen = QPen(QColor(255, 255, 255, 200))
        pen.setWidth(int(pulse_width))
        painter.setPen(pen)
        painter.drawPath(main_path)
        
        # Inner LOVELY rings
        for i in range(2):
            ring_path = QPainterPath()
            ring_radius = 35 - i * 10
            ring_path.addEllipse(60 - ring_radius, 60 - ring_radius, 
                               ring_radius * 2, ring_radius * 2)
            
            alpha = 80 - i * 30
            pen = QPen(QColor(255, 218, 233, int(alpha)))  # Pink tint
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawPath(ring_path)

    def draw_orbiting_particles(self, painter):
        """Draw animated orbiting particles"""
        for i in range(8):
            angle = (self.pulse_phase + i * math.pi/4) % (2 * math.pi)
            radius = 45
            x = 60 + radius * math.cos(angle)
            y = 60 + radius * math.sin(angle)
            
            particle_size = 2 + math.sin(self.pulse_phase * 2 + i) * 1.5
            alpha = 150 + int(50 * math.sin(self.pulse_phase * 3 + i))
            
            # Line 440-460 ke aas-pass:
            color = QColor(255, 182, 193, int(alpha))  # Light Pink
            if i % 3 == 0:
                color = QColor(255, 215, 0, int(alpha))    # Gold
            elif i % 2 == 0:
                color = QColor(255, 255, 255, int(alpha))  # White
                
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(x, y), particle_size, particle_size)

    def draw_center_icon(self, painter):
        """Draw premium center icon with holographic effect"""
        # Background glow for icon
        icon_glow = QRadialGradient(60, 60, 25)
        icon_glow.setColorAt(0, QColor(255, 182, 193, 100))  # Light Pink
        icon_glow.setColorAt(1, QColor(255, 182, 193, 0))
        painter.setBrush(QBrush(icon_glow))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(35, 35, 50, 50)
        
        # Main "M" icon with premium gradient
        painter.setPen(QPen(QColor(255, 255, 255, 255)))
        premium_font = QFont("Segoe UI", 28, QFont.Black)
        painter.setFont(premium_font)
        
        # Icon glow effect
        for i in range(5, 0, -1):
            alpha = 60 - i * 10
            glow_color = QColor(255, 215, 0, int(alpha))  # Gold
            painter.setPen(QPen(glow_color, i))
            painter.drawText(self.rect(), Qt.AlignCenter, "M")
        
        # Main icon
        icon_gradient = QLinearGradient(45, 45, 75, 75)
        icon_gradient.setColorAt(0, QColor(255, 255, 255))      # White
        icon_gradient.setColorAt(0.5, QColor(255, 240, 245))    # Very Light Pink
        icon_gradient.setColorAt(1, QColor(255, 215, 0))
        
        painter.setPen(QPen(QBrush(icon_gradient), 3))
        painter.drawText(self.rect(), Qt.AlignCenter, "M")

    def cleanup_animations(self):
        """Safely cleanup all premium animations"""
        self.is_animating = False
        
        if hasattr(self, 'pulse_timer') and self.pulse_timer.isActive():
            self.pulse_timer.stop()
        
        if hasattr(self, 'animation_group') and self.animation_group:
            try:
                if self.animation_group.state() == QPropertyAnimation.Running:
                    self.animation_group.stop()
                self.animation_group.deleteLater()
            except:
                pass
            finally:
                self.animation_group = None
        
        # Hide all buttons immediately
        for button in self.buttons:
            button.hide()

# ... (rest of your existing code remains exactly the same - firebase, activation, etc.)







        
# ---------- firebase init (service.json bundled inside exe) ----------
def get_service_json_path():
    """
    Returns the path to service.json whether running from source or PyInstaller exe.
    If bundled, loads from _MEIPASS (internal temp folder).
    """
    if getattr(sys, 'frozen', False):  # Running from PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    json_path = os.path.join(base_path, "voice.json")
    return json_path


def init_firebase_from_embedded(database_url=None):
    """
    Initializes Firebase from service.json (bundled inside exe or local dir).
    """
    path = get_service_json_path()
    
    if not os.path.exists(path):
        # Don't show message box here - we'll handle it in main after QApplication is created
        raise FileNotFoundError(f"Firebase service file not found: {path}")
    
    cred = credentials.Certificate(path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': database_url or 'https://mj-nova-default-rtdb.firebaseio.com/'
    })


# ---------- rest of your original app code (unchanged) ----------
def set_env_variable(key, value):
    """Permanently set a system environment variable"""
    try:
        subprocess.run(["setx", key, value], shell=True, check=True)
    except Exception as e:
        print(f"Failed to set environment variable: {e}")

def get_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("true", "1", "yes")
    return False

def prompt_access_key():
    key, ok = QInputDialog.getText(None, "Activation Required", "Enter your Access Key:")
    if ok and key.strip():
        return key.strip()
    return None

def prompt_user_name():
    while True:
        name, ok = QInputDialog.getText(
            None,
            "User Setup - NOVA AI",
            "Enter your name (for personalized greeting):"
        )
        if not ok:
            reply = QMessageBox.question(
                None,
                "Confirm",
                "No name entered. Use default 'User'?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                return "User"
            continue
        if name.strip():
            return name.strip()
        QMessageBox.warning(None, "Invalid", "Name cannot be empty.")

def prompt_lan():
    while True:
        name, ok = QInputDialog.getText(
            None,
            "Language Setup - NOVA AI", 
            "Enter the language you want to use:"
        )
        if not ok:
            reply = QMessageBox.question(
                None,
                "Confirm",
                "No Language Entered. Use default 'Hindi'?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                return "Hindi"
            continue
        if name.strip():
            return name.strip()
        QMessageBox.warning(None, "Invalid", "Language cannot be empty.")

def ensure_user_name():
    current = os.getenv("USER_NAME", "").strip()
    if current:
        return current
    
    # Show name prompt FIRST
    user_name = prompt_user_name()
    
    # Show language prompt SECOND
    mother_tongue = prompt_lan()
    
    # Set environment variables
    set_env_variable("USER_NAME", user_name)
    set_env_variable("LAN", mother_tongue)
    os.environ["USER_NAME"] = user_name
    os.environ["LAN"] = mother_tongue
    
    print(f"✅ User profile set: {user_name}, Language: {mother_tongue}")
    return user_name

BASE_SECRET = (
    "R7d9cQvPZ5mK2tYxW3nB8aJ4uH6sL1eT0gV9rC2pN7qD5fM8hK3zX1yU6jA4bS0i"
    "G7lE2oV9wQ5tR3nD8mC1kH6pJ4xZ0aY7"
)
PREMIUM_SECRET = (
    "N4kM8qS1vH6cL2xT9eR5jU3pA7zY0wD8fG2bC6nV4mK1tQ9rJ5hX3lS7oE0iP8aZ2"
    "Y6uW3dR9"
)
ELITE_SECRET = (
    "Z8xC1vB5nM2kL7jH3gF9dS4aA0pQ6wE2rT8yU1iO7lK3mN9cV5bX2zJ6hD4eR0tY8"
    "W3qP6uI1"
)

VARIANT_SECRET_MAP = {
    "base": BASE_SECRET,
    "premium": PREMIUM_SECRET,
    "elite": ELITE_SECRET,
}

VARIANT_NAMES = {
    "base": "Base",
    "premium": "Premium", 
    "elite": "Elite"
}

UPGRADE_PATHS = {
    "base": "premium",
    "premium": "elite",
    "elite": None  # No upgrade from elite
}

def detect_variant_and_ref(access_key):
    for variant in ["base", "premium", "elite"]:
        ref = db.reference(f"nova{variant}/{access_key}")
        record = ref.get()
        if record is not None:
            return variant, ref, record
    return None, None, None

def prompt_upgrade(current_variant):
    """Ask user if they want to upgrade to next tier"""
    next_variant = UPGRADE_PATHS.get(current_variant)
    
    if not next_variant:
        return False  # No upgrade available
    
    current_name = VARIANT_NAMES.get(current_variant, current_variant)
    next_name = VARIANT_NAMES.get(next_variant, next_variant)
    
    msg = QMessageBox()
    msg.setWindowTitle("Upgrade Available")
    msg.setText(f"You are currently using {current_name} version.\n\nWould you like to upgrade to {next_name} version?")
    msg.setIcon(QMessageBox.Question)
    
    upgrade_btn = QPushButton(f"Upgrade to {next_name}")
    no_btn = QPushButton("Continue with Current")
    
    msg.addButton(upgrade_btn, QMessageBox.AcceptRole)
    msg.addButton(no_btn, QMessageBox.RejectRole)
    
    msg.exec_()
    
    if msg.clickedButton() == upgrade_btn:
        return True
    return False

def process_upgrade(current_variant):
    """Handle the upgrade process"""
    next_variant = UPGRADE_PATHS.get(current_variant)
    if not next_variant:
        return False
    
    next_name = VARIANT_NAMES.get(next_variant, next_variant)
    
    # Prompt for upgrade key
    upgrade_key, ok = QInputDialog.getText(
        None, 
        f"Upgrade to {next_name}", 
        f"Enter your {next_name} Access Key:"
    )
    
    if not ok or not upgrade_key.strip():
        return False
    
    upgrade_key = upgrade_key.strip()
    
    # Verify upgrade key
    variant, ref, record = detect_variant_and_ref(upgrade_key)
    
    if not variant:
        QMessageBox.critical(None, "Error", f"Key '{upgrade_key}' not found in any variant.")
        return False
    
    if variant != next_variant:
        QMessageBox.critical(
            None, 
            "Error", 
            f"This key is for {VARIANT_NAMES.get(variant, variant)} version.\n"
            f"You need a {VARIANT_NAMES.get(next_variant, next_variant)} key for upgrade."
        )
        return False
    
    if get_bool(record.get("isUsed")):
        QMessageBox.critical(None, "Error", f"Key '{upgrade_key}' is already used on another device.")
        return False
    
    # Mark upgrade key as used
    try:
        ref.update({"isUsed": True})
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Failed to update key on server: {e}")
        return False
    
    # Update environment variables for new variant
    set_env_variable("ACCESS_KEY", upgrade_key)
    set_env_variable("IS_ACTIVATED", "true")
    set_env_variable("ACTIVATION_COUNT", "1")
    set_env_variable("NOVA_VARIANT", next_variant)
    set_env_variable("SYSTEM_CONST_32", VARIANT_SECRET_MAP[next_variant])
    
    os.environ["ACCESS_KEY"] = upgrade_key
    os.environ["IS_ACTIVATED"] = "true"
    os.environ["ACTIVATION_COUNT"] = "1"
    os.environ["NOVA_VARIANT"] = next_variant
    os.environ["SYSTEM_CONST_32"] = VARIANT_SECRET_MAP[next_variant]
    
    QMessageBox.information(
        None, 
        "Upgrade Successful", 
        f"Successfully upgraded to {next_name} version!\n"
        f"All features of {next_name} are now available."
    )
    
    return True

def activation_gate():
    access_key = os.getenv("ACCESS_KEY")
    is_activated = os.getenv("IS_ACTIVATED", "").strip().lower() == "true"
    current_variant = os.getenv("NOVA_VARIANT", "")
    
    try:
        activation_count = int(os.getenv("ACTIVATION_COUNT", "0").strip() or "0")
    except ValueError:
        activation_count = 0

    # Check if already activated and valid
    if is_activated and access_key and activation_count >= 1:
        secret = os.getenv("SYSTEM_CONST_32", "")
        if current_variant in VARIANT_SECRET_MAP and secret == VARIANT_SECRET_MAP[current_variant]:
            # Check if upgrade is available and prompt user
            if UPGRADE_PATHS.get(current_variant):
                if prompt_upgrade(current_variant):
                    if process_upgrade(current_variant):
                        # Successfully upgraded, continue with new variant
                        return True
                    else:
                        # Upgrade failed, continue with current variant
                        QMessageBox.information(
                            None,
                            "Upgrade Cancelled",
                            "Continuing with your current version."
                        )
            return True
        else:
            QMessageBox.critical(None, "Error", "This is incompatible version.")
            return False

    # New activation flow (existing code)
    if not access_key:
        access_key = prompt_access_key()
        if not access_key:
            QMessageBox.critical(None, "Error", "Access Key not provided. Exiting.")
            return False

    variant, ref, record = detect_variant_and_ref(access_key)
    if not variant:
        QMessageBox.critical(None, "Error", f"Key '{access_key}' not found in any variant.")
        return False

    if get_bool(record.get("isUsed")):
        QMessageBox.critical(None, "Error", f"Key '{access_key}' is already used on another device.")
        return False

    try:
        ref.update({"isUsed": True})
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Failed to update key on server: {e}")
        return False

    set_env_variable("ACCESS_KEY", access_key)
    set_env_variable("IS_ACTIVATED", "true")
    set_env_variable("ACTIVATION_COUNT", "1")
    set_env_variable("NOVA_VARIANT", variant)
    set_env_variable("SYSTEM_CONST_32", VARIANT_SECRET_MAP[variant])

    os.environ["ACCESS_KEY"] = access_key
    os.environ["IS_ACTIVATED"] = "true"
    os.environ["ACTIVATION_COUNT"] = "1"
    os.environ["NOVA_VARIANT"] = variant
    os.environ["SYSTEM_CONST_32"] = VARIANT_SECRET_MAP[variant]

    return True

def safe_activation_gate():
    try:
        if activation_gate():
            return True, "activated"
        else:
            return False, "failed"
    except Exception as e:
        print("Unexpected Activation Error:", e)
        print(traceback.format_exc())
        QMessageBox.warning(None, "Warning",
                            "Firebase se connect karte time error aaya.\n"
                            "App fallback mode me start ho raha hai.")
        return False, "fallback"




class WaitForInternetDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MJ - Waiting for Internet")
        self.setFixedSize(400, 150)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        layout = QVBoxLayout()
        
        self.message_label = QLabel("🔍 Checking internet connection...\nNOVA requires internet to start")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Infinite progress
        layout.addWidget(self.progress_bar)
        
        self.timer_label = QLabel("Next check in: 10 seconds")
        self.timer_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.timer_label)
        
        button_box = QDialogButtonBox()
        self.cancel_button = button_box.addButton("Cancel", QDialogButtonBox.RejectRole)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        self.cancel_button.clicked.connect(self.reject)
        
        # Setup timer
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_internet)
        self.seconds_remaining = 10
        
        # Start first check immediately
        QTimer.singleShot(1000, self.check_internet)
        
    def check_internet(self):
        """Check if internet is available"""
        if self.is_internet_available():
            self.message_label.setText("✅ Internet connected!\nStarting MJ...")
            self.progress_bar.setRange(0, 1)
            self.progress_bar.setValue(1)
            QTimer.singleShot(1000, self.accept)  # Close after 1 second
        else:
            self.seconds_remaining = 10
            self.message_label.setText("❌ No internet connection\nRetrying automatically...")
            self.start_countdown()
            
    def start_countdown(self):
        """Start 10 second countdown for next check"""
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)  # Update every second
        
    def update_countdown(self):
        """Update countdown timer"""
        self.seconds_remaining -= 1
        self.timer_label.setText(f"Next check in: {self.seconds_remaining} seconds")
        
        if self.seconds_remaining <= 0:
            self.countdown_timer.stop()
            self.check_internet()  # Check again
            
    def is_internet_available(self):
        """Simple internet connectivity check"""
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return True
        except:
            try:
                socket.create_connection(("google.com", 80), timeout=5)
                return True
            except:
                return False

def wait_for_internet():
    """Wait for internet connection with auto-retry"""
    dialog = WaitForInternetDialog()
    result = dialog.exec_()
    return result == QDialog.Accepted




def start_nova_interface(app):
    """Start the MJ AI interface - FIXED VERSION"""
    print("🚀 Starting MJ AI Interface...")
    
    # Show full screen scanning animation first
    scanning_window = ScanningAnimation()
    scanning_window.show()
    print("🔍 Scanning animation started")
    
    def show_main_window():
        scanning_window.close()
        print("🔄 Switching to main floating window...")
        
        main_window = ModernFloatingWindow()
        main_window.show()
        
        # Force window to be on top and active
        main_window.raise_()
        main_window.activateWindow()
        main_window.setFocus()
        
        print("✅ MJ AI Interface Started Successfully")
        print("📍 Floating window should be visible at the top center of your screen")
        print("💡 Hover your mouse over the circular 'M' button to see options!")
        print("🖱️ You can drag the window by clicking and dragging the main circle")
        print("❌ Press Alt+F4 or use task manager to close the application")
        
        # Test: Force a repaint after 1 second
        QTimer.singleShot(1000, lambda: main_window.repaint())
        
    # Use singleShot to schedule main window after scanning
    QTimer.singleShot(3500, show_main_window)

def main():
    """URGENT FIX - Firebase Verification BEFORE UI Launch"""
    app = None
    
    try:
        # Initialize QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("MJ AI")
        app.setApplicationVersion("4.0")
        
        # Prevent app from quitting when last window closes
        app.setQuitOnLastWindowClosed(False)
        
        print("🚀 STARTING MJ AI - PREMIUM EDITION")
        
        # STEP 1: Show welcome message
        QMessageBox.information(None, "MJ AI PREMIUM", 
                               "🚀 MJ AI LOVELY EDITION Starting...\n\n"
                               "Experience the future of AI assistance!\n"
                               "Make sure you are connected to the Internet!")
        
        # STEP 2: Wait for internet connection FIRST
        print("🔍 Checking internet connection...")
        if not wait_for_internet():
            QMessageBox.critical(None, "Error", "Internet connection required. Exiting.")
            return 1
        
        # STEP 3: Initialize Firebase and verify activation
        print("🔑 Initializing Firebase and verifying activation...")
        try:
            init_firebase_from_embedded()
        except Exception as e:
            QMessageBox.critical(None, "Firebase Error", f"Failed to initialize Firebase: {e}")
            return 1
        
        # STEP 4: Run activation gate - THIS MUST COMPLETE BEFORE UI
        print("🔐 Running activation verification...")
        activation_success, status = safe_activation_gate()
        
        if not activation_success:
            if status == "failed":
                QMessageBox.critical(None, "Activation Failed", "Activation verification failed. Exiting.")
                return 1
            elif status == "fallback":
                # Continue in fallback mode
                QMessageBox.warning(None, "Fallback Mode", 
                                   "Running in limited fallback mode.\nSome features may not work.")
        
        # STEP 5: 🔥 CRITICAL FIX - Ensure user name is set BEFORE UI
        print("👤 Setting up user profile...")
        user_name = ensure_user_name()  # 🔥 YEH LINE ADD KARNA HAI
        print(f"✅ User profile set: {user_name}")
        
        # STEP 6: ONLY AFTER ALL VERIFICATIONS - Show UI
        print("🎨 Launching premium UI...")
        
        # Show ULTRA PREMIUM scanning animation
        scanning_window = ScanningAnimation()
        scanning_window.show()
        
        # Create premium main window
        main_window = ModernFloatingWindow()
        
        def show_main_and_keep_alive():
            print("🔄 Transitioning to premium main window...")
            scanning_window.close()
            
            # Show and activate premium main window
            main_window.show()
            main_window.raise_()
            main_window.activateWindow()
            
            # Force focus and prevent minimization
            main_window.setWindowFlags(main_window.windowFlags() | Qt.WindowStaysOnTopHint)
            main_window.show()
            
            print("✅ PREMIUM MAIN WINDOW SHOULD BE VISIBLE NOW!")
            print("📍 Look for the LOVELY circular interface at screen center")
            print("💫 Hover over the glowing 'M' to reveal premium controls")
            print(f"👤 Welcome, {user_name}!")  # 🔥 YEH BHI ADD KARNA HAI
            
            # Keep checking window status
            def check_window_status():
                if main_window.isVisible():
                    print("🎯 Premium window active - EXCELLENT!")
                else:
                    print("❌ Window lost - RESTORING LOVELY INTERFACE!")
                    main_window.show()
                    main_window.raise_()
            
            # Check every 5 seconds
            status_timer = QTimer()
            status_timer.timeout.connect(check_window_status)
            status_timer.start(5000)
        
        # Show main window after scanning with delay
        QTimer.singleShot(3500, show_main_and_keep_alive)
        
        print("🔄 Starting LOVELY EVENT LOOP...")
        result = app.exec_()
        print(f"🔚 Application properly exited: {result}")
        return result
        
    except Exception as e:
        print(f"❌ LOVELY ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        if app:
            app.processEvents()

if __name__ == "__main__":
    # Force the application to stay alive
    import os
    os._exit(main())


