import turtle as pp
import math
import random
from emotions import EYEBROW_SHAPES, MOUTH_SHAPES, get_emotion_data

# Constants
WIDTH = 600
HEIGHT = 500
WRIPP_SPP = 15  # Sampling times of Bessel function

# Global variables for Bezier calculations
Xh = 0
Yh = 0

# Bezier curve functions
def Bezier(p1, p2, t):
    return p1 * (1 - t) + p2 * t

def Bezier_2(x1, y1, x2, y2, x3, y3):
    pp.goto(x1, y1)
    pp.pendown()
    for t in range(0, WRIPP_SPP + 1):
        x = Bezier(Bezier(x1, x2, t / WRIPP_SPP),
                   Bezier(x2, x3, t / WRIPP_SPP), t / WRIPP_SPP)
        y = Bezier(Bezier(y1, y2, t / WRIPP_SPP),
                   Bezier(y2, y3, t / WRIPP_SPP), t / WRIPP_SPP)
        pp.goto(x, y)
    pp.penup()

def Bezier_3(x1, y1, x2, y2, x3, y3, x4, y4):
    x1 = -WIDTH / 2 + x1
    y1 = HEIGHT / 2 - y1
    x2 = -WIDTH / 2 + x2
    y2 = HEIGHT / 2 - y2
    x3 = -WIDTH / 2 + x3
    y3 = HEIGHT / 2 - y3
    x4 = -WIDTH / 2 + x4
    y4 = HEIGHT / 2 - y4
    pp.goto(x1, y1)
    pp.pendown()
    for t in range(0, WRIPP_SPP + 1):
        x = Bezier(Bezier(Bezier(x1, x2, t / WRIPP_SPP), Bezier(x2, x3, t / WRIPP_SPP), t / WRIPP_SPP),
                   Bezier(Bezier(x2, x3, t / WRIPP_SPP), Bezier(x3, x4, t / WRIPP_SPP), t / WRIPP_SPP), t / WRIPP_SPP)
        y = Bezier(Bezier(Bezier(y1, y2, t / WRIPP_SPP), Bezier(y2, y3, t / WRIPP_SPP), t / WRIPP_SPP),
                   Bezier(Bezier(y2, y3, t / WRIPP_SPP), Bezier(y3, y4, t / WRIPP_SPP), t / WRIPP_SPP), t / WRIPP_SPP)
        pp.goto(x, y)
    pp.penup()

# Utility functions
def Moveto(x, y):
    pp.penup()
    pp.goto(-WIDTH / 2 + x, HEIGHT / 2 - y)

def line(x1, y1, x2, y2):
    pp.penup()
    pp.goto(-WIDTH / 2 + x1, HEIGHT / 2 - y1)
    pp.pendown()
    pp.goto(-WIDTH / 2 + x2, HEIGHT / 2 - y2)
    pp.penup()

def lineto(dx, dy):
    pp.pendown()
    pp.goto(pp.xcor() + dx, pp.ycor() - dy)
    pp.penup()

def Lineto(x, y):
    pp.pendown()
    pp.goto(-WIDTH / 2 + x, HEIGHT / 2 - y)
    pp.penup()

def Horizontal(x):
    pp.pendown()
    pp.setx(x - WIDTH / 2)
    pp.penup()

def horizontal(dx):
    pp.seth(0)
    pp.pendown()
    pp.fd(dx)
    pp.penup()

def vertical(dy):
    pp.seth(-90)
    pp.pendown()
    pp.fd(dy)
    pp.penup()
    pp.seth(0)

def polyline(x1, y1, x2, y2, x3, y3):
    pp.penup()
    pp.goto(-WIDTH / 2 + x1, HEIGHT / 2 - y1)
    pp.pendown()
    pp.goto(-WIDTH / 2 + x2, HEIGHT / 2 - y2)
    pp.goto(-WIDTH / 2 + x3, HEIGHT / 2 - y3)
    pp.penup()

