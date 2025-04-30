import turtle as pp
import math

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
    pp.pensize(2)
    
    if emotion == "surprised":
        # Raised eyebrows
        Moveto(210 + offset_x, 175 + offset_y)
        curveto_r(5, -6, 63, 7, 63, 12)
        Moveto(338 + offset_x, 187 + offset_y)
        curveto_r(0, -5, 18, -8, 18, -8)
    elif emotion == "sad":
        # Lowered outer eyebrows
        Moveto(210 + offset_x, 185 + offset_y)
        curveto_r(5, 2, 63, 11, 63, 17)
        Moveto(338 + offset_x, 198 + offset_y)
        curveto_r(0, 2, 18, -3, 18, -3)
    elif emotion == "angry":
        # Angled down in center
        Moveto(210 + offset_x, 178 + offset_y)
        curveto_r(5, 5, 63, 4, 63, 14)
        Moveto(338 + offset_x, 188 + offset_y)
        curveto_r(0, 2, 18, -1, 18, -1) 
    else:
        # Normal eyebrows
        Moveto(210 + offset_x, 180 + offset_y)
        curveto_r(5, -4, 63, 9, 63, 14)
        Moveto(338 + offset_x, 193 + offset_y)
        curveto_r(0, -3, 18, -6, 18, -6)
    
    pp.pensize(1)

