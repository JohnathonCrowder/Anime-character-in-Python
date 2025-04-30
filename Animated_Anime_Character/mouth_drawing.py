from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath
from emotions import get_emotion_data, MOUTH_SHAPES

class MouthRenderer:
    def __init__(self, renderer):
        self.renderer = renderer
    
    def draw_nose_and_mouth(self, painter, offset_x=0, offset_y=0, emotion_data=None):
        """Draw nose and mouth combined for consistent positioning"""
        # Draw nose first
        self.draw_nose(painter, offset_x, offset_y)
        
        # Draw mouth with animation
        self.draw_mouth(painter, offset_x, offset_y, emotion_data)
    
    def draw_nose(self, painter, offset_x=0, offset_y=0):
        """Draw the character's nose"""
        painter.setPen(QPen(QColor("black"), 1))
        
        nose_path = QPainterPath()
        self.renderer.moveto(nose_path, 309 + offset_x, 270 + offset_y)
        self.renderer.Xh = self.renderer.Yh = 0
        
        self.renderer.curveto_r(nose_path, 0, 0, 4, 7, 1, 9)
        painter.drawPath(nose_path)
    
    def draw_mouth(self, painter, offset_x=0, offset_y=0, emotion_data=None):
        """Draw the mouth with talk animation"""
        if not emotion_data:
            emotion_data = get_emotion_data(self.renderer.controller.emotion)
        
        mouth_shape = MOUTH_SHAPES[emotion_data.mouth_type]
        
        painter.setPen(QPen(QColor("black"), 1))
        
        if self.renderer.controller.talk_factor > 0:
            # Talking mouth
            self.draw_talking_mouth(painter, mouth_shape.talking, offset_x, offset_y)
        else:
            # Closed mouth
            self.draw_closed_mouth(painter, mouth_shape.closed, offset_x, offset_y)
    
    def draw_talking_mouth(self, painter, talking_data, offset_x, offset_y):
        """Draw mouth in talking position"""
        path = QPainterPath()
        self.renderer.moveto(path, talking_data.start_x + offset_x, 
                   talking_data.start_y + offset_y)
        self.renderer.Xh = self.renderer.Yh = 0
        
        painter.setBrush(QBrush(QColor("black")))
        
        # Draw upper lip with animation
        for curve_type, *params in talking_data.upper_lip:
            if curve_type == "curveto_r":
                adjusted_params = self.adjust_for_talk_animation(params)
                self.renderer.curveto_r(path, *adjusted_params)
        
        # Draw right corner
        if talking_data.corners and len(talking_data.corners) > 0:
            corner_type, *corner_params = talking_data.corners[0]
            if corner_type == "curveto_r":
                adjusted_params = self.adjust_for_talk_animation(corner_params, is_corner=True)
                self.renderer.curveto_r(path, *adjusted_params)
        
        # Draw lower lip
        for curve_type, *params in talking_data.lower_lip:
            if curve_type == "curveto_r":
                adjusted_params = self.adjust_for_talk_animation(params, lower_lip=True)
                self.renderer.curveto_r(path, *adjusted_params)
        
        # Draw left corner
        if talking_data.corners and len(talking_data.corners) > 1:
            corner_type, *corner_params = talking_data.corners[1]
            if corner_type == "curveto_r":
                adjusted_params = self.adjust_for_talk_animation(corner_params, is_corner=True)
                self.renderer.curveto_r(path, *adjusted_params)
        
        path.closeSubpath()
        painter.drawPath(path)
        
        # Draw inner detail if available
        self.draw_inner_mouth_detail(painter, talking_data.inner_detail, offset_x, offset_y)
    
    def draw_closed_mouth(self, painter, closed_data, offset_x, offset_y):
        """Draw mouth in closed position"""
        path = QPainterPath()
        self.renderer.moveto(path, closed_data.start_x + offset_x, 
                   closed_data.start_y + offset_y)
        self.renderer.Xh = self.renderer.Yh = 0
        
        if len(closed_data.curves) > 1:
            painter.setBrush(QBrush(QColor("black")))
        
        for curve_type, *params in closed_data.curves:
            if curve_type == "curveto_r":
                self.renderer.curveto_r(path, *params)
            elif curve_type == "horizontal":
                self.renderer.horizontal(path, self.renderer.convert_x(path.currentPosition().x()) + params[0])
        
        if len(closed_data.curves) > 1:
            path.closeSubpath()
        
        painter.drawPath(path)
        painter.setBrush(Qt.BrushStyle.NoBrush)
    
    def adjust_for_talk_animation(self, params, is_corner=False, lower_lip=False):
        """Adjust curve parameters for talking animation"""
        adjusted_params = []
        talk_factor = self.renderer.controller.talk_factor
        
        for i, param in enumerate(params):
            if i % 2 == 1:  # Y coordinates
                if is_corner and i > 2:  # Corner adjustment
                    adjusted_params.append(param + (talk_factor * 4))
                elif lower_lip:
                    adjusted_params.append(param + (talk_factor * 6))
                else:
                    adjusted_params.append(param + (talk_factor * 4))
            else:
                adjusted_params.append(param)
        
        return adjusted_params
    
    def draw_inner_mouth_detail(self, painter, inner_detail, offset_x, offset_y):
        """Draw inner mouth detail for talking animation"""
        if not inner_detail or self.renderer.controller.talk_factor <= 0.5:
            return
        
        painter.setBrush(QBrush(QColor(inner_detail["color"])))
        inner_path = QPainterPath()
        
        talk_offset = self.renderer.controller.talk_factor * 3
        self.renderer.moveto(inner_path, 298 + offset_x,
                   310 + offset_y + talk_offset)
        self.renderer.Xh = self.renderer.Yh = 0
        
        for curve_type, *params in inner_detail["curves"]:
            if curve_type == "curveto_r":
                self.renderer.curveto_r(inner_path, *params)
        
        inner_path.closeSubpath()
        painter.drawPath(inner_path)
        painter.setBrush(Qt.BrushStyle.NoBrush)