def Curveto(x1, y1, x2, y2, x, y):
    global Xh, Yh
    pp.penup()
    X_now = pp.xcor() + WIDTH / 2
    Y_now = HEIGHT / 2 - pp.ycor()
    Bezier_3(X_now, Y_now, x1, y1, x2, y2, x, y)
    Xh = x - x2
    Yh = y - y2

def curveto_r(x1, y1, x2, y2, x, y):
    global Xh, Yh
    pp.penup()
    X_now = pp.xcor() + WIDTH / 2
    Y_now = HEIGHT / 2 - pp.ycor()
    Bezier_3(X_now, Y_now, X_now + x1, Y_now + y1,
             X_now + x2, Y_now + y2, X_now + x, Y_now + y)
    Xh = x - x2
    Yh = y - y2

def Smooth(x2, y2, x, y):
    global Xh, Yh
    pp.penup()
    X_now = pp.xcor() + WIDTH / 2
    Y_now = HEIGHT / 2 - pp.ycor()
    Bezier_3(X_now, Y_now, X_now + Xh, Y_now + Yh, x2, y2, x, y)
    Xh = x - x2
    Yh = y - y2

def smooth_r(x2, y2, x, y):
    global Xh, Yh
    pp.penup()
    X_now = pp.xcor() + WIDTH / 2
    Y_now = HEIGHT / 2 - pp.ycor()
    Bezier_3(X_now, Y_now, X_now + Xh, Y_now + Yh,
             X_now + x2, Y_now + y2, X_now + x, Y_now + y)
    Xh = x - x2
    Yh = y - y2

# Character drawing functions
def draw_coat(offset_y=0):
    pp.color("black", "#F2F2F2")  # Coat
    Moveto(61, 462 + offset_y)
    pp.begin_fill()
    smooth_r(12, -41, 27, -58)
    curveto_r(-6, -36, 6, -118, 9, -132)
    curveto_r(-15, -27, -23, -51, -26, -74)
    curveto_r(4, -66, 38, -105, 65, -149)
    Horizontal(486)
    curveto_r(12, 24, 40, 99, 33, 114)
    curveto_r(39, 82, 55, 129, 39, 144)
    smooth_r(-31, 23, -39, 28)
    smooth_r(-12, 37, -12, 37)
    lineto(50, 92)
    Horizontal(445)
    smooth_r(-29, -38, -31, -46)
    smooth_r(78, -107, 72, -119)
    Smooth(355, 178, 340, 176)
    Smooth(272, 63, 264, 64)
    smooth_r(-29, 67, -27, 73)
    Curveto(99, 292, 174, 428, 173, 439)
    smooth_r(-8, 23, -8, 23)
    Lineto(61, 462 + offset_y)
    pp.end_fill()

    # Coat shadow
    Moveto(60.5, 461.5 + offset_y)
    pp.color("black", "#D3DFF0")
    pp.begin_fill()
    curveto_r(0, 0, 17, -42, 27, -59)
    curveto_r(-6, -33, 6, -128, 10, -133)
    curveto_r(-15, -10, -27, -66, -27.285, -75)
    pp.pencolor("#D3DFF0")
    curveto_r(12.285, 11, 82.963, 156, 82.963, 156)
    pp.pencolor("black")
    smooth_r(12.322, 75, 19.322, 86)
    curveto_r(-1, 11, -8, 25, -8, 25)
    Horizontal(60.5)
    pp.end_fill()

    # More coat parts
    Moveto(444.5, 464 + offset_y)
    pp.begin_fill()
    curveto_r(0, 0, -29, -36, -31, -46)
    smooth_r(53.59, -82.337, 53.59, -82.337)
    pp.pencolor("#D3DFF0")
    smooth_r(86.41, -47.663, 96.072, -54.85)
    Curveto(563.5, 297.5, 570.5, 299.5, 518.5, 334)
    pp.pencolor("black")
    curveto_r(-2, 16, -12, 33, -12, 37)
    smooth_r(50, 92, 50, 93)
    Horizontal(444.5)
    pp.end_fill()

