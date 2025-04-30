from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath, QLinearGradient, QRadialGradient
from emotions import get_emotion_data, MOUTH_SHAPES
import random
import math

class MouthRenderer:
    def __init__(self, renderer):
        self.renderer = renderer
        self.lip_moisture = 0.8  # Shininess/moisture of lips
        self.last_talk_factor = 0  # For animation smoothing
        self.talk_transition_speed = 0.2  # Speed of mouth movement transitions
        self.lip_color_base = QColor(252, 157, 157, 200)  # Base color for lips
        self.inner_mouth_color = QColor(90, 10, 10, 180)  # Inner mouth color
        
    def update_lip_moisture(self):
        """Dynamically update lip moisture based on talking and emotion"""
        controller = self.renderer.controller
        target = 0.8  # Base moisture level
        
        # Increase moisture when talking
        if controller.talking:
            target = 0.9 + 0.1 * math.sin(controller.frame * 0.1)
            
        # Adjust based on emotion
        if controller.emotion in ["sad", "crying"]:
            target += 0.2  # Wetter lips for crying/sad
        elif controller.emotion in ["happy", "excited", "laughing"]:
            target += 0.1  # Slightly more moisture for excited emotions
        
        # Smooth transitions
        self.lip_moisture = self.lip_moisture * 0.9 + target * 0.1
    
    def draw_nose_and_mouth(self, painter, offset_x=0, offset_y=0, emotion_data=None):
        """Draw nose and mouth combined for consistent positioning"""
        self.update_lip_moisture()
        
        # Draw nose first (with subtle emotion adjustments)
        self.draw_nose(painter, offset_x, offset_y, emotion_data)
        
        # Draw mouth with enhanced animation
        self.draw_mouth(painter, offset_x, offset_y, emotion_data)
    
    def draw_nose(self, painter, offset_x=0, offset_y=0, emotion_data=None):
        """Draw the character's nose with subtle emotion adjustments"""
        if not emotion_data:
            emotion_data = get_emotion_data(self.renderer.controller.emotion)
            
        # Subtle nose adjustments based on emotion
        nose_y_adjust = 0
        if emotion_data.name in ["happy", "laughing", "excited"]:
            nose_y_adjust = 2  # Nose moves slightly up with smile
        elif emotion_data.name in ["sad", "crying"]:
            nose_y_adjust = -1  # Nose moves slightly down with frown
            
        painter.setPen(QPen(QColor("black"), 1))
        
        nose_path = QPainterPath()
        self.renderer.moveto(nose_path, 309 + offset_x, 270 + offset_y - nose_y_adjust)
        self.renderer.Xh = self.renderer.Yh = 0
        
        # Slightly adjust nose shape based on emotion
        if emotion_data.name in ["angry", "shocked"]:
            self.renderer.curveto_r(nose_path, 0, 0, 5, 7, 2, 9)  # Sharper nose
        else:
            self.renderer.curveto_r(nose_path, 0, 0, 4, 7, 1, 9)  # Standard nose
            
        painter.drawPath(nose_path)
    
    def draw_mouth(self, painter, offset_x=0, offset_y=0, emotion_data=None):
        """Draw the mouth with enhanced animation and details"""
        if not emotion_data:
            emotion_data = get_emotion_data(self.renderer.controller.emotion)
            
        mouth_shape = MOUTH_SHAPES[emotion_data.mouth_type]
        
        # Get talk factor with smoothing for natural transitions
        talk_factor = self.renderer.controller.talk_factor
        talk_factor = self.last_talk_factor * (1 - self.talk_transition_speed) + talk_factor * self.talk_transition_speed
        self.last_talk_factor = talk_factor
        
        # Draw the mouth based on talk state
        if talk_factor > 0.05:  # Talking
            self.draw_talking_mouth(painter, mouth_shape.talking, offset_x, offset_y, talk_factor, emotion_data)
        else:  # Closed mouth
            self.draw_closed_mouth(painter, mouth_shape.closed, offset_x, offset_y, emotion_data)
    
    def draw_talking_mouth(self, painter, talking_data, offset_x, offset_y, talk_factor, emotion_data):
        """Draw mouth in talking position with enhanced details"""
        # Mouth outline
        path = QPainterPath()
        self.renderer.moveto(path, talking_data.start_x + offset_x, 
                   talking_data.start_y + offset_y)
        self.renderer.Xh = self.renderer.Yh = 0
        
        # Calculate dynamic intensity based on talk factor and emotion
        intensity = talk_factor * (1.0 + random.uniform(-0.1, 0.1))  # Add subtle randomness
        if emotion_data.name in ["excited", "shocked", "laughing"]:
            intensity *= 1.3  # More dramatic mouth movement
        elif emotion_data.name in ["shy", "sleepy", "bored"]:
            intensity *= 0.7  # More subtle mouth movement
        
        # Draw upper lip with animation and color
        upper_lip_path = QPainterPath()
        self.renderer.moveto(upper_lip_path, talking_data.start_x + offset_x, 
                   talking_data.start_y + offset_y)
        self.renderer.Xh = self.renderer.Yh = 0
        
        for curve_type, *params in talking_data.upper_lip:
            if curve_type == "curveto_r":
                adjusted_params = self.adjust_for_talk_animation(params, intensity=intensity)
                self.renderer.curveto_r(upper_lip_path, *adjusted_params)
        
        # Draw right corner
        right_corner_path = QPainterPath(upper_lip_path.currentPosition())
        if talking_data.corners and len(talking_data.corners) > 0:
            corner_type, *corner_params = talking_data.corners[0]
            if corner_type == "curveto_r":
                adjusted_params = self.adjust_for_talk_animation(corner_params, is_corner=True, intensity=intensity)
                self.renderer.curveto_r(right_corner_path, *adjusted_params)
        
        upper_lip_path.connectPath(right_corner_path)
        
        # Calculate upper lip endpoint for later
        upper_lip_end = right_corner_path.currentPosition()
        
        # Draw lower lip
        lower_lip_path = QPainterPath(upper_lip_end)
        
        for curve_type, *params in talking_data.lower_lip:
            if curve_type == "curveto_r":
                adjusted_params = self.adjust_for_talk_animation(params, lower_lip=True, intensity=intensity)
                self.renderer.curveto_r(lower_lip_path, *adjusted_params)
        
        # Draw left corner
        left_corner_path = QPainterPath(lower_lip_path.currentPosition())
        if talking_data.corners and len(talking_data.corners) > 1:
            corner_type, *corner_params = talking_data.corners[1]
            if corner_type == "curveto_r":
                adjusted_params = self.adjust_for_talk_animation(corner_params, is_corner=True, intensity=intensity)
                self.renderer.curveto_r(left_corner_path, *adjusted_params)
        
        lower_lip_path.connectPath(left_corner_path)
        
        # Create complete mouth path
        mouth_path = QPainterPath(upper_lip_path)
        mouth_path.connectPath(lower_lip_path)
        mouth_path.connectPath(left_corner_path)
        mouth_path.closeSubpath()
        
        # Draw mouth interior with gradient
        mouth_gradient = QRadialGradient()
        mouth_gradient.setCenter(QPointF(talking_data.start_x + 15 + offset_x, 
                                         talking_data.start_y + 12 + offset_y + intensity * 4))
        mouth_gradient.setFocalPoint(QPointF(talking_data.start_x + 15 + offset_x, 
                                            talking_data.start_y + 8 + offset_y + intensity * 4))
        mouth_gradient.setRadius(30)
        
        # Adjust gradient colors based on emotion
        dark_color = QColor(40, 10, 10, 220)
        mid_color = QColor(90, 20, 20, 200)
        
        if emotion_data.name in ["excited", "laughing"]:
            dark_color.setRed(60)  # Brighter mouth for excited emotions
        elif emotion_data.name in ["sad", "crying"]:
            dark_color.setAlpha(250)  # Darker mouth for sad emotions
            
        mouth_gradient.setColorAt(0, mid_color)
        mouth_gradient.setColorAt(0.7, dark_color)
        
        painter.setBrush(QBrush(mouth_gradient))
        painter.setPen(QPen(QColor("black"), 1.0))
        painter.drawPath(mouth_path)
        
        # Draw inner mouth detail if available and talking enough
        if intensity > 0.5 and talking_data.inner_detail:
            self.draw_enhanced_inner_mouth_detail(painter, talking_data.inner_detail, offset_x, offset_y, intensity, emotion_data)
        
        # Draw lip shading and highlights
        self.draw_lip_details(painter, mouth_path, intensity, emotion_data)
    
    def draw_closed_mouth(self, painter, closed_data, offset_x, offset_y, emotion_data):
        """Draw mouth in closed position with enhanced details"""
        path = QPainterPath()
        self.renderer.moveto(path, closed_data.start_x + offset_x, 
                   closed_data.start_y + offset_y)
        self.renderer.Xh = self.renderer.Yh = 0
        
        # If the mouth has multiple curves, it's a more complex mouth shape
        complex_mouth = len(closed_data.curves) > 1
        
        # Create paths for upper and lower lips for complex mouths
        if complex_mouth:
            upper_path = QPainterPath()
            lower_path = QPainterPath()
            
            self.renderer.moveto(upper_path, closed_data.start_x + offset_x, 
                       closed_data.start_y + offset_y)
            
            # Find midpoint in curves to separate upper/lower lips
            midpoint = len(closed_data.curves) // 2
            
            # Draw upper lip
            for i, (curve_type, *params) in enumerate(closed_data.curves):
                if i < midpoint:
                    if curve_type == "curveto_r":
                        self.renderer.curveto_r(upper_path, *params)
                    elif curve_type == "horizontal":
                        self.renderer.horizontal(upper_path, self.renderer.convert_x(upper_path.currentPosition().x()) + params[0])
            
            # Get the endpoint of upper lip for starting lower lip
            upper_end = upper_path.currentPosition()
            
            # Draw lower lip
            self.renderer.moveto(lower_path, upper_end.x(), upper_end.y())
            for i, (curve_type, *params) in enumerate(closed_data.curves):
                if i >= midpoint:
                    if curve_type == "curveto_r":
                        self.renderer.curveto_r(lower_path, *params)
                    elif curve_type == "horizontal":
                        self.renderer.horizontal(lower_path, self.renderer.convert_x(lower_path.currentPosition().x()) + params[0])
            
            # Create complete path
            path = QPainterPath(upper_path)
            path.connectPath(lower_path)
            path.closeSubpath()
            
            # Draw filled mouth with gradient
            lip_gradient = QLinearGradient()
            lip_gradient.setStart(QPointF(closed_data.start_x + offset_x, 
                                         closed_data.start_y + offset_y - 2))
            lip_gradient.setFinalStop(QPointF(closed_data.start_x + offset_x, 
                                             closed_data.start_y + offset_y + 5))
            
            # Get appropriate lip colors based on emotion
            lip_color = self.get_lip_color_for_emotion(emotion_data)
            lip_color_dark = QColor(lip_color)
            # FIX: Use int() to convert float to integer
            lip_color_dark.setRed(int(lip_color_dark.red() * 0.8))
            
            lip_gradient.setColorAt(0, lip_color)
            lip_gradient.setColorAt(1, lip_color_dark)
            
            painter.setPen(QPen(QColor("black"), 1.0))
            painter.setBrush(QBrush(lip_gradient))
            painter.drawPath(path)
            
            # Draw lip line and highlights
            self.draw_lip_details(painter, path, 0, emotion_data) 
        else:
            # Simple mouth - just a line
            for curve_type, *params in closed_data.curves:
                if curve_type == "curveto_r":
                    self.renderer.curveto_r(path, *params)
                elif curve_type == "horizontal":
                    self.renderer.horizontal(path, self.renderer.convert_x(path.currentPosition().x()) + params[0])
            
            # Draw the line with thicker pen for simple mouths
            pen = QPen(QColor("black"), 1.5)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            painter.drawPath(path)
            
            # Add subtle lip color hint below the mouth line for certain emotions
            if emotion_data.name in ["happy", "shy", "winking", "excited"]:
                lip_hint = QPainterPath()
                current_pos = path.currentPosition()
                start_pos = path.elementAt(0)
                
                self.renderer.moveto(lip_hint, start_pos.x, start_pos.y + 2)
                
                # Create subtle curve below the mouth
                mid_x = (start_pos.x + current_pos.x) / 2
                mid_y = start_pos.y + 3 + (1 if emotion_data.name == "happy" else 0)
                
                self.renderer.curveto(lip_hint, 
                                    mid_x - 10, mid_y,
                                    mid_x + 10, mid_y,
                                    current_pos.x, current_pos.y + 2)
                
                # Draw subtle lip coloring
                painter.setPen(Qt.PenStyle.NoPen)
                lip_color = self.get_lip_color_for_emotion(emotion_data)
                lip_color.setAlpha(60)  # Very subtle
                painter.setBrush(QBrush(lip_color))
                painter.drawPath(lip_hint)
    
    def adjust_for_talk_animation(self, params, is_corner=False, lower_lip=False, intensity=1.0):
        """Adjust curve parameters for talking animation with enhanced dynamics"""
        adjusted_params = []
        talk_factor = intensity  # Use provided intensity
        
        # Add subtle left/right shift to params for more natural movement
        horizontal_shift = random.uniform(-0.5, 0.5) * talk_factor
        
        for i, param in enumerate(params):
            if i % 2 == 0:  # X coordinates - add subtle horizontal movement
                adjusted_params.append(param + horizontal_shift)
            else:  # Y coordinates
                if is_corner and i > 2:  # Corner adjustment
                    adjusted_params.append(param + (talk_factor * 4))
                elif lower_lip:  
                    # Lower lip moves more for most emotions
                    adjusted_params.append(param + (talk_factor * 6.5))
                else:
                    # Upper lip has less movement
                    adjusted_params.append(param + (talk_factor * 3.8))
        
        return adjusted_params
    
    def draw_enhanced_inner_mouth_detail(self, painter, inner_detail, offset_x, offset_y, intensity, emotion_data):
        """Draw enhanced inner mouth detail for talking animation"""
        # Create tongue path
        tongue_path = QPainterPath()
        
        talk_offset = intensity * 4
        self.renderer.moveto(tongue_path, 298 + offset_x,
                   310 + offset_y + talk_offset)
        self.renderer.Xh = self.renderer.Yh = 0
        
        # Make the tongue shape more dynamic based on intensity
        adjusted_curves = []
        for curve_type, *params in inner_detail["curves"]:
            if curve_type == "curveto_r":
                adjusted_params = []
                for i, param in enumerate(params):
                    # Add subtle randomness to tongue position 
                    random_factor = random.uniform(0.8, 1.2)
                    adjusted_params.append(param * random_factor)
                adjusted_curves.append((curve_type, *adjusted_params))
        
        # Draw the tongue curves
        for curve_type, *params in adjusted_curves:
            if curve_type == "curveto_r":
                self.renderer.curveto_r(tongue_path, *params)
        
        tongue_path.closeSubpath()
        
        # Create tongue gradient
        tongue_gradient = QRadialGradient()
        center_x = 310 + offset_x
        center_y = 315 + offset_y + talk_offset
        tongue_gradient.setCenter(center_x, center_y)
        tongue_gradient.setFocalPoint(center_x - 5, center_y - 2)
        tongue_gradient.setRadius(20)
        
        # Get tongue color based on emotion
        base_color = QColor(inner_detail["color"])
        if emotion_data.name in ["excited", "laughing"]:
            base_color = QColor(255, 120, 120)  # Brighter for excited
        elif emotion_data.name in ["angry", "shocked"]:
            base_color = QColor(230, 90, 90)  # Deeper red for angry
            
        # Create gradient
        tongue_gradient.setColorAt(0.2, base_color)
        darker = QColor(base_color)
        # FIX: Use int() to convert float to integer
        darker.setRed(int(base_color.red() * 0.7))
        tongue_gradient.setColorAt(0.8, darker)
        
        painter.setPen(QPen(QColor(180, 70, 70, 200), 0.5))
        painter.setBrush(QBrush(tongue_gradient))
        painter.drawPath(tongue_path)
        
        # Add texture details to tongue
        if intensity > 0.7:
            self.draw_tongue_texture(painter, tongue_path, center_x, center_y)
    
    def draw_tongue_texture(self, painter, tongue_path, center_x, center_y):
        """Add realistic texture to the tongue"""
        painter.setPen(QPen(QColor(180, 70, 70, 40), 0.5))
        
        # Draw a few curved lines to suggest the tongue's center line and texture
        texture_path = QPainterPath()
        texture_path.moveTo(center_x - 10, center_y)
        texture_path.cubicTo(
            center_x - 5, center_y - 2,
            center_x + 5, center_y - 2,
            center_x + 10, center_y
        )
        painter.drawPath(texture_path)
        
        # Add a few more subtle texture lines
        for i in range(3):
            offset = i * 1.5
            texture_path = QPainterPath()
            texture_path.moveTo(center_x - 8, center_y + offset)
            texture_path.cubicTo(
                center_x - 3, center_y + offset - 1,
                center_x + 3, center_y + offset - 1,
                center_x + 8, center_y + offset
            )
            painter.drawPath(texture_path)
    
    def draw_lip_details(self, painter, mouth_path, intensity, emotion_data):
        """Add shading and highlights to lips"""
        # Draw lip line with proper thickness
        painter.setPen(QPen(QColor("black"), 1.0))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(mouth_path)
        
        # Add highlight/shine to lips based on lip_moisture
        if self.lip_moisture > 0.5:
            # Get lip area
            bounds = mouth_path.boundingRect()
            
            # Create highlight path - a thin curved line on the bottom lip
            highlight_path = QPainterPath()
            highlight_path.moveTo(bounds.left() + bounds.width() * 0.3, 
                                 bounds.top() + bounds.height() * 0.7)
            
            # Create a curved highlight
            highlight_path.cubicTo(
                bounds.left() + bounds.width() * 0.4, bounds.top() + bounds.height() * 0.65,
                bounds.left() + bounds.width() * 0.6, bounds.top() + bounds.height() * 0.65,
                bounds.left() + bounds.width() * 0.7, bounds.top() + bounds.height() * 0.7
            )
            
            # Draw highlight with proper opacity based on moisture
            highlight_color = QColor(255, 255, 255, int(80 * self.lip_moisture))
            painter.setPen(QPen(highlight_color, 1.5))
            painter.drawPath(highlight_path)
            
            # For very moist/crying lips, add a second highlight
            if self.lip_moisture > 0.9 and emotion_data.name in ["crying", "sad"]:
                second_highlight = QPainterPath()
                second_highlight.moveTo(bounds.left() + bounds.width() * 0.35, 
                                      bounds.top() + bounds.height() * 0.4)
                second_highlight.cubicTo(
                    bounds.left() + bounds.width() * 0.45, bounds.top() + bounds.height() * 0.35,
                    bounds.left() + bounds.width() * 0.55, bounds.top() + bounds.height() * 0.35,
                    bounds.left() + bounds.width() * 0.65, bounds.top() + bounds.height() * 0.4
                )
                
                painter.setPen(QPen(QColor(255, 255, 255, 40), 1.0))
                painter.drawPath(second_highlight)
    
    def get_lip_color_for_emotion(self, emotion_data):
        """Get appropriate lip color based on emotion"""
        base_color = QColor(self.lip_color_base)
        
        if emotion_data.name in ["angry", "shocked"]:
            # Redder for angry
            base_color.setRed(255)
            base_color.setGreen(130)
        elif emotion_data.name in ["sad", "crying"]:
            # More purple/blue for sad
            base_color.setRed(230)
            base_color.setGreen(140)
            base_color.setBlue(150)
        elif emotion_data.name in ["excited", "laughing"]:
            # Brighter for excited/laughing
            base_color.setRed(255)
            base_color.setGreen(180)
        elif emotion_data.name in ["shy", "winking"]:
            # Softer pink for shy
            base_color.setRed(255)
            base_color.setGreen(170)
            base_color.setBlue(170)
            
        # Adjust alpha based on emotion and moisture
        base_color.setAlpha(int(min(255, 180 + self.lip_moisture * 50)))
        
        return base_color