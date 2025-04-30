# eye_drawing.py
import math
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath, QRadialGradient, QLinearGradient

class EyeRenderer:
    def __init__(self, renderer):
        self.renderer = renderer
        self.Xh = 0
        self.Yh = 0
        
        # Blue eye colors - adjusted for beautiful anime blue eyes
        self.eye_colors = {
            "normal": {
                "iris_inner": QColor("#1E90FF"),  # Bright blue
                "iris_mid": QColor("#4169E1"),    # Royal blue
                "iris_outer": QColor("#000080"),  # Navy blue
                "iris_edge": QColor("#191970"),   # Midnight blue
            },
            "angry": {
                "iris_inner": QColor("#1C86EE"),  # Dodger blue with intensity
                "iris_mid": QColor("#3A5FCD"),    # Royal blue with red tint
                "iris_outer": QColor("#27408B"),  # Dark blue with intensity
                "iris_edge": QColor("#1A1A5C"),   # Deep dark blue
            },
            "sad": {
                "iris_inner": QColor("#87CEFA"),  # Light sky blue
                "iris_mid": QColor("#4682B4"),    # Steel blue
                "iris_outer": QColor("#36648B"),  # Dark steel blue
                "iris_edge": QColor("#2C3E50"),   # Grayish blue
            },
            "happy": {
                "iris_inner": QColor("#00BFFF"),  # Deep sky blue
                "iris_mid": QColor("#1E90FF"),    # Dodger blue
                "iris_outer": QColor("#104E8B"),  # Deep blue
                "iris_edge": QColor("#08457E"),   # Dark azure
            }
        }
    
    def get_eye_color_set(self, emotion):
        """Get the appropriate color set for the current emotion"""
        if emotion in ["angry", "excited", "shocked"]:
            return self.eye_colors["angry"]
        elif emotion in ["sad", "crying"]:
            return self.eye_colors["sad"]
        elif emotion in ["happy", "laughing"]:
            return self.eye_colors["happy"]
        else:
            return self.eye_colors["normal"]
    
    def draw_eyes(self, painter, offset_x=0, offset_y=0, blink_factor=0, emotion_data=None):
        """Draw high-quality character eyes with detailed iris, reflections, and shadows"""
        # Adjust blink factor for sleepy emotions
        if self.renderer.controller.emotion == "sleepy" and blink_factor < emotion_data.blink_adjust:
            blink_factor = emotion_data.blink_adjust
        
        # Special case for winking
        winking = self.renderer.controller.emotion == "winking"
        left_blink = blink_factor
        right_blink = 1.0 if winking else blink_factor
        
        # --- LEFT EYE ---
        self.draw_detailed_eye(painter, offset_x, offset_y, left_blink, 
                              206, 212, emotion_data, "left")
        
        # --- RIGHT EYE ---
        self.draw_detailed_eye(painter, offset_x, offset_y, right_blink, 
                              384, 204, emotion_data, "right", is_winking=winking)
    
    def draw_detailed_eye(self, painter, offset_x, offset_y, blink_factor, 
                          base_x, base_y, emotion_data, side="left", is_winking=False):
        """Draw a single eye with high detail"""
        
        # Eye white (sclera) with shadow
        self.draw_eye_white(painter, offset_x, offset_y, blink_factor, 
                           base_x, base_y, emotion_data, side)
        
        # Don't draw iris, pupils, etc. if eye is closed (blink > 0.8)
        if blink_factor < 0.8:
            # Iris and pupil layers
            self.draw_detailed_iris(painter, offset_x, offset_y, blink_factor,
                                  base_x, base_y, emotion_data, side)
            
            # Eye shine and reflections
            self.draw_eye_reflections(painter, offset_x, offset_y, blink_factor,
                                    base_x, base_y, emotion_data, side)
        
        # Eye outlines and details
        self.draw_eye_outlines(painter, offset_x, offset_y, blink_factor,
                              base_x, base_y, emotion_data, side, is_winking)
        
        # Eyelashes
        if blink_factor < 0.4 and self.renderer.controller.emotion not in ["happy", "sleepy"]:
            self.draw_detailed_eyelashes(painter, offset_x, offset_y, base_x, base_y, side)
    
    def draw_eye_white(self, painter, offset_x, offset_y, blink_factor,
                       base_x, base_y, emotion_data, side):
        """Draw the white of the eye with subtle shading"""
        
        # Main white area
        white_path = QPainterPath()
        self.renderer.moveto(white_path, base_x + offset_x, base_y + offset_y)
        self.renderer.Xh = self.renderer.Yh = 0
        
        if side == "left":
            # Left eye shape
            self.renderer.relative_lineto(white_path, 15 + emotion_data.eye_width_adjust, -7)
            self.renderer.curveto_r(white_path, 4, -1, 26 + emotion_data.eye_width_adjust, -2, 
                          30 + emotion_data.eye_width_adjust, 0)
            self.renderer.smooth_r(white_path, 10, 3, 12, 7)
            self.renderer.smooth_r(white_path, 2, 27 - 25*blink_factor + emotion_data.eye_height_adjust, 
                         -1, 30 - 28*blink_factor + emotion_data.eye_height_adjust)
            self.renderer.smooth_r(white_path, -39 - emotion_data.eye_width_adjust, 5, 
                         -44 - emotion_data.eye_width_adjust, 1)
        else:
            # Right eye shape
            self.renderer.curveto_r(white_path, -3, -1, -18 - emotion_data.eye_width_adjust, -1, 
                          -28 - emotion_data.eye_width_adjust, 1)
            self.renderer.smooth_r(white_path, -9, 6, -10, 9)
            self.renderer.smooth_r(white_path, 3, 18 - 16*blink_factor + emotion_data.eye_height_adjust, 
                         6, 23 - 21*blink_factor + emotion_data.eye_height_adjust)
            self.renderer.smooth_r(white_path, 38 + emotion_data.eye_width_adjust, 6, 
                         40 + emotion_data.eye_width_adjust, 4)
            self.renderer.smooth_r(white_path, 10, -9, 13, -22)
            self.renderer.lineto(white_path, base_x + offset_x, base_y + offset_y)
        
        white_path.closeSubpath()
        
        # Apply gradient for depth
        gradient = QRadialGradient(QPointF(base_x + offset_x, base_y + offset_y + 5), 30)
        gradient.setColorAt(0, QColor("#FFFFFF"))
        gradient.setColorAt(0.7, QColor("#F8F8F8"))
        gradient.setColorAt(1, QColor("#F0F0F0"))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(white_path)
        
        # Add subtle shadow at edges for depth
        shadow_path = QPainterPath(white_path)
        painter.setBrush(QBrush(QColor(0, 0, 0, 15)))  # Very light shadow
        painter.drawPath(shadow_path)
    
    def draw_detailed_iris(self, painter, offset_x, offset_y, blink_factor,
                          base_x, base_y, emotion_data, side):
        """Draw highly detailed iris with multiple layers"""
        
        if side == "left":
            iris_x = 216 + offset_x + emotion_data.iris_offset_x
            iris_y = 206 + offset_y + emotion_data.iris_offset_y
        else:
            iris_x = 354 + offset_x + emotion_data.iris_offset_x
            iris_y = 207 + offset_y + emotion_data.iris_offset_y
        
        # Iris base layer
        iris_path = QPainterPath()
        self.renderer.moveto(iris_path, iris_x, iris_y)
        self.renderer.Xh = self.renderer.Yh = 0
        
        if side == "left":
            self.renderer.curveto_r(iris_path, -1, 5, 0, 26 - 24*blink_factor, 7, 35 - 33*blink_factor)
            self.renderer.smooth_r(iris_path, 30, 2, 33, 0)
            self.renderer.smooth_r(iris_path, 5, -31 + 29*blink_factor, 2, -34 + 32*blink_factor)
            self.renderer.curveto(iris_path, iris_x + 3, iris_y - 3, iris_x, iris_y, iris_x, iris_y)
        else:
            self.renderer.curveto_r(iris_path, -2, 1, 2, 29 - 27*blink_factor, 4, 31 - 29*blink_factor)
            self.renderer.smooth_r(iris_path, 30, 3, 33, 1)
            self.renderer.smooth_r(iris_path, 6, -24 + 22*blink_factor, 4, -27 + 25*blink_factor)
            self.renderer.relative_lineto(iris_path, -11, -8)
            self.renderer.curveto(iris_path, iris_x + 20, iris_y - 3, iris_x, iris_y, iris_x, iris_y)
        
        # Multi-color gradient for blue iris
        iris_gradient = QRadialGradient(QPointF(iris_x + 15, iris_y + 17), 30)
        
        # Get appropriate color set based on emotion
        colors = self.get_eye_color_set(self.renderer.controller.emotion)
        
        iris_gradient.setColorAt(0, colors["iris_inner"])
        iris_gradient.setColorAt(0.4, colors["iris_mid"])
        iris_gradient.setColorAt(0.7, colors["iris_outer"])
        iris_gradient.setColorAt(1, colors["iris_edge"])
        
        painter.setBrush(QBrush(iris_gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(iris_path)
        
        # Draw iris patterns (radial lines)
        pattern_center = QPointF(iris_x + 15, iris_y + 17)
        
        # Light blue radial lines
        painter.setPen(QPen(QColor(173, 216, 230, 100), 1))  # Light blue with transparency
        
        for i in range(36):  # More lines for better detail
            angle = i * 10 * math.pi / 180
            start_radius = 8
            end_radius = 24 - blink_factor * 10
            
            start_x = pattern_center.x() + start_radius * math.cos(angle)
            start_y = pattern_center.y() + start_radius * math.sin(angle)
            end_x = pattern_center.x() + end_radius * math.cos(angle)
            end_y = pattern_center.y() + end_radius * math.sin(angle)
            
            painter.drawLine(QPointF(start_x, start_y), QPointF(end_x, end_y))
        
        # Add some crystalline structure
        painter.setPen(QPen(QColor(70, 130, 180, 80), 1))  # Steel blue with transparency
        
        for i in range(12):
            angle = i * 30 * math.pi / 180
            mid_radius = 15 - blink_factor * 7
            
            # Create small crystaline patterns
            x1 = pattern_center.x() + mid_radius * math.cos(angle)
            y1 = pattern_center.y() + mid_radius * math.sin(angle)
            x2 = pattern_center.x() + (mid_radius - 3) * math.cos(angle + 0.1)
            y2 = pattern_center.y() + (mid_radius - 3) * math.sin(angle + 0.1)
            x3 = pattern_center.x() + (mid_radius - 3) * math.cos(angle - 0.1)
            y3 = pattern_center.y() + (mid_radius - 3) * math.sin(angle - 0.1)
            
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
            painter.drawLine(QPointF(x1, y1), QPointF(x3, y3))
        
        # Draw pupil
        pupil_center = QPointF(iris_x + 15, iris_y + 17)
        pupil_size = 8 - blink_factor * 4
        
        # Pupil gradient for depth
        pupil_gradient = QRadialGradient(pupil_center, pupil_size)
        pupil_gradient.setColorAt(0, QColor(0, 0, 0, 255))
        pupil_gradient.setColorAt(0.7, QColor(0, 0, 20, 255))
        pupil_gradient.setColorAt(1, QColor(0, 0, 0, 255))
        
        painter.setBrush(QBrush(pupil_gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(pupil_center, pupil_size, pupil_size)
        
        # Add subtle blue glow around pupil
        glow_gradient = QRadialGradient(pupil_center, pupil_size * 1.5)
        glow_gradient.setColorAt(0, QColor(30, 144, 255, 0))
        glow_gradient.setColorAt(0.5, QColor(30, 144, 255, 50))
        glow_gradient.setColorAt(1, QColor(30, 144, 255, 0))
        
        painter.setBrush(QBrush(glow_gradient))
        painter.drawEllipse(pupil_center, pupil_size * 1.5, pupil_size * 1.5)
    
    def draw_eye_reflections(self, painter, offset_x, offset_y, blink_factor,
                            base_x, base_y, emotion_data, side):
        """Draw multiple layers of reflections and shine"""
        
        if side == "left":
            highlight_x = 253 + offset_x
            highlight_y = 211 + offset_y
        else:
            highlight_x = 392 + offset_x
            highlight_y = 209 + offset_y
        
        # Primary light reflection
        reflection_center = QPointF(highlight_x, highlight_y)
        
        # Create gradient for soft reflection
        reflection_gradient = QRadialGradient(reflection_center, 10)
        reflection_gradient.setColorAt(0, QColor(255, 255, 255, 255))
        reflection_gradient.setColorAt(0.3, QColor(255, 255, 255, 220))
        reflection_gradient.setColorAt(0.6, QColor(255, 255, 255, 150))
        reflection_gradient.setColorAt(1, QColor(255, 255, 255, 0))
        
        painter.setBrush(QBrush(reflection_gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        
        reflection_size = 10 - blink_factor * 7
        painter.drawEllipse(reflection_center, reflection_size, reflection_size * 0.7)
        
        # Secondary highlights - multiple small ones for sparkle effect
        secondary_highlights = [
            (4, 3, 3),   # offset_x, offset_y, size
            (-2, 5, 2),
            (6, -2, 2.5),
            (-4, -3, 1.5),
            (3, 6, 1.8)
        ]
        
        for dx, dy, size in secondary_highlights:
            if side == "right":
                dx = -dx  # Mirror for right eye
                
            highlight_pos = QPointF(highlight_x + dx, highlight_y + dy)
            highlight_size = size - blink_factor * size * 0.7
            
            small_gradient = QRadialGradient(highlight_pos, highlight_size)
            small_gradient.setColorAt(0, QColor(255, 255, 255, 200))
            small_gradient.setColorAt(0.8, QColor(255, 255, 255, 50))
            small_gradient.setColorAt(1, QColor(255, 255, 255, 0))
            
            painter.setBrush(QBrush(small_gradient))
            painter.drawEllipse(highlight_pos, highlight_size, highlight_size * 0.8)
        
        # Specular highlight on lower part of eye (blue tint)
        if blink_factor < 0.5:
            lower_highlight = QPointF(highlight_x + 10, highlight_y + 15)
            
            lower_gradient = QLinearGradient(lower_highlight, 
                                           QPointF(lower_highlight.x() + 20, lower_highlight.y()))
            lower_gradient.setColorAt(0, QColor(173, 216, 230, 0))    # Light blue
            lower_gradient.setColorAt(0.5, QColor(173, 216, 230, 80))
            lower_gradient.setColorAt(1, QColor(173, 216, 230, 0))
            
            painter.setBrush(QBrush(lower_gradient))
            painter.drawEllipse(lower_highlight, 12, 4)
    
    def draw_eye_outlines(self, painter, offset_x, offset_y, blink_factor,
                         base_x, base_y, emotion_data, side, is_winking=False):
        """Draw eye outlines with variable thickness"""
        
        # Upper eyelid
        upper_path = QPainterPath()
        self.renderer.moveto(upper_path, base_x + offset_x, base_y + offset_y)
        self.renderer.Xh = self.renderer.Yh = 0
        
        if side == "left":
            self.renderer.relative_lineto(upper_path, 15 + emotion_data.eye_width_adjust, -7)
            self.renderer.curveto_r(upper_path, 4, -1, 26 + emotion_data.eye_width_adjust, -2, 
                          30 + emotion_data.eye_width_adjust, 0)
            self.renderer.smooth_r(upper_path, 10, 3, 12, 7)
            
            # Variable thickness based on curve
            thickness_points = []
            for i in range(20):
                t = i / 19
                point = upper_path.pointAtPercent(t)
                # Thicker at ends, thinner in middle
                thickness = 2.5 + 1.0 * math.sin(t * math.pi)
                thickness_points.append((point, thickness))
        else:
            self.renderer.curveto_r(upper_path, -3, -1, -18 - emotion_data.eye_width_adjust, -1, 
                          -28 - emotion_data.eye_width_adjust, 1)
            self.renderer.smooth_r(upper_path, -9, 6, -10, 9)
            
            # Variable thickness
            thickness_points = []
            for i in range(20):
                t = i / 19
                point = upper_path.pointAtPercent(t)
                thickness = 2.5 + 1.0 * math.sin(t * math.pi)
                thickness_points.append((point, thickness))
        
        # Draw upper eyelid with variable thickness
        for i in range(len(thickness_points) - 1):
            start_point, start_thickness = thickness_points[i]
            end_point, end_thickness = thickness_points[i + 1]
            
            pen = QPen(QColor("black"), start_thickness)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            painter.drawLine(start_point, end_point)
        
        # Lower eyelid (thinner)
        painter.setPen(QPen(QColor("#505050"), 1))
        lower_path = QPainterPath()
        
        if side == "left":
            self.renderer.moveto(lower_path, base_x + offset_x + 12 + 30 + emotion_data.eye_width_adjust, 
                       base_y + offset_y + 7)
            self.renderer.smooth_r(lower_path, 2, 27 - 25*blink_factor + emotion_data.eye_height_adjust, 
                         -1, 30 - 28*blink_factor + emotion_data.eye_height_adjust)
            self.renderer.smooth_r(lower_path, -39 - emotion_data.eye_width_adjust, 5, 
                         -44 - emotion_data.eye_width_adjust, 1)
        else:
            self.renderer.moveto(lower_path, base_x + offset_x - 10 - 30 - emotion_data.eye_width_adjust, 
                       base_y + offset_y + 9)
            self.renderer.smooth_r(lower_path, 3, 18 - 16*blink_factor + emotion_data.eye_height_adjust, 
                         6, 23 - 21*blink_factor + emotion_data.eye_height_adjust)
            self.renderer.smooth_r(lower_path, 38 + emotion_data.eye_width_adjust, 6, 
                         40 + emotion_data.eye_width_adjust, 4)
        
        painter.drawPath(lower_path)
        
        # Double eyelid fold
        if blink_factor < 0.6:
            painter.setPen(QPen(QColor("#404040"), 1))
            fold_path = QPainterPath()
            
            if side == "left":
                self.renderer.moveto(fold_path, base_x + offset_x + 5, base_y + offset_y - 4)
                self.renderer.curveto_r(fold_path, 15, -3, 35, -1, 45, 5)
            else:
                self.renderer.moveto(fold_path, base_x + offset_x - 5, base_y + offset_y - 4)
                self.renderer.curveto_r(fold_path, -15, -3, -35, -1, -45, 5)
            
            painter.drawPath(fold_path)
    
    def draw_detailed_eyelashes(self, painter, offset_x, offset_y, base_x, base_y, side):
        """Draw detailed eyelashes with varying lengths and curves"""
        
        if side == "left":
            lash_base_points = [
                (base_x + 15, base_y - 7),
                (base_x + 25, base_y - 7),
                (base_x + 35, base_y - 5),
                (base_x + 45, base_y - 2),
                (base_x + 48, base_y + 2),
                (base_x + 50, base_y + 5),
            ]
            
            # Upper lashes
            for i, (x, y) in enumerate(lash_base_points):
                length = 12 - i * 1.5
                angle = -30 - i * 10
                
                path = QPainterPath()
                self.renderer.moveto(path, x + offset_x, y + offset_y)
                
                control_x = x + math.cos(math.radians(angle)) * length * 0.7
                control_y = y + math.sin(math.radians(angle)) * length * 0.7
                end_x = x + math.cos(math.radians(angle - 10)) * length
                end_y = y + math.sin(math.radians(angle - 10)) * length
                
                self.renderer.curveto(path, 
                            control_x + offset_x, control_y + offset_y,
                            end_x + offset_x - 1, end_y + offset_y,
                            end_x + offset_x, end_y + offset_y)
                
                # Vary thickness
                thickness = 2.5 - i * 0.3
                painter.setPen(QPen(QColor("black"), thickness))
                painter.drawPath(path)
            
            # Lower lashes (shorter and sparser)
            lower_lash_points = [
                (base_x + 10, base_y + 25),
                (base_x + 20, base_y + 27),
                (base_x + 30, base_y + 28),
                (base_x + 40, base_y + 27),
            ]
            
            for i, (x, y) in enumerate(lower_lash_points):
                length = 5 - i * 0.5
                angle = 20 + i * 8
                
                path = QPainterPath()
                self.renderer.moveto(path, x + offset_x, y + offset_y)
                
                end_x = x + math.cos(math.radians(angle)) * length
                end_y = y + math.sin(math.radians(angle)) * length
                
                self.renderer.lineto(path, end_x + offset_x, end_y + offset_y)
                
                painter.setPen(QPen(QColor("#404040"), 1))
                painter.drawPath(path)
        
        else:  # Right eye (mirrored)
            # Similar logic but with mirrored coordinates
            lash_base_points = [
                (base_x - 15, base_y - 7),
                (base_x - 25, base_y - 7),
                (base_x - 35, base_y - 5),
                (base_x - 45, base_y - 2),
                (base_x - 48, base_y + 2),
                (base_x - 50, base_y + 5),
            ]
            
            # Upper lashes
            for i, (x, y) in enumerate(lash_base_points):
                length = 12 - i * 1.5
                angle = 180 + 30 + i * 10
                
                path = QPainterPath()
                self.renderer.moveto(path, x + offset_x, y + offset_y)
                
                control_x = x + math.cos(math.radians(angle)) * length * 0.7
                control_y = y + math.sin(math.radians(angle)) * length * 0.7
                end_x = x + math.cos(math.radians(angle + 10)) * length
                end_y = y + math.sin(math.radians(angle + 10)) * length
                
                self.renderer.curveto(path, 
                            control_x + offset_x, control_y + offset_y,
                            end_x + offset_x + 1, end_y + offset_y,
                            end_x + offset_x, end_y + offset_y)
                
                thickness = 2.5 - i * 0.3
                painter.setPen(QPen(QColor("black"), thickness))
                painter.drawPath(path)