def draw_jacket_inside(offset_y=0):
    pp.color("black", "#2b1d2a")  # Inside the jacket
    Moveto(225, 462 + offset_y)
    pp.begin_fill()
    Horizontal(165)
    smooth_r(9, -15, 8, -25)
    curveto_r(-47, -126, 6, -212, 12, -225)
    Curveto(185, 305, 202, 428, 225, 462 + offset_y)
    Lineto(225, 462 + offset_y)
    pp.end_fill()

    Moveto(390, 462 + offset_y)
    pp.begin_fill()
    curveto_r(10, -23, 34, -180, 35, -222)
    curveto_r(7, 4, 54, 45, 61, 61)
    smooth_r(-73, 101, -72, 118)
    curveto_r(5, 15, 31, 46, 31, 45)
    Lineto(390, 462 + offset_y)
    pp.end_fill()

    pp.color("black", "#2b1d29")  # Inside the jacket
    Moveto(225, 462 + offset_y)
    pp.begin_fill()
    curveto_r(-28, -50, -40, -166, -40, -250)
    curveto_r(6, 51, -6, 87, 45, 106)
    smooth_r(64, 27, 89, 24)
    smooth_r(49, -18, 56, -20)
    smooth_r(50, -10, 51, -85)
    curveto_r(0, 29, -25, 201, -36, 225)
    Lineto(225, 462 + offset_y)
    pp.end_fill()

def draw_clothes(offset_y=0):
    pp.color("black", "#3D3D3D")  # Clothes
    Moveto(225, 462 + offset_y)
    pp.begin_fill()
    curveto_r(-5, -5, -22, -53, -23, -70)
    lineto(32, -13)
    curveto_r(3, -25, 6, -28, 12, -36)
    smooth_r(13, -12, 16, -12)
    vertical(-2)
    curveto_r(45, 20, 64, 14, 94, 1)
    vertical(2)
    curveto_r(8, -2, 15, 2, 17, 4)
    smooth_r(0, 6, -2, 9)
    curveto_r(10, 10, 10, 29, 11, 33)
    smooth_r(23, 4, 25, 6)
    smooth_r(-17, 83, -17, 78)
    Lineto(225, 462 + offset_y)
    pp.end_fill()

def draw_neck(offset_y=0):
    pp.color("black", "#968281")  # Neck
    Moveto(262, 329 + offset_y)
    pp.begin_fill()
    vertical(17)
    curveto_r(1, 2, 44, 14, 45, 15)
    smooth_r(3, 12, 3, 12)
    horizontal(3)
    vertical(-5)
    curveto_r(1, -3, 4, -6, 5, -7)
    lineto(36, -14)
    curveto_r(1, -1, 3, -16, 2, -17)
    Curveto(318, 348 + offset_y, 296, 344 + offset_y, 262, 329 + offset_y)
    pp.end_fill()

def draw_collar(offset_y=0):
    pp.color("black", "#A2B8D6")  # Collar
    Moveto(262, 331 + offset_y)
    pp.begin_fill()
    curveto_r(0, 8, -1, 13, 0, 15)
    smooth_r(43, 14, 45, 15)
    lineto(3, 12)
    horizontal(3)
    smooth_r(-1, -3, 0, -5)
    lineto(5, -7)
    lineto(36, -14)
    curveto_r(1, -1, 2, -12, 2, -15)
    smooth_r(25, -2, 15, 13)
    curveto_r(-2, 4, -7, 29, -7, 32)
    smooth_r(-35, 19, -41, 22)
    smooth_r(-9, 14, -12, 14)
    smooth_r(-7, -12, -14, -15)
    curveto_r(-19, -2, -41, -25, -41, -25)
    smooth_r(-10, -26, -10, -30)
    Smooth(255, 332 + offset_y, 262, 331 + offset_y)
    pp.end_fill()

    Moveto(262, 346 + offset_y)
    lineto(-12, -6)
    Moveto(369, 333 + offset_y)
    curveto_r(2, 4, -6, 10, -15, 14)

    # Collar through bow tie parts
    pp.color("black", "#A2B8D6")
    Moveto(297, 387 + offset_y)
    pp.begin_fill()
    lineto(-11, 6)
    curveto_r(-1, 0, -20, -7, -30, -19)
    Curveto(259, 373 + offset_y, 297, 385 + offset_y, 297, 387 + offset_y)
    pp.end_fill()

    Moveto(323, 384 + offset_y)
    pp.begin_fill()
    lineto(8, 7)
    lineto(30, -14)
    curveto_r(1, -1, 5, -6, 4, -7)
    Smooth(329, 379 + offset_y, 323, 384 + offset_y)
    pp.end_fill()

