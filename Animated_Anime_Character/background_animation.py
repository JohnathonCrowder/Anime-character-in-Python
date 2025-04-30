from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath, QLinearGradient, QRadialGradient
import math
import random

class BackgroundRenderer:
    def __init__(self, renderer):
        self.renderer = renderer
        self.timer = 0
        self.stars = []
        self.shooting_stars = []
        self.create_stars(150)  # Create initial stars
        self.moon_phase = 0.8  # 0 to 1, where 1 is full moon
        self.fireflies = self.create_fireflies(20)
        self.hills = self.generate_hills()
        self.trees = self.generate_trees(8)
        
        # Create a new shooting star every few seconds
        self.shooting_star_timer = random.randint(100, 200)
        
    def create_stars(self, count):
        """Create stars for the night sky"""
        for _ in range(count):
            self.stars.append({
                'x': random.uniform(0, self.renderer.width),
                'y': random.uniform(0, self.renderer.height * 0.7),  # Keep stars in the sky
                'size': random.uniform(1, 3),
                'brightness': random.uniform(0.5, 1.0),
                'twinkle_speed': random.uniform(0.01, 0.05),
                'phase': random.uniform(0, 2 * math.pi),
                'color': self.get_star_color()
            })
    
    def get_star_color(self):
        """Get a random star color"""
        colors = [
            QColor(255, 255, 255),  # White
            QColor(255, 255, 220),  # Warm white
            QColor(220, 220, 255),  # Bluish white
            QColor(255, 230, 200),  # Slight orange
            QColor(200, 230, 255),  # Slight blue
        ]
        return random.choice(colors)
    
    def create_shooting_star(self):
        """Create a new shooting star"""
        start_x = random.uniform(0, self.renderer.width)
        start_y = random.uniform(0, self.renderer.height * 0.4)
        angle = random.uniform(math.pi * 0.1, math.pi * 0.4)  # Downward angle
        
        if random.random() > 0.5:  # Randomly go left or right
            angle = math.pi - angle  # Flip angle
        
        length = random.uniform(50, 150)
        
        return {
            'x': start_x,
            'y': start_y,
            'angle': angle,
            'speed': random.uniform(5, 10),
            'length': length,
            'progress': 0,
            'lifetime': random.uniform(30, 60),
            'thickness': random.uniform(1, 2),
            'color': QColor(255, 255, 255)
        }
    
    def create_fireflies(self, count):
        """Create fireflies for the countryside"""
        fireflies = []
        for _ in range(count):
            fireflies.append({
                'x': random.uniform(0, self.renderer.width),
                'y': random.uniform(self.renderer.height * 0.5, self.renderer.height * 0.9),
                'size': random.uniform(1.5, 3),
                'brightness': random.uniform(0.3, 1.0),
                'speed': random.uniform(0.3, 0.8),
                'angle': random.uniform(0, 2 * math.pi),
                'glow_phase': random.uniform(0, 2 * math.pi),
                'glow_speed': random.uniform(0.03, 0.08)
            })
        return fireflies
    
    def generate_hills(self):
        """Generate silhouette hills for the countryside"""
        hills = []
        
        # Create 3 layers of hills with different heights
        for layer in range(3):
            hill = {
                'points': [],
                'height': self.renderer.height * (0.75 - layer * 0.06),  # Different base height for each layer
                'color': QColor(20 + layer * 15, 30 + layer * 15, 20 + layer * 15)  # Slightly different colors
            }
            
            # Generate points for a smooth hill
            num_points = 10 + layer * 5
            x_step = self.renderer.width / (num_points - 3)
            
            # Start and end below the screen
            hill['points'].append(QPointF(-10, self.renderer.height))
            
            for i in range(num_points):
                x = i * x_step
                
                # Calculate height with randomness, but ensure it's within bounds
                height_factor = 0.1 + 0.15 * layer
                y_offset = random.uniform(0, self.renderer.height * height_factor)
                y = hill['height'] - y_offset
                
                hill['points'].append(QPointF(x, y))
            
            # End below the screen
            hill['points'].append(QPointF(self.renderer.width + 10, self.renderer.height))
            hills.append(hill)
        
        return hills
    
    def generate_trees(self, count):
        """Generate trees for the countryside"""
        trees = []
        for _ in range(count):
            trees.append({
                'x': random.uniform(0, self.renderer.width),
                'y': random.uniform(self.renderer.height * 0.75, self.renderer.height * 0.85),
                'height': random.uniform(70, 150),
                'width': random.uniform(30, 60)
            })
        return trees
    
    def update(self):
        """Update background animation"""
        self.timer += 1
        
        # Update star twinkle
        for star in self.stars:
            star['phase'] += star['twinkle_speed']
        
        # Update fireflies
        for firefly in self.fireflies:
            # Update glow
            firefly['glow_phase'] += firefly['glow_speed']
            
            # Move the firefly in a random-ish pattern
            if random.random() < 0.02:
                firefly['angle'] += random.uniform(-0.5, 0.5)
            
            # Move forward and add slight vertical motion
            firefly['x'] += math.cos(firefly['angle']) * firefly['speed']
            firefly['y'] += math.sin(firefly['angle']) * firefly['speed'] * 0.5
            
            # Wrap around screen edges
            if firefly['x'] < 0:
                firefly['x'] = self.renderer.width
            elif firefly['x'] > self.renderer.width:
                firefly['x'] = 0
                
            # Keep within a certain height range
            min_height = self.renderer.height * 0.5
            max_height = self.renderer.height * 0.9
            if firefly['y'] < min_height:
                firefly['y'] = min_height
                firefly['angle'] = random.uniform(0, math.pi)  # Force downward
            elif firefly['y'] > max_height:
                firefly['y'] = max_height
                firefly['angle'] = random.uniform(math.pi, 2 * math.pi)  # Force upward
        
        # Handle shooting stars
        self.shooting_star_timer -= 1
        if self.shooting_star_timer <= 0:
            self.shooting_stars.append(self.create_shooting_star())
            self.shooting_star_timer = random.randint(100, 200)
        
        # Update existing shooting stars
        for star in self.shooting_stars[:]:
            star['progress'] += star['speed']
            if star['progress'] > star['lifetime']:
                self.shooting_stars.remove(star)
    
    def draw_background(self, painter):
        """Draw the animated background"""
        # Draw night sky gradient
        self.draw_night_sky(painter)
        
        # Draw stars
        self.draw_stars(painter)
        
        # Draw shooting stars
        self.draw_shooting_stars(painter)
        
        # Draw moon
        self.draw_moon(painter)
        
        # Draw hills
        self.draw_hills(painter)
        
        # Draw trees
        self.draw_trees(painter)
        
        # Draw fireflies
        self.draw_fireflies(painter)
    
    def draw_night_sky(self, painter):
        """Draw gradient night sky"""
        gradient = QLinearGradient(0, 0, 0, self.renderer.height * 0.8)
        
        # Deep space to horizon gradient
        gradient.setColorAt(0, QColor(10, 10, 35))  # Deep space blue
        gradient.setColorAt(0.4, QColor(20, 20, 60))  # Dark blue
        gradient.setColorAt(0.7, QColor(40, 20, 65))  # Deep purple
        gradient.setColorAt(1, QColor(60, 30, 50))  # Lighter purple/pink horizon
        
        painter.fillRect(0, 0, self.renderer.width, self.renderer.height, gradient)
    
    def draw_stars(self, painter):
        """Draw twinkling stars"""
        painter.setPen(Qt.PenStyle.NoPen)
        
        for star in self.stars:
            # Calculate twinkle factor
            twinkle = 0.5 + 0.5 * math.sin(star['phase'] + self.timer * star['twinkle_speed'])
            current_brightness = star['brightness'] * twinkle
            
            # Create a glow effect
            glow_color = QColor(star['color'])
            glow_color.setAlpha(int(100 * current_brightness))
            painter.setBrush(QBrush(glow_color))
            glow_size = star['size'] * 2.5
            painter.drawEllipse(QPointF(star['x'], star['y']), glow_size, glow_size)
            
            # Draw the star itself
            star_color = QColor(star['color'])
            star_color.setAlpha(int(255 * current_brightness))
            painter.setBrush(QBrush(star_color))
            painter.drawEllipse(QPointF(star['x'], star['y']), star['size'], star['size'])
    
    def draw_shooting_stars(self, painter):
        """Draw shooting stars"""
        for star in self.shooting_stars:
            # Calculate the start and end points of the streak
            end_x = star['x']
            end_y = star['y']
            start_x = end_x - math.cos(star['angle']) * star['progress']
            start_y = end_y - math.sin(star['angle']) * star['progress']
            
            # Calculate the length based on progress
            curr_length = min(star['length'], star['progress'])
            trail_x = start_x + math.cos(star['angle']) * (star['progress'] - curr_length)
            trail_y = start_y + math.sin(star['angle']) * (star['progress'] - curr_length)
            
            # Draw the trail with a gradient
            gradient = QLinearGradient(end_x, end_y, trail_x, trail_y)
            gradient.setColorAt(0, QColor(255, 255, 255, 200))
            gradient.setColorAt(1, QColor(255, 255, 255, 0))
            
            # Fix the QPen initialization
            pen = QPen()
            pen.setBrush(QBrush(gradient))
            pen.setWidth(int(star['thickness']))
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            
            painter.drawLine(QPointF(trail_x, trail_y), QPointF(end_x, end_y))
            
            # Draw the bright head
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(255, 255, 255, 230)))
            painter.drawEllipse(QPointF(end_x, end_y), star['thickness'] * 2, star['thickness'] * 2)
    
    def draw_moon(self, painter):
        """Draw the moon"""
        # Position the moon
        moon_x = self.renderer.width * 0.8
        moon_y = self.renderer.height * 0.2
        moon_radius = 35
        
        # Create moon glow
        for i in range(4):
            alpha = 40 - i * 10
            size = moon_radius * (1 + i * 0.5)
            glow_color = QColor(220, 220, 180, alpha)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(glow_color))
            painter.drawEllipse(QPointF(moon_x, moon_y), size, size)
        
        # Draw the full moon
        painter.setBrush(QBrush(QColor(230, 230, 200)))
        painter.drawEllipse(QPointF(moon_x, moon_y), moon_radius, moon_radius)
        
        # Apply moon phase (if not full)
        if self.moon_phase < 1.0:
            shadow_width = moon_radius * 2 * (1.0 - self.moon_phase)
            offset = moon_radius - shadow_width / 2
            
            # Draw the shadow part
            painter.setBrush(QBrush(QColor(10, 10, 35)))  # Same as sky color
            painter.drawEllipse(QPointF(moon_x + offset, moon_y), shadow_width / 2, moon_radius)
        
        # Draw some subtle craters
        painter.setPen(QPen(QColor(210, 210, 180), 1))
        painter.setBrush(QBrush(QColor(220, 220, 190)))
        
        # Draw several small craters
        crater_positions = [
            (moon_x - moon_radius * 0.3, moon_y - moon_radius * 0.4, moon_radius * 0.15),
            (moon_x + moon_radius * 0.4, moon_y + moon_radius * 0.2, moon_radius * 0.1),
            (moon_x - moon_radius * 0.1, moon_y + moon_radius * 0.5, moon_radius * 0.12),
        ]
        
        for x, y, size in crater_positions:
            # Only draw if visible (not in shadow)
            if self.moon_phase == 1.0 or x < moon_x + offset:
                painter.drawEllipse(QPointF(x, y), size, size)
    
    def draw_hills(self, painter):
        """Draw the countryside hills"""
        for hill in self.hills:
            # Create a path from the points
            path = QPainterPath()
            path.moveTo(hill['points'][0])
            
            for point in hill['points'][1:]:
                path.lineTo(point)
            
            # Fill the hill
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(hill['color']))
            painter.drawPath(path)
    
    def draw_trees(self, painter):
        """Draw silhouette trees"""
        for tree in self.trees:
            # Draw trunk
            trunk_width = tree['width'] * 0.2
            trunk_height = tree['height'] * 0.3
            
            trunk = QRectF(
                tree['x'] - trunk_width/2,
                tree['y'] - trunk_height,
                trunk_width,
                trunk_height
            )
            
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor(30, 20, 10)))
            painter.drawRect(trunk)
            
            # Draw foliage (triangular for pine trees)
            foliage_width = tree['width']
            foliage_height = tree['height'] * 0.7
            
            foliage_path = QPainterPath()
            foliage_path.moveTo(tree['x'] - foliage_width/2, tree['y'] - trunk_height)
            foliage_path.lineTo(tree['x'] + foliage_width/2, tree['y'] - trunk_height)
            foliage_path.lineTo(tree['x'], tree['y'] - trunk_height - foliage_height)
            foliage_path.closeSubpath()
            
            painter.setBrush(QBrush(QColor(20, 40, 20)))
            painter.drawPath(foliage_path)
    
    def draw_fireflies(self, painter):
        """Draw glowing fireflies"""
        for firefly in self.fireflies:
            # Calculate glow based on phase
            glow = 0.5 + 0.5 * math.sin(firefly['glow_phase'])
            current_brightness = firefly['brightness'] * glow
            
            # Draw outer glow
            glow_color = QColor(230, 255, 150, int(100 * current_brightness))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(glow_color))
            glow_size = firefly['size'] * 3
            painter.drawEllipse(QPointF(firefly['x'], firefly['y']), glow_size, glow_size)
            
            # Draw inner bright spot
            bright_color = QColor(255, 255, 200, int(255 * current_brightness))
            painter.setBrush(QBrush(bright_color))
            painter.drawEllipse(QPointF(firefly['x'], firefly['y']), firefly['size'], firefly['size'])