def draw_eyes(offset_x=0, offset_y=0, blink_factor=0, emotion="neutral"):
    # Eyes base
    pp.color("black", "#D1D1D1")
    pp.pensize(2)
    
    # Adjust eye shape based on emotion
    eye_height_adjust = 0
    if emotion == "happy":
        eye_height_adjust = 5
    elif emotion == "surprised":
        eye_height_adjust = -10
    elif emotion == "sad":
        eye_height_adjust = 2
    
    # Left eye
    Moveto(206 + offset_x, 212 + offset_y)
    pp.begin_fill()
    lineto(15, -7)
    curveto_r(4, -1, 26, -2, 30, 0)
    smooth_r(10, 3, 12, 7)
    pp.pencolor("#D1D1D1")
    pp.pensize(1)
    smooth_r(2, 27 - 25*blink_factor + eye_height_adjust, -1, 30 - 28*blink_factor + eye_height_adjust)
    smooth_r(-39, 5, -44, 1)
    Smooth(206 + offset_x, 212 + offset_y, 206 + offset_x, 212 + offset_y)
    pp.end_fill()
    
    # Right eye  
    Moveto(384 + offset_x, 204 + offset_y)
    pp.begin_fill()
    pp.pencolor("black")
    pp.pensize(2)
    curveto_r(-3, -1, -18, -1, -28, 1)
    smooth_r(-9, 6, -10, 9)
    pp.pencolor("#D1D1D1")
    pp.pensize(1)
    smooth_r(3, 18 - 16*blink_factor + eye_height_adjust, 6, 23 - 21*blink_factor + eye_height_adjust)
    smooth_r(38, 6, 40, 4)
    smooth_r(10, -9, 13, -22)
    pp.pencolor("black")
    pp.pensize(2)
    Lineto(384 + offset_x, 204 + offset_y)
    pp.end_fill()
    
    if blink_factor < 0.8:  # Don't draw iris when mostly blinking
        # Iris
        pp.color("#0C1631", "#0C1631")
        pp.pensize(1)
        
        # Left iris - adjust position based on emotion
        iris_offset_x = 0
        iris_offset_y = 0
        if emotion == "surprised":
            iris_offset_y = -5
        elif emotion == "sad":
            iris_offset_y = 3
        elif emotion == "happy":
            iris_offset_y = 2
        
        # Left iris
        Moveto(216 + offset_x + iris_offset_x, 206 + offset_y + iris_offset_y)
        pp.begin_fill()
        curveto_r(-1, 5, 0, 26 - 24*blink_factor, 7, 35 - 33*blink_factor)
        smooth_r(30, 2, 33, 0)
        smooth_r(5, -31 + 29*blink_factor, 2, -34 + 32*blink_factor)
        Smooth(219 + offset_x + iris_offset_x, 203 + offset_y + iris_offset_y, 
               216 + offset_x + iris_offset_x, 206 + offset_y + iris_offset_y)
        pp.end_fill()
        
        # Right iris
        Moveto(354 + offset_x + iris_offset_x, 207 + offset_y + iris_offset_y)
        pp.begin_fill()
        curveto_r(-2, 1, 2, 29 - 27*blink_factor, 4, 31 - 29*blink_factor)
        smooth_r(30, 3, 33, 1)
        smooth_r(6, -24 + 22*blink_factor, 4, -27 + 25*blink_factor)
        lineto(-11, -8)
        Curveto(382 + offset_x + iris_offset_x, 204 + offset_y + iris_offset_y, 
                357 + offset_x + iris_offset_x, 206 + offset_y + iris_offset_y, 
                354 + offset_x + iris_offset_x, 207 + offset_y + iris_offset_y)
        pp.end_fill()
    
    # Eye highlights
    if blink_factor < 0.6:
        pp.color("#F5F5F5", "#F5F5F5")
        Moveto(253 + offset_x, 211 + offset_y)
        pp.begin_fill()
        curveto_r(-3, 0, -8, 8 - 7*blink_factor, 1, 10 - 9*blink_factor)
        Smooth(258 + offset_x, 210 + offset_y, 253 + offset_x, 211 + offset_y)
        pp.end_fill()
        
        Moveto(392 + offset_x, 209 + offset_y)
        pp.begin_fill()
        lineto(4, 3)
        vertical(4 - 3*blink_factor)
        lineto(-4, 2)
        Curveto(386 + offset_x, 214 + offset_y, 392 + offset_x, 209 + offset_y, 392 + offset_x, 209 + offset_y)
        pp.end_fill()
    
    # Eye details (only when open)
    if blink_factor < 0.4 and emotion != "happy":
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
    
    # Improved mouth animation
    if talk_factor > 0:
        # Advanced talking mouth shapes
        if emotion == "happy":
            # Happy talking - wide smile variation
            Moveto(291 + offset_x, 307 + offset_y)
            pp.begin_fill()
            
            # Upper lip with variable curve
            curveto_r(10, 5 + talk_factor*3, 25, 8 + talk_factor*4, 38, 5 + talk_factor*3)
            
            # Right corner
            curveto_r(2, 0, 3, -1 - talk_factor*2, 3, -3 - talk_factor*3)
            
            # Lower lip
            curveto_r(0, 2 + talk_factor*4, -15, 8 + talk_factor*6, -38, 8 + talk_factor*4)
            
            # Left corner
            curveto_r(-3, -2 - talk_factor*2, -3, -4 - talk_factor*3, 0, -7 - talk_factor*3)
            
            pp.end_fill()
            
        elif emotion == "sad":
            # Sad talking - downturned mouth
            Moveto(293 + offset_x, 310 + offset_y)
            pp.begin_fill()
            
            # Upper lip
            curveto_r(10, -2 + talk_factor*2, 25, -4 + talk_factor*3, 35, -2 + talk_factor*2)
            
            # Right corner
            curveto_r(2, 1, 2, 3 + talk_factor*2, 1, 4 + talk_factor*3)
            
            # Lower lip
            curveto_r(-5, 3 + talk_factor*4, -20, 6 + talk_factor*5, -35, 4 + talk_factor*3)
            
            # Left corner
            curveto_r(-2, -1, -2, -3 - talk_factor*2, 0, -5 - talk_factor*3)
            
            pp.end_fill()
            
        elif emotion == "surprised":
            # Surprised talking - O shape that changes
            center_x = 308 + offset_x
            center_y = 308 + offset_y
            
            # Dynamic O shape
            Moveto(center_x - 12, center_y)
            pp.begin_fill()
            
            # Top curve
            curveto_r(6, -6 - talk_factor*4, 18, -6 - talk_factor*4, 24, 0)
            
            # Right side
            curveto_r(4, 4 + talk_factor*2, 4, 8 + talk_factor*4, 0, 12 + talk_factor*6)
            
            # Bottom curve
            curveto_r(-6, 4 + talk_factor*2, -18, 4 + talk_factor*2, -24, 0)
            
            # Left side
            curveto_r(-4, -4 - talk_factor*2, -4, -8 - talk_factor*4, 0, -12 - talk_factor*6)
            
            pp.end_fill()
            
        else:
            # Natural talking mouth with better shape variation
            Moveto(292 + offset_x, 307 + offset_y)
            pp.begin_fill()
            
            # Different mouth shapes based on talk_factor
            if talk_factor < 0.3:
                # Small opening
                curveto_r(8, 1, 20, 2, 32, 1)
                curveto_r(2, 1, 2, 2, 1, 3)
                curveto_r(-10, 3, -22, 3, -32, 0)
                curveto_r(-2, -1, -2, -2, -1, -3)
                
            elif talk_factor < 0.6:
                # Medium opening
                curveto_r(10, 2, 22, 4, 34, 2)
                curveto_r(2, 2, 2, 4, 0, 6)
                curveto_r(-12, 5, -24, 5, -34, 0)
                curveto_r(-2, -2, -2, -4, 0, -6)
                
            else:
                # Wide opening
                curveto_r(12, 3, 24, 6, 36, 3)
                curveto_r(2, 3, 2, 6, -1, 9)
                curveto_r(-14, 6, -26, 6, -36, 0)
                curveto_r(-2, -3, -2, -6, 1, -9)
            
            pp.end_fill()
            
            # Add inner mouth detail for larger openings
            if talk_factor > 0.5:
                pp.color("#FF6B6B", "#FF6B6B")  # Tongue color
                Moveto(298 + offset_x, 310 + offset_y + talk_factor*3)
                pp.begin_fill()
                curveto_r(5, 1, 12, 2, 18, 1)
                curveto_r(3, 2, 2, 4, -1, 5)
                curveto_r(-8, 1, -16, 0, -18, -2)
                curveto_r(-2, -2, -1, -4, 1, -5)
                pp.end_fill()
                pp.color("black", "black")  # Reset color
    else:
        # Closed mouth expressions (unchanged)
        if emotion == "happy":
            # Happy smile
            Moveto(293 + offset_x, 307.5 + offset_y)
            pp.begin_fill()
            curveto_r(10, 6, 22, 9, 34, 4)
            curveto_r(2, -1, 1, -3, 0, -3)
            horizontal(-34)
            pp.end_fill()
        elif emotion == "sad":
            # Sad frown
            Moveto(293 + offset_x, 311.5 + offset_y)
            pp.begin_fill()
            curveto_r(10, -4, 22, -6, 34, -3)
            curveto_r(2, 1, 1, 2, 0, 2)
            horizontal(-34)
            pp.end_fill()
        elif emotion == "surprised":
            # Surprised small O
            pp.begin_fill()
            Moveto(302 + offset_x, 307.5 + offset_y)
            curveto_r(5, -3, 10, -3, 15, 0)
            curveto_r(3, 3, 3, 6, 0, 9)
            curveto_r(-5, 3, -10, 3, -15, 0)
            curveto_r(-3, -3, -3, -6, 0, -9)
            pp.end_fill()
        else:
            # Normal mouth
            Moveto(293 + offset_x, 307.5 + offset_y)
            curveto_r(10, 0, 22, 1, 34, 0)