def draw_tie(offset_y=0):
    pp.color("black", "#151515")  # Tie
    Moveto(247, 358 + offset_y)
    pp.begin_fill()
    curveto_r(-5, 3, -8, 20, -6, 23)
    curveto_r(25, 21, 50, 17, 50, 17)
    lineto(-23, 64)
    horizontal(22)
    smooth_r(1, -13, 2, -16)
    lineto(13, -50)
    curveto_r(2, 2, 7, 3, 10, 1)
    smooth_r(18, 65, 18, 65)
    horizontal(19)
    lineto(-24, -65)
    curveto_r(21, 5, 39, -10, 44, -13)
    curveto_r(5, -20, 1, -21, 0, -24)
    curveto_r(-18, -2, -49, 15, -52, 17)
    smooth_r(-11, -3, -15, -1)
    Smooth(252, 356 + offset_y, 247, 358 + offset_y)
    pp.end_fill()

def draw_face(offset_x=0, offset_y=0):
    pp.color("black", "#F3EEEB")  # Face
    Moveto(185 + offset_x, 212 + offset_y)
    pp.begin_fill()
    curveto_r(4, -9, 46, -77, 52, -75)
    curveto_r(-2, -17, 19, -68, 27, -73)
    curveto_r(16, 15, 71, 108, 76, 112)
    smooth_r(76, 53, 86, 60)
    curveto_r(0, 65, -27, 75, -31, 76)
    curveto_r(-50, 28, -70, 30, -85, 30)
    smooth_r(-77, -22, -86, -26)
    Curveto(180 + offset_x, 302 + offset_y, 186 + offset_x, 228 + offset_y, 185 + offset_x, 212 + offset_y)
    pp.end_fill()

def draw_hair(offset_x=0, offset_y=0):
    pp.color("black", "#2B1D29")  # Hair
    Moveto(189 + offset_x, 202 + offset_y)
    pp.begin_fill()
    curveto_r(-1, 22, 19, 51, 19, 51)
    smooth_r(-10, -42, 7, -92)
    Curveto(212 + offset_x, 168 + offset_y, 196 + offset_x, 189 + offset_y, 189 + offset_x, 202 + offset_y)
    pp.end_fill()

    Moveto(221 + offset_x, 155 + offset_y)
    pp.begin_fill()
    curveto_r(-2, 6, 5, 48, 5, 48)
    smooth_r(18, -28, 20, -48)
    curveto_r(-5, 24, 4, 43, 7, 50)
    curveto_r(-10, -49, 3, -72, 13, -106)
    curveto_r(-2, -7, -3, -32, -3, -35)
    curveto_r(-17, 18, -27, 71, -27, 71)
    Lineto(221 + offset_x, 155 + offset_y)
    pp.end_fill()

    Moveto(264 + offset_x, 64 + offset_y)
    pp.begin_fill()
    curveto_r(-4, 5, 14, 100, 14, 100)
    smooth_r(-6, -79, -5, -85)
    curveto_r(0, 98, 49, 139, 49, 139)
    smooth_r(8, -50, 3, -65)
    Smooth(272 + offset_x, 64 + offset_y, 264 + offset_x, 64 + offset_y)
    pp.end_fill()

    Moveto(342 + offset_x, 176 + offset_y)
    pp.begin_fill()
    curveto_r(-1, 27, -10, 57, -10, 57)
    smooth_r(20, -33, 17, -54)
    Lineto(342 + offset_x, 176 + offset_y)
    pp.end_fill()

    pp.penup()
    pp.begin_fill()
    polyline(349 + offset_x, 180 + offset_y, 353 + offset_x, 203 + offset_y, 361 + offset_x, 203 + offset_y)
    polyline(361 + offset_x, 203 + offset_y, 362 + offset_x, 188 + offset_y, 349 + offset_x, 180 + offset_y)
    pp.end_fill()

