import sys
import math
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QGroupBox, QSlider,
                            QGraphicsView, QGraphicsScene, QGridLayout)
from PyQt6.QtCore import Qt, QTimer, QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath, QFont
from emotions import get_emotion_data, get_available_emotions, EYEBROW_SHAPES, MOUTH_SHAPES
from eye_drawing import EyeRenderer



# Constants
WIDTH = 600
HEIGHT = 500

class AnimationController:
    def __init__(self):
        self.frame = 0
        self.blink_interval = random.randint(50, 150)
        self.blink_duration = 10
        self.breath_speed = 0.03
        self.head_move_speed = 0.02
        self.talk_counter = 0
        self.emotion = "neutral"
        self.talking = False
        self.breath_offset = 0
        self.head_offset_x = 0
        self.head_offset_y = 0
        self.blink_factor = 0
        self.talk_factor = 0
        self.eye_renderer = EyeRenderer(self)
        
    def update(self):
        self.frame += 1
        
        # Calculate breathing animation
        self.breath_offset = 2 * math.sin(self.frame * self.breath_speed)
        
        # Calculate head movement
        self.head_offset_x = 2 * math.sin(self.frame * self.head_move_speed)
        self.head_offset_y = 1 * math.sin(self.frame * self.head_move_speed * 0.7)
        
        # Calculate blink animation
        if self.frame % self.blink_interval < self.blink_duration:
            self.blink_factor = math.sin((self.frame % self.blink_duration) * 
                                       math.pi / self.blink_duration)
        else:
            self.blink_factor = 0
            
        # Adjust blink interval
        if self.frame % self.blink_interval == 0:
            self.blink_interval = random.randint(50, 150)
        
        # Calculate talk animation
        if self.talking:
            if self.talk_counter <= 0:
                self.talk_counter = random.randint(20, 40)
            
            if self.talk_counter % 10 < 3:
                self.talk_factor = 0.8 * math.sin(self.talk_counter * 0.5)
            elif self.talk_counter % 10 < 7:
                self.talk_factor = 0.7 + 0.1 * math.sin(self.talk_counter * 0.2)
            else:
                self.talk_factor = 0.3 * math.sin(self.talk_counter * 0.4)
            
            self.talk_factor += random.uniform(-0.05, 0.05)
            self.talk_factor = max(0, min(1, self.talk_factor))
            
            self.talk_counter -= 1
            if self.talk_counter <= 0:
                self.talk_counter = 0
        else:
            self.talk_factor = 0

