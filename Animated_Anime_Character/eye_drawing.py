from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath
from emotions import get_emotion_data, EYEBROW_SHAPES

class EyeRenderer:
    def __init__(self, renderer):
        self.renderer = renderer
    
    def draw_eyes(self, painter, offset_x=0, offset_y=0, blink_factor=0, emotion_data=None):
        """Draw eyes matching the original turtle graphics version"""
        # Adjust blink factor for sleepy emotions
        if self.renderer.controller.emotion == "sleepy" and blink_factor < emotion_data.blink_adjust:
            blink_factor = emotion_data.blink_adjust
        
        # Special case for winking
        winking = self.renderer.controller.emotion == "winking"
        left_blink = blink_factor
        right_blink = 1.0 if winking else blink_factor * 0.95  # Slight delay for realism
        
        # Draw eyebrows (now with proper emotion support)
        self.draw_eyebrows(painter, offset_x, offset_y, emotion_data)
        
        # Draw eye whites
        self.draw_eye_whites(painter, offset_x, offset_y, left_blink, right_blink, emotion_data)
        
        # Draw irises if eyes are open
        if blink_factor < 0.8:
            self.draw_irises(painter, offset_x, offset_y, left_blink, right_blink, emotion_data, winking)
            self.draw_eye_shadows(painter, offset_x, offset_y, left_blink, right_blink)
            self.draw_eye_highlights(painter, offset_x, offset_y, left_blink, right_blink, winking)
        
        # Draw eye lines and lashes
        self.draw_eye_lines(painter, offset_x, offset_y, left_blink, right_blink, winking)
    
    def draw_eyebrows(self, painter, offset_x, offset_y, emotion_data=None):
        """Draw eyebrows with emotion adjustments"""
        painter.setPen(QPen(QColor("black"), 2))
        
        # Get emotion data for eyebrow adjustments
        if not emotion_data:
            emotion_data = get_emotion_data(self.renderer.controller.emotion)
        
        eyebrow_shape = EYEBROW_SHAPES[emotion_data.eyebrow_type]
        
        # Left eyebrow with emotion
        left_brow_path = QPainterPath()
        self.renderer.moveto(left_brow_path, 210 + offset_x, eyebrow_shape.left_start_y + offset_y)
        self.renderer.Xh = self.renderer.Yh = 0  # Reset for smooth curves
        
        for curve_params in eyebrow_shape.left_curve:
            self.renderer.curveto_r(left_brow_path, *curve_params)
        
        painter.drawPath(left_brow_path)
        
        # Right eyebrow with emotion
        right_brow_path = QPainterPath()
        self.renderer.moveto(right_brow_path, 338 + offset_x, eyebrow_shape.right_start_y + offset_y)
        self.renderer.Xh = self.renderer.Yh = 0  # Reset for smooth curves
        
        for curve_params in eyebrow_shape.right_curve:
            self.renderer.curveto_r(right_brow_path, *curve_params)
        
        painter.drawPath(right_brow_path)
    
    def draw_eye_whites(self, painter, offset_x, offset_y, left_blink, right_blink, emotion_data):
        """Draw eye whites with realistic blinking"""
        # Get moisture for subtle effects
        moisture = getattr(self.renderer.controller, 'eye_moisture', 1.0)
        
        # Left eye white
        painter.setPen(QPen(QColor("black"), 2))
        painter.setBrush(QBrush(QColor("#D1D1D1")))
        
        left_eye_path = QPainterPath()
        self.renderer.moveto(left_eye_path, 206 + offset_x, 212 + offset_y)
        self.renderer.relative_lineto(left_eye_path, 15, -7)
        self.renderer.curveto_r(left_eye_path, 4, -1, 26, -2, 30, 0)
        self.renderer.smooth_r(left_eye_path, 10, 3, 12, 7)
        
        # More natural eyelid movement - upper lid moves more than lower
        upper_lid_factor = left_blink * 1.2
        lower_lid_factor = left_blink * 0.6
        
        painter.setPen(QPen(QColor("#D1D1D1"), 1))
        self.renderer.smooth_r(left_eye_path, 2, 27 - 27*lower_lid_factor, -1, 30 - 30*lower_lid_factor)
        self.renderer.smooth_r(left_eye_path, -39, 5 - 7*upper_lid_factor, -44, 1 - 1*upper_lid_factor)
        self.renderer.smooth(left_eye_path, 206 + offset_x, 212 + offset_y, 206 + offset_x, 212 + offset_y)
        
        painter.drawPath(left_eye_path)
        
        # Right eye white - slightly asymmetric for realism
        right_top_path = QPainterPath()
        self.renderer.moveto(right_top_path, 384 + offset_x, 204 + offset_y)
        self.renderer.curveto_r(right_top_path, -3, -1, -18, -1, -28, 1)
        self.renderer.smooth_r(right_top_path, -9, 6, -10, 9)
        
        painter.setPen(QPen(QColor("black"), 2))
        painter.drawPath(right_top_path)
        
        # Bottom part with realistic movement
        right_bottom_path = QPainterPath()
        self.renderer.moveto(right_bottom_path, 346 + offset_x, 214 + offset_y)
        
        upper_lid_factor = right_blink * 1.2
        lower_lid_factor = right_blink * 0.6
        
        self.renderer.smooth_r(right_bottom_path, 3, 18 - 18*lower_lid_factor, 6, 23 - 23*lower_lid_factor)
        self.renderer.smooth_r(right_bottom_path, 38, 6 - 8*upper_lid_factor, 40, 4 - 4*upper_lid_factor)
        self.renderer.smooth_r(right_bottom_path, 10, -9, 13, -22)
        
        painter.setPen(QPen(QColor("#D1D1D1"), 1))
        painter.drawPath(right_bottom_path)
        
        # Fill the entire eye
        full_eye_path = QPainterPath()
        self.renderer.moveto(full_eye_path, 384 + offset_x, 204 + offset_y)
        self.renderer.curveto_r(full_eye_path, -3, -1, -18, -1, -28, 1)
        self.renderer.smooth_r(full_eye_path, -9, 6, -10, 9)
        self.renderer.smooth_r(full_eye_path, 3, 18 - 18*lower_lid_factor, 6, 23 - 23*lower_lid_factor)
        self.renderer.smooth_r(full_eye_path, 38, 6 - 8*upper_lid_factor, 40, 4 - 4*upper_lid_factor)
        self.renderer.smooth_r(full_eye_path, 10, -9, 13, -22)
        full_eye_path.closeSubpath()
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#D1D1D1")))
        painter.drawPath(full_eye_path)
        
        # Add subtle eyelid creases during blink
        if left_blink > 0.1:
            painter.setPen(QPen(QColor("#CCCCCC"), 0.5))
            crease_path = QPainterPath()
            self.renderer.moveto(crease_path, 210 + offset_x, 205 + offset_y - 8*left_blink)
            self.renderer.curveto_r(crease_path, 15, 0, 35, 0, 50, 2)
            painter.drawPath(crease_path)
        
        if right_blink > 0.1:
            painter.setPen(QPen(QColor("#CCCCCC"), 0.5))
            crease_path = QPainterPath()
            self.renderer.moveto(crease_path, 350 + offset_x, 199 + offset_y - 8*right_blink)
            self.renderer.curveto_r(crease_path, -15, 0, -35, 0, -50, 2)
            painter.drawPath(crease_path)
    
    def draw_irises(self, painter, offset_x, offset_y, left_blink, right_blink, emotion_data, winking):
        """Draw irises matching original style with natural movement"""
        painter.setPen(QPen(QColor("#0C1631"), 1))
        painter.setBrush(QBrush(QColor("#0C1631")))
        
        # Subtle iris movement during blink
        iris_y_offset_left = left_blink * 5
        iris_y_offset_right = right_blink * 5
        
        # Left iris
        if not (winking and left_blink >= 0.8):
            left_iris_path = QPainterPath()
            self.renderer.moveto(left_iris_path, 216 + offset_x + emotion_data.iris_offset_x, 
                       206 + offset_y + emotion_data.iris_offset_y + iris_y_offset_left)
            self.renderer.curveto_r(left_iris_path, -1, 5, 0, 26 - 24*left_blink, 7, 35 - 33*left_blink)
            self.renderer.smooth_r(left_iris_path, 30, 2, 33, 0)
            self.renderer.smooth_r(left_iris_path, 5, -31 + 29*left_blink, 2, -34 + 32*left_blink)
            self.renderer.smooth(left_iris_path, 219 + offset_x + emotion_data.iris_offset_x, 
                        203 + offset_y + emotion_data.iris_offset_y + iris_y_offset_left,
                        216 + offset_x + emotion_data.iris_offset_x, 
                        206 + offset_y + emotion_data.iris_offset_y + iris_y_offset_left)
            
            painter.drawPath(left_iris_path)
        
        # Right iris
        if not winking or right_blink < 0.8:
            right_iris_path = QPainterPath()
            self.renderer.moveto(right_iris_path, 354 + offset_x + emotion_data.iris_offset_x, 
                       207 + offset_y + emotion_data.iris_offset_y + iris_y_offset_right)
            self.renderer.curveto_r(right_iris_path, -2, 1, 2, 29 - 27*right_blink, 4, 31 - 29*right_blink)
            self.renderer.smooth_r(right_iris_path, 30, 3, 33, 1)
            self.renderer.smooth_r(right_iris_path, 6, -24 + 22*right_blink, 4, -27 + 25*right_blink)
            self.renderer.relative_lineto(right_iris_path, -11, -8)
            self.renderer.curveto(right_iris_path, 382 + offset_x + emotion_data.iris_offset_x, 
                        204 + offset_y + emotion_data.iris_offset_y + iris_y_offset_right,
                        357 + offset_x + emotion_data.iris_offset_x, 
                        206 + offset_y + emotion_data.iris_offset_y + iris_y_offset_right,
                        354 + offset_x + emotion_data.iris_offset_x, 
                        207 + offset_y + emotion_data.iris_offset_y + iris_y_offset_right)
            
            painter.drawPath(right_iris_path)
    
    def draw_eye_shadows(self, painter, offset_x, offset_y, left_blink, right_blink):
        """Draw eye shadows layer 4"""
        # Left eye shadow
        painter.setPen(QPen(QColor("#352F53"), 1))
        painter.setBrush(QBrush(QColor("#352F53")))
        
        left_shadow_path = QPainterPath()
        self.renderer.moveto(left_shadow_path, 219 + offset_x, 229 + offset_y)
        self.renderer.smooth_r(left_shadow_path, 2, -5, 6, -4)
        self.renderer.smooth_r(left_shadow_path, 18, 13, 27, 1)
        self.renderer.curveto_r(left_shadow_path, 3, 0, 5, 3, 5, 3)
        self.renderer.vertical(left_shadow_path, 13)
        self.renderer.horizontal(left_shadow_path, 224)
        self.renderer.lineto(left_shadow_path, 219 + offset_x, 229 + offset_y)
        
        painter.drawPath(left_shadow_path)
        
        # Right eye shadow
        right_shadow_path = QPainterPath()
        self.renderer.moveto(right_shadow_path, 357 + offset_x, 227 + offset_y)
        self.renderer.smooth_r(right_shadow_path, 4, -6, 10, -2)
        self.renderer.smooth_r(right_shadow_path, 10, 13, 19, 1)
        self.renderer.curveto_r(right_shadow_path, 6, 0, 8, 6, 8, 6)
        self.renderer.relative_lineto(right_shadow_path, -2, 9)
        self.renderer.curveto_r(right_shadow_path, -12, 3, -29, 0, -32, -2)
        self.renderer.smooth(right_shadow_path, 357 + offset_x, 227 + offset_y, 357 + offset_x, 227 + offset_y)
        
        painter.drawPath(right_shadow_path)
        
        # Layer 5 highlights
        painter.setPen(QPen(QColor("#9A90CB"), 1))
        painter.setBrush(QBrush(QColor("#9A90CB")))
        
        left_hl_path = QPainterPath()
        self.renderer.moveto(left_hl_path, 227 + offset_x, 231 + offset_y)
        self.renderer.curveto_r(left_hl_path, -6, 0, -5, 5, -3, 8)
        self.renderer.smooth_r(left_hl_path, 24, 2, 27, 0)
        self.renderer.smooth_r(left_hl_path, 0, -8, -1, -8)
        self.renderer.smooth(left_hl_path, 234 + offset_x, 231 + offset_y, 227 + offset_x, 231 + offset_y)
        
        painter.drawPath(left_hl_path)
        
        right_hl_path = QPainterPath()
        self.renderer.moveto(right_hl_path, 361 + offset_x, 227 + offset_y)
        self.renderer.curveto_r(right_hl_path, 2, 18, 26, 14, 30, 6)
        self.renderer.smooth_r(right_hl_path, -1, -3, -2, -4)
        self.renderer.smooth_r(right_hl_path, -15, 9, -24, -4)
        self.renderer.curveto(right_hl_path, 363 + offset_x, 224 + offset_y, 361 + offset_x, 225 + offset_y, 361 + offset_x, 227 + offset_y)
        
        painter.drawPath(right_hl_path)
    
    def draw_eye_highlights(self, painter, offset_x, offset_y, left_blink, right_blink, winking):
        """Draw eye highlights with moisture effects"""
        painter.setPen(Qt.PenStyle.NoPen)
        
        # Get eye moisture from controller (defaults to 1.0 if not set)
        moisture = getattr(self.renderer.controller, 'eye_moisture', 1.0)
        
        # Adjust highlight opacity based on moisture and blink state
        highlight_alpha = int(255 * moisture * (1 - left_blink * 0.7))
        highlight_color = QColor("#F5F5F5")
        highlight_color.setAlpha(highlight_alpha)
        painter.setBrush(QBrush(highlight_color))
        
        # Left eye highlight
        if left_blink < 0.6:
            highlight_path = QPainterPath()
            self.renderer.moveto(highlight_path, 253 + offset_x, 211 + offset_y)
            self.renderer.curveto_r(highlight_path, -3, 0, -8, 8 - 7*left_blink, 1, 10 - 9*left_blink)
            self.renderer.smooth(highlight_path, 258 + offset_x, 210 + offset_y, 253 + offset_x, 211 + offset_y)
            painter.drawPath(highlight_path)
            
            # Additional small highlight for tear film effect
            if moisture > 0.9 and left_blink < 0.3:
                highlight_secondary = QColor(255, 255, 255, 180)
                painter.setBrush(QBrush(highlight_secondary))
                painter.drawEllipse(QPointF(245 + offset_x, 215 + offset_y), 2, 1)
        
        # Right eye highlight
        if right_blink < 0.6 and not winking:
            right_alpha = int(255 * moisture * (1 - right_blink * 0.7))
            right_color = QColor("#F5F5F5")
            right_color.setAlpha(right_alpha)
            painter.setBrush(QBrush(right_color))
            
            right_highlight_path = QPainterPath()
            self.renderer.moveto(right_highlight_path, 392 + offset_x, 209 + offset_y)
            self.renderer.relative_lineto(right_highlight_path, 4, 3)
            self.renderer.vertical(right_highlight_path, 4 - 3*right_blink)
            self.renderer.relative_lineto(right_highlight_path, -4, 2)
            self.renderer.curveto(right_highlight_path, 386 + offset_x, 214 + offset_y, 
                        392 + offset_x, 209 + offset_y,
                        392 + offset_x, 209 + offset_y)
            painter.drawPath(right_highlight_path)
            
            # Additional small highlight for tear film effect
            if moisture > 0.9 and right_blink < 0.3:
                highlight_secondary = QColor(255, 255, 255, 180)
                painter.setBrush(QBrush(highlight_secondary))
                painter.drawEllipse(QPointF(385 + offset_x, 213 + offset_y), 2, 1)
    
    def draw_eye_lines(self, painter, offset_x, offset_y, left_blink, right_blink, winking):
        """Draw eye lines and lashes with natural movement during blinks"""
        # Adjust eye curve thickness during blink
        curve_thickness = max(1, 3 - left_blink * 2)
        painter.setPen(QPen(QColor("black"), curve_thickness))
        
        # Draw eye curves that adjust with blinking
        curve_path = QPainterPath()
        self.renderer.moveto(curve_path, 225 + offset_x, 215 + offset_y - 3*left_blink)
        self.renderer.curveto_r(curve_path, 10, 28 - 15*left_blink, 22, 16 - 10*left_blink, 24, 6)
        painter.drawPath(curve_path)
        
        right_curve_thickness = max(1, 3 - right_blink * 2)
        painter.setPen(QPen(QColor("black"), right_curve_thickness))
        
        right_curve_path = QPainterPath()
        self.renderer.moveto(right_curve_path, 365 + offset_x, 219 + offset_y - 3*right_blink)
        self.renderer.curveto_r(right_curve_path, 4, 14 - 8*right_blink, 18, 24 - 12*right_blink, 22, -3)
        painter.drawPath(right_curve_path)
        
        # Draw lashes that move with blink
        painter.setPen(QPen(QColor("black"), 2))
        
        if left_blink < 0.4:
            lash_lines = [
                (240.5, 207.5, 227.5, 211.5),
                (245.5, 209.5, 227.5, 214.5),
                (247.5, 211.5, 227.5, 217.5),
                (247.5, 214.5, 229.5, 220.5),
                (247.5, 218.5, 230.5, 223.5),
                (246.5, 222.5, 232.5, 226.5),
                (244.5, 225.5, 234.5, 228.5)
            ]
            
            # Adjust lash positions during blink
            for i, (x1, y1, x2, y2) in enumerate(lash_lines):
                y_offset = left_blink * 5 * (1 - i/len(lash_lines))  # Outer lashes move more
                s_pt = QPointF(x1 + offset_x, y1 + offset_y + y_offset)
                e_pt = QPointF(x2 + offset_x, y2 + offset_y + y_offset*0.5)
                painter.drawLine(s_pt, e_pt)
        
        if right_blink < 0.4 and not winking:
            right_lash_lines = [
                (377.5, 207.5, 367.5, 210.5),
                (384.5, 207.5, 366.5, 212.5),
                (385.5, 210.5, 366.5, 215.5),
                (384.5, 213.5, 366.5, 218.5),
                (384.5, 215.5, 367.5, 220.5),
                (384.5, 218.5, 368.5, 223.5),
                (382.5, 223.5, 370.5, 227.5)
            ]
            
            # Adjust lash positions during blink
            for i, (x1, y1, x2, y2) in enumerate(right_lash_lines):
                y_offset = right_blink * 5 * (1 - i/len(right_lash_lines))  # Outer lashes move more
                s_pt = QPointF(x1 + offset_x, y1 + offset_y + y_offset)
                e_pt = QPointF(x2 + offset_x, y2 + offset_y + y_offset*0.5)
                painter.drawLine(s_pt, e_pt)