def draw_eyebrows(offset_x=0, offset_y=0, emotion="neutral"):
    emotion_data = get_emotion_data(emotion)
    eyebrow_shape = EYEBROW_SHAPES[emotion_data.eyebrow_type]
    
    pp.pensize(2)
    
    # Left eyebrow
    Moveto(210 + offset_x, eyebrow_shape.left_start_y + offset_y)
    for curve_params in eyebrow_shape.left_curve:
        curveto_r(*curve_params)
    
    # Right eyebrow
    Moveto(338 + offset_x, eyebrow_shape.right_start_y + offset_y)
    for curve_params in eyebrow_shape.right_curve:
        curveto_r(*curve_params)
    
    pp.pensize(1)

def draw_eyes(offset_x=0, offset_y=0, blink_factor=0, emotion="neutral"):
    emotion_data = get_emotion_data(emotion)
    
    # Adjust blink factor for sleepy emotions
    if emotion == "sleepy" and blink_factor < emotion_data.blink_adjust:
        blink_factor = emotion_data.blink_adjust
    
    # Special case for winking - force right eye closed
    winking = emotion == "winking"
    
    # Eyes base
    pp.color("black", "#D1D1D1")
    pp.pensize(2)
    
    # Left eye - using emotion adjustments
    left_blink = blink_factor
    Moveto(206 + offset_x, 212 + offset_y)
    pp.begin_fill()
    lineto(15 + emotion_data.eye_width_adjust, -7)
    curveto_r(4, -1, 26 + emotion_data.eye_width_adjust, -2, 30 + emotion_data.eye_width_adjust, 0)
    smooth_r(10, 3, 12, 7)
    pp.pencolor("#D1D1D1")
    pp.pensize(1)
    smooth_r(2, 27 - 25*left_blink + emotion_data.eye_height_adjust, 
             -1, 30 - 28*left_blink + emotion_data.eye_height_adjust)
    smooth_r(-39 - emotion_data.eye_width_adjust, 5, -44 - emotion_data.eye_width_adjust, 1)
    Smooth(206 + offset_x, 212 + offset_y, 206 + offset_x, 212 + offset_y)
    pp.end_fill()
    
    # Right eye - force closed if winking  
    right_blink = 1.0 if winking else blink_factor
    Moveto(384 + offset_x, 204 + offset_y)
    pp.begin_fill()
    pp.pencolor("black")
    pp.pensize(2)
    curveto_r(-3, -1, -18 - emotion_data.eye_width_adjust, -1, -28 - emotion_data.eye_width_adjust, 1)
    smooth_r(-9, 6, -10, 9)
    pp.pencolor("#D1D1D1")
    pp.pensize(1)
    smooth_r(3, 18 - 16*right_blink + emotion_data.eye_height_adjust, 
             6, 23 - 21*right_blink + emotion_data.eye_height_adjust)
    smooth_r(38 + emotion_data.eye_width_adjust, 6, 40 + emotion_data.eye_width_adjust, 4)
    smooth_r(10, -9, 13, -22)
    pp.pencolor("black")
    pp.pensize(2)
    Lineto(384 + offset_x, 204 + offset_y)
    pp.end_fill()
    
    if blink_factor < 0.8:  # Don't draw iris when mostly blinking
        # Iris
        pp.color("#0C1631", "#0C1631")
        pp.pensize(1)
        
        if winking and right_blink >= 0.8:
            # Only draw left iris when winking
            # Left iris
            Moveto(216 + offset_x + emotion_data.iris_offset_x, 
                   206 + offset_y + emotion_data.iris_offset_y)
            pp.begin_fill()
            curveto_r(-1, 5, 0, 26 - 24*left_blink, 7, 35 - 33*left_blink)
            smooth_r(30, 2, 33, 0)
            smooth_r(5, -31 + 29*left_blink, 2, -34 + 32*left_blink)
            Smooth(219 + offset_x + emotion_data.iris_offset_x, 
                   203 + offset_y + emotion_data.iris_offset_y, 
                   216 + offset_x + emotion_data.iris_offset_x, 
                   206 + offset_y + emotion_data.iris_offset_y)
            pp.end_fill()
        else:
            # Draw both irises normally
            # Left iris
            Moveto(216 + offset_x + emotion_data.iris_offset_x, 
                   206 + offset_y + emotion_data.iris_offset_y)
            pp.begin_fill()
            curveto_r(-1, 5, 0, 26 - 24*left_blink, 7, 35 - 33*left_blink)
            smooth_r(30, 2, 33, 0)
            smooth_r(5, -31 + 29*left_blink, 2, -34 + 32*left_blink)
            Smooth(219 + offset_x + emotion_data.iris_offset_x, 
                   203 + offset_y + emotion_data.iris_offset_y, 
                   216 + offset_x + emotion_data.iris_offset_x, 
                   206 + offset_y + emotion_data.iris_offset_y)
            pp.end_fill()
            
            # Right iris
            Moveto(354 + offset_x + emotion_data.iris_offset_x, 
                   207 + offset_y + emotion_data.iris_offset_y)
            pp.begin_fill()
            curveto_r(-2, 1, 2, 29 - 27*right_blink, 4, 31 - 29*right_blink)
            smooth_r(30, 3, 33, 1)
            smooth_r(6, -24 + 22*right_blink, 4, -27 + 25*right_blink)
            lineto(-11, -8)
            Curveto(382 + offset_x + emotion_data.iris_offset_x, 
                    204 + offset_y + emotion_data.iris_offset_y, 
                    357 + offset_x + emotion_data.iris_offset_x, 
                    206 + offset_y + emotion_data.iris_offset_y, 
                    354 + offset_x + emotion_data.iris_offset_x, 
                    207 + offset_y + emotion_data.iris_offset_y)
            pp.end_fill()
    
    # Eye highlights
    if blink_factor < 0.6 and emotion != "sleepy":
        pp.color("#F5F5F5", "#F5F5F5")
        # Left eye highlight
        if left_blink < 0.6:
            Moveto(253 + offset_x, 211 + offset_y)
            pp.begin_fill()
            curveto_r(-3, 0, -8, 8 - 7*left_blink, 1, 10 - 9*left_blink)
            Smooth(258 + offset_x, 210 + offset_y, 253 + offset_x, 211 + offset_y)
            pp.end_fill()
        
        # Right eye highlight - only if not winking
        if right_blink < 0.6 and not winking:
            Moveto(392 + offset_x, 209 + offset_y)
            pp.begin_fill()
            lineto(4, 3)
            vertical(4 - 3*right_blink)
            lineto(-4, 2)
            Curveto(386 + offset_x, 214 + offset_y, 392 + offset_x, 209 + offset_y, 392 + offset_x, 209 + offset_y)
            pp.end_fill()
    
    # Eye details (only when open)
    if blink_factor < 0.4 and emotion not in ["happy", "sleepy"]:
        pp.pencolor("black")
        pp.pensize(2)
        Moveto(240.5 + offset_x, 207.5 + offset_y)
        line(240.5 + offset_x, 207.5 + offset_y, 227.5 + offset_x, 211.5 + offset_y)
        line(245.5 + offset_x, 209.5 + offset_y, 227.5 + offset_x, 214.5 + offset_y)
        line(247.5 + offset_x, 211.5 + offset_y, 227.5 + offset_x, 217.5 + offset_y)
        line(247.5 + offset_x, 214.5 + offset_y, 229.5 + offset_x, 220.5 + offset_y)
        line(247.5 + offset_x, 218.5 + offset_y, 230.5 + offset_x, 223.5 + offset_y)
        line(246.5 + offset_x, 222.5 + offset_y, 232.5 + offset_x, 226.5 + offset_y)
        line(244.5 + offset_x, 225.5 + offset_y, 234.5 + offset_x, 228.5 + offset_y)
        
        # Right eye details - only if not winking
        if not winking and right_blink < 0.4:
            line(377.5 + offset_x, 207.5 + offset_y, 367.5 + offset_x, 210.5 + offset_y)
            line(384.5 + offset_x, 207.5 + offset_y, 366.5 + offset_x, 212.5 + offset_y)
            line(385.5 + offset_x, 210.5 + offset_y, 366.5 + offset_x, 215.5 + offset_y)
            line(384.5 + offset_x, 213.5 + offset_y, 366.5 + offset_x, 218.5 + offset_y)
            line(384.5 + offset_x, 215.5 + offset_y, 367.5 + offset_x, 220.5 + offset_y)
            line(384.5 + offset_x, 218.5 + offset_y, 368.5 + offset_x, 223.5 + offset_y)
            line(382.5 + offset_x, 223.5 + offset_y, 370.5 + offset_x, 227.5 + offset_y)