class QtCharacterRenderer:
    def __init__(self, controller):
        self.controller = controller
        self.width = WIDTH
        self.height = HEIGHT
        self.wripp_spp = 15  # Bezier curve sampling
        self.last_ctrl2 = None  # For smooth curves
        self.Xh = 0  # For Smooth curves
        self.Yh = 0  # For Smooth curves
        self.eye_renderer = EyeRenderer(self)
        
    def convert_x(self, x):
        """Convert x from turtle coords to Qt coords"""
        return x
        
    def convert_y(self, y):
        """Convert y from turtle coords to Qt coords"""
        # Fix: Invert Y coordinate to display right-side up
        return y
        
    def convert_point(self, x, y):
        """Convert point from turtle coords to Qt coords"""
        return QPointF(self.convert_x(x), self.convert_y(y))
        
    def moveto(self, path, x, y):
        """Move to position without drawing"""
        path.moveTo(self.convert_point(x, y))
        
    def lineto(self, path, x, y):
        """Line to absolute position"""
        path.lineTo(self.convert_point(x, y))

    def relative_lineto(self, path, dx, dy):
        """Line to relative position"""
        current = path.currentPosition()
        path.lineTo(current + QPointF(dx, dy))  # Fixed: don't invert dy

    def horizontal(self, path, x):
        """Horizontal line to absolute x position"""
        current = path.currentPosition()
        path.lineTo(QPointF(self.convert_x(x), current.y()))

    def vertical(self, path, dy):
        """Vertical line relative"""
        current = path.currentPosition()
        path.lineTo(QPointF(current.x(), current.y() + dy))  # Fixed: don't invert dy

    def curveto_r(self, path, dx1, dy1, dx2, dy2, dx, dy):
        """Add relative cubic bezier curve"""
        current = path.currentPosition()
        ctrl1 = current + QPointF(dx1, dy1)  # Fixed: don't invert dy values
        ctrl2 = current + QPointF(dx2, dy2)
        end = current + QPointF(dx, dy)
        
        path.cubicTo(ctrl1, ctrl2, end)
        self.Xh = dx - dx2
        self.Yh = dy - dy2
        
    def smooth_r(self, path, dx2, dy2, dx, dy):
        """Add smooth relative cubic bezier curve"""
        current = path.currentPosition()
        
        # First control point is reflection of previous second control point
        ctrl1 = current + QPointF(self.Xh, self.Yh)  # Fixed: don't invert Yh
        ctrl2 = current + QPointF(dx2, dy2)
        end = current + QPointF(dx, dy)
        
        path.cubicTo(ctrl1, ctrl2, end)
        self.Xh = dx - dx2
        self.Yh = dy - dy2
    
    def curveto(self, path, x1, y1, x2, y2, x, y):
        """Add absolute cubic bezier curve"""
        current = path.currentPosition()
        ctrl1 = self.convert_point(x1, y1)
        ctrl2 = self.convert_point(x2, y2)
        end = self.convert_point(x, y)
        
        path.cubicTo(ctrl1, ctrl2, end)
        self.Xh = x - x2
        self.Yh = y - y2
    
    def draw_coat(self, painter, offset_y=0):
        """Draw the character's coat"""
        painter.setPen(QPen(QColor("black"), 1))
        painter.setBrush(QBrush(QColor("#F2F2F2")))
        
        path = QPainterPath()
        self.moveto(path, 61, 462 + offset_y)
        self.Xh = self.Yh = 0
        
        # Coat outline
        self.smooth_r(path, 12, -41, 27, -58)
        self.curveto_r(path, -6, -36, 6, -118, 9, -132)
        self.curveto_r(path, -15, -27, -23, -51, -26, -74)
        self.curveto_r(path, 4, -66, 38, -105, 65, -149)
        self.horizontal(path, 486)
        self.curveto_r(path, 12, 24, 40, 99, 33, 114)
        self.curveto_r(path, 39, 82, 55, 129, 39, 144)
        self.smooth_r(path, -31, 23, -39, 28)
        self.smooth_r(path, -12, 37, -12, 37)
        self.relative_lineto(path, 50, 92)
        self.horizontal(path, 445)
        self.smooth_r(path, -29, -38, -31, -46)
        self.smooth_r(path, 78, -107, 72, -119)
        self.curveto(path, 355, 178, 340, 176, 340, 176)
        self.curveto(path, 272, 63, 264, 64, 264, 64)
        self.smooth_r(path, -29, 67, -27, 73)
        self.curveto(path, 99, 292, 174, 428, 173, 439)
        self.smooth_r(path, -8, 23, -8, 23)
        self.lineto(path, 61, 462 + offset_y)
        
        painter.drawPath(path)
        
        # Coat shadow
        shadow_path = QPainterPath()
        self.moveto(shadow_path, 60.5, 461.5 + offset_y)
        self.Xh = self.Yh = 0
        painter.setBrush(QBrush(QColor("#D3DFF0")))
        
        self.curveto_r(shadow_path, 0, 0, 17, -42, 27, -59)
        self.curveto_r(shadow_path, -6, -33, 6, -128, 10, -133)
        self.curveto_r(shadow_path, -15, -10, -27, -66, -27.285, -75)
        
        painter.setPen(QPen(QColor("#D3DFF0"), 1))
        self.curveto_r(shadow_path, 12.285, 11, 82.963, 156, 82.963, 156)
        painter.setPen(QPen(QColor("black"), 1))
        
        self.smooth_r(shadow_path, 12.322, 75, 19.322, 86)
        self.curveto_r(shadow_path, -1, 11, -8, 25, -8, 25)
        self.horizontal(shadow_path, 60.5)
        
        painter.drawPath(shadow_path)
        
        # More coat parts
        more_path = QPainterPath()
        self.moveto(more_path, 444.5, 464 + offset_y)
        self.Xh = self.Yh = 0
        
        self.curveto_r(more_path, 0, 0, -29, -36, -31, -46)
        self.smooth_r(more_path, 53.59, -82.337, 53.59, -82.337)
        
        painter.setPen(QPen(QColor("#D3DFF0"), 1))
        self.smooth_r(more_path, 86.41, -47.663, 96.072, -54.85)
        self.curveto(more_path, 563.5, 297.5, 570.5, 299.5, 518.5, 334)
        
        painter.setPen(QPen(QColor("black"), 1))
        self.curveto_r(more_path, -2, 16, -12, 33, -12, 37)
        self.smooth_r(more_path, 50, 92, 50, 93)
        self.horizontal(more_path, 444.5)
        
        painter.drawPath(more_path)
        
    def draw_jacket_inside(self, painter, offset_y=0):
        """Draw the inside of the jacket"""
        painter.setPen(QPen(QColor("black"), 1))
        painter.setBrush(QBrush(QColor("#2b1d2a")))
        
        # Left side
        path = QPainterPath()
        self.moveto(path, 225, 462 + offset_y)
        self.Xh = self.Yh = 0
        
        self.horizontal(path, 165)
        self.smooth_r(path, 9, -15, 8, -25)
        self.curveto_r(path, -47, -126, 6, -212, 12, -225)
        self.curveto(path, 185, 305, 202, 428, 225, 462 + offset_y)
        
        painter.drawPath(path)
        
        # Right side
        right_path = QPainterPath()
        self.moveto(right_path, 390, 462 + offset_y)
        self.Xh = self.Yh = 0
        
        self.curveto_r(right_path, 10, -23, 34, -180, 35, -222)
        self.curveto_r(right_path, 7, 4, 54, 45, 61, 61)
        self.smooth_r(right_path, -73, 101, -72, 118)
        self.curveto_r(right_path, 5, 15, 31, 46, 31, 45)
        self.lineto(right_path, 390, 462 + offset_y)
        
        painter.drawPath(right_path)
        
        # Center part
        painter.setBrush(QBrush(QColor("#2b1d29")))
        center_path = QPainterPath()
        self.moveto(center_path, 225, 462 + offset_y)
        self.Xh = self.Yh = 0
        
        self.curveto_r(center_path, -28, -50, -40, -166, -40, -250)
        self.curveto_r(center_path, 6, 51, -6, 87, 45, 106)
        self.smooth_r(center_path, 64, 27, 89, 24)
        self.smooth_r(center_path, 49, -18, 56, -20)
        self.smooth_r(center_path, 50, -10, 51, -85)
        self.curveto_r(center_path, 0, 29, -25, 201, -36, 225)
        self.lineto(center_path, 225, 462 + offset_y)
        
        painter.drawPath(center_path)
    
    def draw_clothes(self, painter, offset_y=0):
        """Draw the character's clothes"""
        painter.setPen(QPen(QColor("black"), 1))
        painter.setBrush(QBrush(QColor("#3D3D3D")))
        
        path = QPainterPath()
        self.moveto(path, 225, 462 + offset_y)
        self.Xh = self.Yh = 0
        
        self.curveto_r(path, -5, -5, -22, -53, -23, -70)
        self.relative_lineto(path, 32, -13)
        self.curveto_r(path, 3, -25, 6, -28, 12, -36)
        self.smooth_r(path, 13, -12, 16, -12)
        self.vertical(path, -2)
        self.curveto_r(path, 45, 20, 64, 14, 94, 1)
        self.vertical(path, 2)
        self.curveto_r(path, 8, -2, 15, 2, 17, 4)
        self.smooth_r(path,0, 6, -2, 9)
        self.curveto_r(path, 10, 10, 10, 29, 11, 33)
        self.smooth_r(path, 23, 4, 25, 6)
        self.smooth_r(path, -17, 83, -17, 78)
        self.lineto(path, 225, 462 + offset_y)
        
        painter.drawPath(path)
    
    def draw_neck(self, painter, offset_y=0):
        """Draw the character's neck"""
        painter.setPen(QPen(QColor("black"), 1))
        painter.setBrush(QBrush(QColor("#968281")))
        
        path = QPainterPath()
        self.moveto(path, 262, 329 + offset_y)
        self.Xh = self.Yh = 0
        
        self.vertical(path, 17)
        self.curveto_r(path, 1, 2, 44, 14, 45, 15)
        self.smooth_r(path, 3, 12, 3, 12)
        self.horizontal(path, 313)  # 310 + 3
        self.vertical(path, -5)
        self.curveto_r(path, 1, -3, 4, -6, 5, -7)
        self.relative_lineto(path, 36, -14)
        self.curveto_r(path, 1, -1, 3, -16, 2, -17)
        self.curveto(path, 318, 348 + offset_y, 296, 344 + offset_y, 262, 329 + offset_y)
        
        painter.drawPath(path)
        
    def draw_collar(self, painter, offset_y=0):
        """Draw the character's collar"""
        painter.setPen(QPen(QColor("black"), 1))
        painter.setBrush(QBrush(QColor("#A2B8D6")))
        
        path = QPainterPath()
        self.moveto(path, 262, 331 + offset_y)
        self.Xh = self.Yh = 0
        
        self.curveto_r(path, 0, 8, -1, 13, 0, 15)
        self.smooth_r(path, 43, 14, 45, 15)
        self.relative_lineto(path, 3, 12)
        self.horizontal(path, 313)  # 310 + 3
        self.smooth_r(path, -1, -3, 0, -5)
        self.relative_lineto(path, 5, -7)
        self.relative_lineto(path, 36, -14)
        self.curveto_r(path, 1, -1, 2, -12, 2, -15)
        self.smooth_r(path, 25, -2, 15, 13)
        self.curveto_r(path, -2, 4, -7, 29, -7, 32)
        self.smooth_r(path, -35, 19, -41, 22)
        self.smooth_r(path, -9, 14, -12, 14)
        self.smooth_r(path, -7, -12, -14, -15)
        self.curveto_r(path, -19, -2, -41, -25, -41, -25)
        self.smooth_r(path, -10, -26, -10, -30)
        self.curveto(path, 255, 332 + offset_y, 262, 331 + offset_y, 262, 331 + offset_y)
        
        painter.drawPath(path)
        
        # Draw collar line details
        painter.setPen(QPen(QColor("black"), 1))
        line_path = QPainterPath()
        self.moveto(line_path, 262, 346 + offset_y)
        self.relative_lineto(line_path, -12, -6)
        painter.drawPath(line_path)
        
        curve_path = QPainterPath()
        self.moveto(curve_path, 369, 333 + offset_y)
        self.Xh = self.Yh = 0
        self.curveto_r(curve_path, 2, 4, -6, 10, -15, 14)
        painter.drawPath(curve_path)
        
        # Collar through bow tie parts
        painter.setBrush(QBrush(QColor("#A2B8D6")))
        
        left_path = QPainterPath()
        self.moveto(left_path, 297, 387 + offset_y)
        self.Xh = self.Yh = 0
        self.relative_lineto(left_path, -11, 6)
        self.curveto_r(left_path, -1, 0, -20, -7, -30, -19)
        self.curveto(left_path, 259, 373 + offset_y, 297, 385 + offset_y, 297, 387 + offset_y)
        painter.drawPath(left_path)
        
        right_path = QPainterPath()
        self.moveto(right_path, 323, 384 + offset_y)
        self.Xh = self.Yh = 0
        self.relative_lineto(right_path, 8, 7)
        self.relative_lineto(right_path, 30, -14)
        self.curveto_r(right_path, 1, -1, 5, -6, 4, -7)
        self.curveto(right_path, 329, 379 + offset_y, 323, 384 + offset_y, 323, 384 + offset_y)
        painter.drawPath(right_path)
    
    def draw_tie(self, painter, offset_y=0):
        """Draw the character's tie"""
        painter.setPen(QPen(QColor("black"), 1))
        painter.setBrush(QBrush(QColor("#151515")))
        
        path = QPainterPath()
        self.moveto(path, 247, 358 + offset_y)
        self.Xh = self.Yh = 0
        
        self.curveto_r(path, -5, 3, -8, 20, -6, 23)
        self.curveto_r(path, 25, 21, 50, 17, 50, 17)
        self.relative_lineto(path, -23, 64)
        self.horizontal(path, 291)  # 269 + 22
        self.smooth_r(path, 1, -13, 2, -16)
        self.relative_lineto(path, 13, -50)
        self.curveto_r(path, 2, 2, 7, 3, 10, 1)
        self.smooth_r(path, 18, 65, 18, 65)
        self.horizontal(path, 334)  # 315 + 19
        self.relative_lineto(path, -24, -65)
        self.curveto_r(path, 21, 5, 39, -10, 44, -13)
        self.curveto_r(path, 5, -20, 1, -21, 0, -24)
        self.curveto_r(path, -18, -2, -49, 15, -52, 17)
        self.smooth_r(path, -11, -3, -15, -1)
        self.curveto(path, 252, 356 + offset_y, 247, 358 + offset_y, 247, 358 + offset_y)
        
        painter.drawPath(path)
    
    def draw_face(self, painter, offset_x=0, offset_y=0):
        """Draw the character's face"""
        painter.setPen(QPen(QColor("black"), 1))
        painter.setBrush(QBrush(QColor("#F3EEEB")))
        
        path = QPainterPath()
        self.moveto(path, 185 + offset_x, 212 + offset_y)
        self.Xh = self.Yh = 0
        
        self.curveto_r(path, 4, -9, 46, -77, 52, -75)
        self.curveto_r(path, -2, -17, 19, -68, 27, -73)
        self.curveto_r(path, 16, 15, 71, 108, 76, 112)
        self.smooth_r(path, 76, 53, 86, 60)
        self.curveto_r(path, 0, 65, -27, 75, -31, 76)
        self.curveto_r(path, -50, 28, -70, 30, -85, 30)
        self.smooth_r(path, -77, -22, -86, -26)
        self.curveto(path, 180 + offset_x, 302 + offset_y, 186 + offset_x, 228 + offset_y, 185 + offset_x, 212 + offset_y)
        
        painter.drawPath(path)
    
    def draw_hair(self, painter, offset_x=0, offset_y=0):
        """Draw the character's hair"""
        painter.setPen(QPen(QColor("black"), 1))
        painter.setBrush(QBrush(QColor("#2B1D29")))
        
        # First part
        path1 = QPainterPath()
        self.moveto(path1, 189 + offset_x, 202 + offset_y)
        self.Xh = self.Yh = 0
        self.curveto_r(path1, -1, 22, 19, 51, 19, 51)
        self.smooth_r(path1, -10, -42, 7, -92)
        self.curveto(path1, 212 + offset_x, 168 + offset_y, 196 + offset_x, 189 + offset_y, 189 + offset_x, 202 + offset_y)
        painter.drawPath(path1)
        
        # Second part
        path2 = QPainterPath()
        self.moveto(path2, 221 + offset_x, 155 + offset_y)
        self.Xh = self.Yh = 0
        self.curveto_r(path2, -2, 6, 5, 48, 5, 48)
        self.smooth_r(path2, 18, -28, 20, -48)
        self.curveto_r(path2, -5, 24, 4, 43, 7, 50)
        self.curveto_r(path2, -10, -49, 3, -72, 13, -106)
        self.curveto_r(path2, -2, -7, -3, -32, -3, -35)
        self.curveto_r(path2, -17, 18, -27, 71, -27, 71)
        self.lineto(path2, 221 + offset_x, 155 + offset_y)
        painter.drawPath(path2)
        
        # Third part
        path3 = QPainterPath()
        self.moveto(path3, 264 + offset_x, 64 + offset_y)
        self.Xh = self.Yh = 0
        self.curveto_r(path3, -4, 5, 14, 100, 14, 100)
        self.smooth_r(path3, -6, -79, -5, -85)
        self.curveto_r(path3, 0, 98, 49, 139, 49, 139)
        self.smooth_r(path3, 8, -50, 3, -65)
        self.curveto(path3, 272 + offset_x, 64 + offset_y, 264 + offset_x, 64 + offset_y, 264 + offset_x, 64 + offset_y)
        painter.drawPath(path3)
        
        # Fourth part
        path4 = QPainterPath()
        self.moveto(path4, 342 + offset_x, 176 + offset_y)
        self.Xh = self.Yh = 0
        self.curveto_r(path4, -1, 27, -10, 57, -10, 57)
        self.smooth_r(path4, 20, -33, 17, -54)
        self.lineto(path4, 342 + offset_x, 176 + offset_y)
        painter.drawPath(path4)
        
        # Fifth part (polyline)
        path5 = QPainterPath()
        self.moveto(path5, 349 + offset_x, 180 + offset_y)
        self.lineto(path5, 353 + offset_x, 203 + offset_y)
        self.lineto(path5, 361 + offset_x, 203 + offset_y)
        self.lineto(path5, 362 + offset_x, 188 + offset_y)
        self.lineto(path5, 349 + offset_x, 180 + offset_y)
        painter.drawPath(path5)
    
    def draw_eyebrows(self, painter, offset_x=0, offset_y=0):
        """Draw the character's eyebrows"""
        emotion_data = get_emotion_data(self.controller.emotion)
        eyebrow_shape = EYEBROW_SHAPES[emotion_data.eyebrow_type]
        
        painter.setPen(QPen(QColor("black"), 2))
        
        # Left eyebrow
        left_path = QPainterPath()
        self.moveto(left_path, 210 + offset_x, eyebrow_shape.left_start_y + offset_y)
        self.Xh = self.Yh = 0
        
        for curve_params in eyebrow_shape.left_curve:
            self.curveto_r(left_path, *curve_params)
        
        painter.drawPath(left_path)
        
        # Right eyebrow
        right_path = QPainterPath()
        self.moveto(right_path, 338 + offset_x, eyebrow_shape.right_start_y + offset_y)
        self.Xh = self.Yh = 0
        
        for curve_params in eyebrow_shape.right_curve:
            self.curveto_r(right_path, *curve_params)
        
        painter.drawPath(right_path)
        
    def draw_eyes(self, painter, offset_x=0, offset_y=0):
        """Draw the character's eyes using the EyeRenderer"""
        emotion_data = get_emotion_data(self.controller.emotion)
        self.eye_renderer.draw_eyes(painter, offset_x, offset_y, 
                                self.controller.blink_factor, emotion_data)
    
    def draw_nose(self, painter, offset_x=0, offset_y=0):
        """Draw the character's nose"""
        painter.setPen(QPen(QColor("black"), 1))
        
        nose_path = QPainterPath()
        self.moveto(nose_path, 309 + offset_x, 270 + offset_y)
        self.Xh = self.Yh = 0
        
        self.curveto_r(nose_path, 0, 0, 4, 7, 1, 9)
        painter.drawPath(nose_path)
    
    def draw_mouth(self, painter, offset_x=0, offset_y=0):
        """Draw the mouth with talk animation"""
        emotion_data = get_emotion_data(self.controller.emotion)
        mouth_shape = MOUTH_SHAPES[emotion_data.mouth_type]
        
        painter.setPen(QPen(QColor("black"), 1))
        
        if self.controller.talk_factor > 0:
            # Talking mouth
            talking_data = mouth_shape.talking
            path = QPainterPath()
            self.moveto(path, talking_data.start_x + offset_x, 
                       talking_data.start_y + offset_y)
            self.Xh = self.Yh = 0
            
            painter.setBrush(QBrush(QColor("black")))
            
            # Draw upper lip with animation
            for curve_type, *params in talking_data.upper_lip:
                if curve_type == "curveto_r":
                    adjusted_params = []
                    for i, param in enumerate(params):
                        if i % 2 == 1:  # Y coordinates
                            adjusted_params.append(param + (self.controller.talk_factor * 4))
                        else:
                            adjusted_params.append(param)
                    self.curveto_r(path, *adjusted_params)
            
            # Draw right corner
            if talking_data.corners and len(talking_data.corners) > 0:
                corner_type, *corner_params = talking_data.corners[0]
                if corner_type == "curveto_r":
                    adjusted_params = []
                    for i, param in enumerate(corner_params):
                        if i % 2 == 1 and i > 2:  # Y coordinates after first pair
                            adjusted_params.append(param + (self.controller.talk_factor * 4))
                        else:
                            adjusted_params.append(param)
                    self.curveto_r(path, *adjusted_params)
            
            # Draw lower lip
            for curve_type, *params in talking_data.lower_lip:
                if curve_type == "curveto_r":
                    adjusted_params = []
                    for i, param in enumerate(params):
                        if i % 2 == 1:  # Y coordinates
                            adjusted_params.append(param + (self.controller.talk_factor * 6))
                        else:
                            adjusted_params.append(param)
                    self.curveto_r(path, *adjusted_params)
            
            # Draw left corner
            if talking_data.corners and len(talking_data.corners) > 1:
                corner_type, *corner_params = talking_data.corners[1]
                if corner_type == "curveto_r":
                    adjusted_params = []
                    for i, param in enumerate(corner_params):
                        if i % 2 == 1 and i > 2:  # Y coordinates after first pair
                            adjusted_params.append(param + (self.controller.talk_factor * 4))
                        else:
                            adjusted_params.append(param)
                    self.curveto_r(path, *adjusted_params)
            
            path.closeSubpath()
            painter.drawPath(path)
            
            # Draw inner detail if available
            if talking_data.inner_detail and self.controller.talk_factor > 0.5:
                painter.setBrush(QBrush(QColor(talking_data.inner_detail["color"])))
                inner_path = QPainterPath()
                self.moveto(inner_path, 298 + offset_x,
                           310 + offset_y + self.controller.talk_factor*3)
                self.Xh = self.Yh = 0
                
                for curve_type, *params in talking_data.inner_detail["curves"]:
                    if curve_type == "curveto_r":
                        self.curveto_r(inner_path, *params)
                
                inner_path.closeSubpath()
                painter.drawPath(inner_path)
                painter.setBrush(Qt.BrushStyle.NoBrush)
        else:
            # Closed mouth
            closed_data = mouth_shape.closed
            path = QPainterPath()
            self.moveto(path, closed_data.start_x + offset_x, 
                       closed_data.start_y + offset_y)
            self.Xh = self.Yh = 0
            
            if len(closed_data.curves) > 1:
                painter.setBrush(QBrush(QColor("black")))
            
            for curve_type, *params in closed_data.curves:
                if curve_type == "curveto_r":
                    self.curveto_r(path, *params)
                elif curve_type == "horizontal":
                    self.horizontal(path, self.convert_x(path.currentPosition().x()) + params[0])
            
            if len(closed_data.curves) > 1:
                path.closeSubpath()
            
            painter.drawPath(path)
            painter.setBrush(Qt.BrushStyle.NoBrush)
    
    def draw_special_effects(self, painter, offset_x=0, offset_y=0):
        """Draw special effects based on emotion"""
        emotion_data = get_emotion_data(self.controller.emotion)
        
        for effect in emotion_data.special_effects:
            if effect == "blush":
                self.draw_blush(painter, offset_x, offset_y)
            elif effect == "sweat_drop" and random.random() < 0.05:
                self.draw_sweat_drop(painter, offset_x, offset_y)
            elif effect == "vein_mark" and random.random() < 0.03:
                self.draw_vein_mark(painter, offset_x, offset_y)
            elif effect == "swirl_mark" and random.random() < 0.07:
                self.draw_swirl_mark(painter, offset_x, offset_y)
            elif effect == "tears":
                self.draw_tears(painter, offset_x, offset_y)
    
    def draw_blush(self, painter, offset_x=0, offset_y=0):
        """Draw blush effect"""
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(255, 183, 183, 150)))  # Semi-transparent pink
        
        # Left cheek
        left_center = self.convert_point(230 + offset_x, 272 + offset_y)
        painter.drawEllipse(left_center, 12, 8)
        
        # Right cheek
        right_center = self.convert_point(365 + offset_x, 272 + offset_y)
        painter.drawEllipse(right_center, 12, 8)
    
    def draw_sweat_drop(self, painter, offset_x=0, offset_y=0):
        """Draw sweat drop for nervous emotions"""
        painter.setPen(QPen(QColor("black"), 1))
        painter.setBrush(QBrush(QColor("#A0D8FF")))
        
        path = QPainterPath()
        self.moveto(path, 390 + offset_x, 180 + offset_y)
        self.Xh = self.Yh = 0
        
        self.curveto_r(path, 2, -5, 6, -10, 3, -15)
        self.curveto_r(path, -4, -2, -8, -1, -10, 5)
        self.curveto_r(path, 1, 5, 5, 8, 7, 10)
        path.closeSubpath()
        
        painter.drawPath(path)
    
    def draw_vein_mark(self, painter, offset_x=0, offset_y=0):
        """Draw vein mark for angry emotion"""
        painter.setPen(QPen(QColor("#FF5555"), 2))
        
        start = self.convert_point(185 + offset_x, 180 + offset_y)
        painter.save()
        painter.translate(start)
        
        for i in range(3):
            painter.drawLine(QPointF(0, 0), QPointF(8, 0))
            painter.rotate(60)
            painter.drawLine(QPointF(8, 0), QPointF(8, 5))
            painter.rotate(-120)
        
        painter.restore()
    
    def draw_swirl_mark(self, painter, offset_x=0, offset_y=0):
        """Draw swirl mark for confused emotion"""
        painter.setPen(QPen(QColor("#5555FF"), 2))
        
        path = QPainterPath()
        start = self.convert_point(200 + offset_x, 160 + offset_y)
        path.moveTo(start)
        
        # Create a spiral
        for i in range(12):
            angle = i * 30 * math.pi / 180
            radius = 5 + i * 0.5
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            path.lineTo(start.x() + x, start.y() - y)
        
        painter.drawPath(path)
    
    def draw_tears(self, painter, offset_x=0, offset_y=0):
        """Draw tears for crying emotion"""
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(160, 216, 255, 200)))  # Semi-transparent blue
        
        tear_positions = [
            (235, 240, 16),  # Left eye tears
            (250, 250, 12),
            (360, 245, 14),  # Right eye tears
            (375, 255, 10),
        ]
        
        for x, y, length in tear_positions:
            path = QPainterPath()
            self.moveto(path, x + offset_x, y + offset_y)
            self.Xh = self.Yh = 0
            
            # Teardrop shape
            self.curveto_r(path, 2, 2, 4, length-5, 0, length)
            self.curveto_r(path, -4, 0, -6, -5, -4, -length)
            path.closeSubpath()
            
            painter.drawPath(path)
    
    def draw(self, painter):
        """Main drawing function"""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Clear background
        painter.fillRect(0, 0, self.width, self.height, QColor("white"))
        
        # Translate to center the character
        painter.translate(self.width/2 - 300, self.height/2 - 250)
        
        # Draw character parts in order
        offset_x = self.controller.head_offset_x
        offset_y = self.controller.head_offset_y + self.controller.breath_offset
        
        # Body parts (not affected by head movement)
        self.draw_coat(painter, self.controller.breath_offset)
        self.draw_jacket_inside(painter, self.controller.breath_offset)
        self.draw_clothes(painter, self.controller.breath_offset)
        self.draw_neck(painter, self.controller.breath_offset)
        self.draw_collar(painter, self.controller.breath_offset)
        self.draw_tie(painter, self.controller.breath_offset)
        
        # Face parts (affected by head movement)
        self.draw_face(painter, offset_x, offset_y)
        self.draw_hair(painter, offset_x, offset_y)
        self.draw_eyebrows(painter, offset_x, offset_y)
        self.draw_eyes(painter, offset_x, offset_y)
        self.draw_nose(painter, offset_x, offset_y)
        self.draw_mouth(painter, offset_x, offset_y)
        
        # Special effects
        self.draw_special_effects(painter, offset_x, offset_y)