def draw_nose_mouth(offset_x=0, offset_y=0, talk_factor=0, emotion="neutral"):
    pp.pencolor("black")
    pp.pensize(1)
    
    # Nose
    Moveto(309 + offset_x, 270 + offset_y)
    curveto_r(0, 0, 4, 7, 1, 9)
    
    # Get emotion data and mouth shape
    emotion_data = get_emotion_data(emotion)
    mouth_shape = MOUTH_SHAPES[emotion_data.mouth_type]
    
    if talk_factor > 0:
        # Talking mouth
        talking_data = mouth_shape.talking
        Moveto(talking_data.start_x + offset_x, talking_data.start_y + offset_y)
        pp.begin_fill()
        
        # Draw upper lip
        for curve_type, *params in talking_data.upper_lip:
            if curve_type == "curveto_r":
                adjusted_params = []
                for i, param in enumerate(params):
                    if i % 2 == 1:  # Y coordinates
                        adjusted_params.append(param + (talk_factor * 4))
                    else:
                        adjusted_params.append(param)
                curveto_r(*adjusted_params)
            elif curve_type == "horizontal":
                horizontal(*params)
        
        # Draw right corner
        if talking_data.corners and len(talking_data.corners) > 0:
            corner_type, *corner_params = talking_data.corners[0]
            if corner_type == "curveto_r":
                adjusted_params = []
                for i, param in enumerate(corner_params):
                    if i % 2 == 1 and i > 2:  # Y coordinates after first pair
                        adjusted_params.append(param + (talk_factor * 4))
                    else:
                        adjusted_params.append(param)
                curveto_r(*adjusted_params)
        
        # Draw lower lip
        for curve_type, *params in talking_data.lower_lip:
            if curve_type == "curveto_r":
                adjusted_params = []
                for i, param in enumerate(params):
                    if i % 2 == 1:  # Y coordinates
                        adjusted_params.append(param + (talk_factor * 6))
                    else:
                        adjusted_params.append(param)
                curveto_r(*adjusted_params)
            elif curve_type == "horizontal":
                horizontal(*params)
        
        # Draw left corner
        if talking_data.corners and len(talking_data.corners) > 1:
            corner_type, *corner_params = talking_data.corners[1]
            if corner_type == "curveto_r":
                adjusted_params = []
                for i, param in enumerate(corner_params):
                    if i % 2 == 1 and i > 2:  # Y coordinates after first pair
                        adjusted_params.append(param + (talk_factor * 4))
                    else:
                        adjusted_params.append(param)
                curveto_r(*adjusted_params)
        
        pp.end_fill()
        
        # Draw inner detail if available and talking enough
        if talking_data.inner_detail and talk_factor > 0.5:
            pp.color(talking_data.inner_detail["color"], talking_data.inner_detail["color"])
            Moveto(298 + offset_x, 310 + offset_y + talk_factor*3)
            pp.begin_fill()
            for curve_type, *params in talking_data.inner_detail["curves"]:
                if curve_type == "curveto_r":
                    curveto_r(*params)
            pp.end_fill()
            pp.color("black", "black")  # Reset color
    else:
        # Closed mouth
        closed_data = mouth_shape.closed
        Moveto(closed_data.start_x + offset_x, closed_data.start_y + offset_y)
        
        if len(closed_data.curves) > 1:  # If multiple curves, use fill
            pp.begin_fill()
        
        for curve_type, *params in closed_data.curves:
            if curve_type == "curveto_r":
                curveto_r(*params)
            elif curve_type == "horizontal":
                horizontal(*params)
        
        if len(closed_data.curves) > 1:
            pp.end_fill()

# Special effects functions
def draw_blush(offset_x=0, offset_y=0, intensity=1.0):
    # Draw blush marks for shy emotion
    pp.color("#FFB7B7", "#FFB7B7")  # Light pink
    # Left cheek
    Moveto(230 + offset_x, 272 + offset_y)
    pp.begin_fill()
    pp.circle(12 * intensity)
    pp.end_fill()
    
    # Right cheek
    Moveto(365 + offset_x, 272 + offset_y)
    pp.begin_fill()
    pp.circle(12 * intensity)
    pp.end_fill()
    
    pp.color("black", "#F3EEEB")  # Reset color

def draw_sweat_drop(offset_x=0, offset_y=0):
    # Draw sweat drop for nervous/anxious emotions
    pp.color("#A0D8FF", "#A0D8FF")  # Light blue
    Moveto(390 + offset_x, 180 + offset_y)
    pp.begin_fill()
    curveto_r(2, -5, 6, -10, 3, -15)
    curveto_r(-4, -2, -8, -1, -10, 5)
    curveto_r(1, 5, 5, 8, 7, 10)
    pp.end_fill()
    pp.color("black", "#F3EEEB")  # Reset color

def draw_vein_mark(offset_x=0, offset_y=0):
    # Draw vein mark for angry emotion
    pp.pencolor("#FF5555")
    pp.pensize(2)
    Moveto(185 + offset_x, 180 + offset_y)
    pp.pendown()
    for i in range(3):
        pp.forward(8)
        pp.right(60)
        pp.forward(5)
        pp.left(120)
    pp.penup()
    pp.pencolor("black")
    pp.pensize(1)