class CharacterView(QGraphicsView):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.renderer = QtCharacterRenderer(controller)
        
        # Set up scene
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setSceneRect(0, 0, WIDTH, HEIGHT)
        
        # Remove scrollbars
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Set background
        self.setBackgroundBrush(QBrush(QColor("#FFFFFF")))
        
        # Update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(33)  # ~30 FPS
        
    def update_animation(self):
        self.controller.update()
        self.viewport().update()
        
    def paintEvent(self, event):
        """Override paint event for direct rendering"""
        painter = QPainter(self.viewport())
        self.renderer.draw(painter)
        painter.end()

class AnimeAvatarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Anime Avatar Control")
        self.setFixedSize(900, 600)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # Create animation controller
        self.controller = AnimationController()
        
        # Create character view
        self.character_view = CharacterView(self.controller)
        layout.addWidget(self.character_view, 3)
        
        # Create control panel
        control_panel = self.create_control_panel()
        layout.addWidget(control_panel, 1)
        
    def create_control_panel(self):
        """Create the control panel for animations"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Emotion control group
        emotion_group = QGroupBox("Emotions")
        emotion_layout = QGridLayout()
        
        emotions = get_available_emotions()
        emotions.sort()  # Sort alphabetically
        
        for i, emotion in enumerate(emotions):
            btn = QPushButton(emotion.capitalize())
            btn.clicked.connect(lambda checked, e=emotion: self.set_emotion(e))
            row = i // 3
            col = i % 3
            emotion_layout.addWidget(btn, row, col)
        
        emotion_group.setLayout(emotion_layout)
        layout.addWidget(emotion_group)
        
        # Animation controls
        animation_group = QGroupBox("Animation Controls")
        animation_layout = QVBoxLayout()
        
        # Talk toggle
        self.talk_btn = QPushButton("Toggle Talking")
        self.talk_btn.setCheckable(True)
        self.talk_btn.setChecked(False)
        self.talk_btn.clicked.connect(self.toggle_talking)
        animation_layout.addWidget(self.talk_btn)
        
        # Blink frequency slider
        blink_layout = QHBoxLayout()
        blink_layout.addWidget(QLabel("Blink Frequency:"))
        blink_slider = QSlider(Qt.Orientation.Horizontal)
        blink_slider.setRange(1, 10)
        blink_slider.setValue(5)
        blink_slider.valueChanged.connect(self.adjust_blink_frequency)
        blink_layout.addWidget(blink_slider)
        animation_layout.addLayout(blink_layout)
        
        # Breath speed slider
        breath_layout = QHBoxLayout()
        breath_layout.addWidget(QLabel("Breathing Speed:"))
        breath_slider = QSlider(Qt.Orientation.Horizontal)
        breath_slider.setRange(1, 10)
        breath_slider.setValue(5)
        breath_slider.valueChanged.connect(self.adjust_breath_speed)
        breath_layout.addWidget(breath_slider)
        animation_layout.addLayout(breath_layout)
        
        # Head movement slider
        head_layout = QHBoxLayout()
        head_layout.addWidget(QLabel("Head Movement:"))
        head_slider = QSlider(Qt.Orientation.Horizontal)
        head_slider.setRange(0, 10)
        head_slider.setValue(5)
        head_slider.valueChanged.connect(self.adjust_head_movement)
        head_layout.addWidget(head_slider)
        animation_layout.addLayout(head_layout)
        
        animation_group.setLayout(animation_layout)
        layout.addWidget(animation_group)
        
        # Current emotion display
        self.emotion_label = QLabel("Current Emotion: neutral")
        self.emotion_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.emotion_label)
        
        layout.addStretch()
        return panel
    
    def set_emotion(self, emotion):
        """Set the character's emotion"""
        self.controller.emotion = emotion
        self.emotion_label.setText(f"Current Emotion: {emotion}")
    
    def toggle_talking(self, checked):
        """Toggle talking animation"""
        self.controller.talking = checked
        if checked:
            self.talk_btn.setStyleSheet("background-color: #90EE90;")
            self.controller.talk_counter = 20  # Set initial talk counter
        else:
            self.talk_btn.setStyleSheet("")
            self.controller.talk_counter = 0
            self.controller.talk_factor = 0
    
    def adjust_blink_frequency(self, value):
        """Adjust blink frequency"""
        self.controller.blink_interval = 200 - (value * 18)
    
    def adjust_breath_speed(self, value):
        """Adjust breathing speed"""
        self.controller.breath_speed = 0.015 + (value * 0.003)
    
    def adjust_head_movement(self, value):
        """Adjust head movement speed"""
        self.controller.head_move_speed = 0.01 * value / 5

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    window = AnimeAvatarApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()