def draw_swirl_mark(offset_x=0, offset_y=0):
    # Draw swirl mark for confused emotion
    pp.pencolor("#5555FF")
    pp.pensize(2)
    Moveto(200 + offset_x, 160 + offset_y)
    pp.pendown()
    for i in range(12):
        pp.circle(5, 30)
        pp.right(30)
        pp.forward(i * 0.5)
    pp.penup()
    pp.pencolor("black")
    pp.pensize(1)

def draw_tears(offset_x=0, offset_y=0):
    """Draw tears for crying emotion"""
    pp.color("#A0D8FF", "#A0D8FF")  # Light blue
    
    # Draw multiple tears
    tear_positions = [
        (235, 240, 16),  # Left eye, x, y, length
        (250, 250, 12),
        (360, 245, 14),  # Right eye
        (375, 255, 10),
    ]
    
    for x, y, length in tear_positions:
        Moveto(x + offset_x, y + offset_y)
        pp.begin_fill()
        # Teardrop shape
        curveto_r(2, 2, 4, length-5, 0, length)
        curveto_r(-4, 0, -6, -5, -4, -length)
        pp.end_fill()
    
    pp.color("black", "#F3EEEB")  # Reset color

def draw_wink(offset_x=0, offset_y=0):
    """Draw wink effect (closed right eye)"""
    # This is handled by the draw_eyes function with special logic
    pass