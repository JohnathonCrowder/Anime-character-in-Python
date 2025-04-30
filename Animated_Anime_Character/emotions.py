import math

class EmotionData:
    def __init__(self, name, eyebrow_type, eye_type, mouth_type, 
                 eye_height_adjust=0, eye_width_adjust=0, iris_offset_x=0, 
                 iris_offset_y=0, special_effects=None, blink_adjust=1.0):
        self.name = name
        self.eyebrow_type = eyebrow_type
        self.eye_type = eye_type
        self.mouth_type = mouth_type
        self.eye_height_adjust = eye_height_adjust
        self.eye_width_adjust = eye_width_adjust
        self.iris_offset_x = iris_offset_x
        self.iris_offset_y = iris_offset_y
        self.special_effects = special_effects or []
        self.blink_adjust = blink_adjust

class EyebrowShape:
    def __init__(self, left_start_y, left_curve, right_start_y, right_curve):
        self.left_start_y = left_start_y
        self.left_curve = left_curve
        self.right_start_y = right_start_y
        self.right_curve = right_curve

class MouthShape:
    def __init__(self, closed_shape, talking_shape):
        self.closed = ClosedMouthData(**closed_shape)
        self.talking = TalkingMouthData(**talking_shape)

class ClosedMouthData:
    def __init__(self, start_x, start_y, curves):
        self.start_x = start_x
        self.start_y = start_y
        self.curves = curves

class TalkingMouthData:
    def __init__(self, start_x, start_y, upper_lip, lower_lip, corners, inner_detail=None):
        self.start_x = start_x
        self.start_y = start_y
        self.upper_lip = upper_lip
        self.lower_lip = lower_lip
        self.corners = corners
        self.inner_detail = inner_detail

# Eyebrow definitions
EYEBROW_SHAPES = {
    "normal": EyebrowShape(
        left_start_y=180, 
        left_curve=[(5, -4, 63, 9, 63, 14)],
        right_start_y=193,
        right_curve=[(0, -3, 18, -6, 18, -6)]
    ),
    "surprised": EyebrowShape(
        left_start_y=175, 
        left_curve=[(5, -6, 63, 7, 63, 12)],
        right_start_y=187,
        right_curve=[(0, -5, 18, -8, 18, -8)]
    ),
    "sad": EyebrowShape(
        left_start_y=185, 
        left_curve=[(5, 2, 63, 11, 63, 17)],
        right_start_y=198,
        right_curve=[(0, 2, 18, -3, 18, -3)]
    ),
    "angry": EyebrowShape(
        left_start_y=175, 
        left_curve=[(5, 10, 63, 2, 63, 15)],
        right_start_y=183,
        right_curve=[(0, 8, 18, -3, 18, -3)]
    ),
    "excited": EyebrowShape(
        left_start_y=172, 
        left_curve=[(5, -5, 63, 5, 63, 10)],
        right_start_y=185,
        right_curve=[(0, -4, 18, -7, 18, -7)]
    ),
    "shy": EyebrowShape(
        left_start_y=178, 
        left_curve=[(5, -1, 63, 6, 63, 14)],
        right_start_y=190,
        right_curve=[(0, -2, 18, -4, 18, -4)]
    ),
    "sleepy": EyebrowShape(
        left_start_y=183, 
        left_curve=[(5, 0, 63, 3, 63, 3)],
        right_start_y=195,
        right_curve=[(0, 0, 18, -2, 18, -2)]
    ),
    "shocked": EyebrowShape(
        left_start_y=170,
        left_curve=[(5, -8, 63, 5, 63, 10)],
        right_start_y=182,
        right_curve=[(0, -7, 18, -10, 18, -10)]
    ),
    "smug": EyebrowShape(
        left_start_y=182,
        left_curve=[(5, -2, 63, 12, 63, 16)],
        right_start_y=188,
        right_curve=[(0, 0, 18, -2, 18, -2)]
    ),
    "crying": EyebrowShape(
        left_start_y=188,
        left_curve=[(5, 3, 63, 13, 63, 20)],
        right_start_y=200,
        right_curve=[(0, 4, 18, -1, 18, -1)]
    ),
    "confused": EyebrowShape(
        left_start_y=175,
        left_curve=[(5, -5, 63, 7, 63, 12)],
        right_start_y=195,
        right_curve=[(0, 2, 18, -4, 18, -4)]
    ),
    "thinking": EyebrowShape(
        left_start_y=180,
        left_curve=[(5, -3, 63, 8, 63, 13)],
        right_start_y=185,
        right_curve=[(0, -8, 18, -5, 18, -5)]
    ),
    "bored": EyebrowShape(
        left_start_y=185,
        left_curve=[(5, 0, 63, 0, 63, 0)],
        right_start_y=195,
        right_curve=[(0, 0, 18, 0, 18, 0)]
    ),
    "winking": EyebrowShape(
        left_start_y=180,
        left_curve=[(5, -4, 63, 9, 63, 14)],
        right_start_y=175,
        right_curve=[(0, -6, 18, -8, 18, -8)]
    ),
    "laughing": EyebrowShape(
        left_start_y=180,
        left_curve=[(5, 0, 63, 10, 63, 15)],
        right_start_y=193,
        right_curve=[(0, 0, 18, -7, 18, -7)]
    ),
}

# Mouth definitions
MOUTH_SHAPES = {
    "normal": MouthShape(
        closed_shape={
            "start_x": 293,
            "start_y": 307.5,
            "curves": [
                ("curveto_r", 10, 0, 22, 1, 34, 0)
            ]
        },
        talking_shape={
            "start_x": 292,
            "start_y": 307,
            "upper_lip": [
                ("curveto_r", 10, 2, 22, 4, 34, 2)
            ],
            "lower_lip": [
                ("curveto_r", -12, 5, -24, 5, -34, 0)
            ],
            "corners": [
                ("curveto_r", 2, 2, 2, 4, 0, 6),  # right corner
                ("curveto_r", -2, -2, -2, -4, 0, -6)  # left corner
            ],
            "inner_detail": {
                "color": "#FF6B6B",
                "curves": [
                    ("curveto_r", 5, 1, 12, 2, 18, 1),
                    ("curveto_r", 3, 2, 2, 4, -1, 5),
                    ("curveto_r", -8, 1, -16, 0, -18, -2),
                    ("curveto_r", -2, -2, -1, -4, 1, -5)
                ]
            }
        }
    ),
    "happy": MouthShape(
        closed_shape={
            "start_x": 293,
            "start_y": 307.5,
            "curves": [
                ("curveto_r", 10, 6, 22, 9, 34, 4),
                ("curveto_r", 2, -1, 1, -3, 0, -3),
                ("horizontal", -34)
            ]
        },
        talking_shape={
            "start_x": 291,
            "start_y": 307,
            "upper_lip": [
                ("curveto_r", 10, 5, 25, 8, 38, 5)
            ],
            "lower_lip": [
                ("curveto_r", 0, 2, -15, 8, -38, 8)
            ],
            "corners": [
                ("curveto_r", 2, 0, 3, -1, 3, -3),
                ("curveto_r", -3, -2, -3, -4, 0, -7)
            ]
        }
    ),
    "sad": MouthShape(
        closed_shape={
            "start_x": 293,
            "start_y": 311.5,
            "curves": [
                ("curveto_r", 10, -4, 22, -6, 34, -3),
                ("curveto_r", 2, 1, 1, 2, 0, 2),
                ("horizontal", -34)
            ]
        },
        talking_shape={
            "start_x": 293,
            "start_y": 310,
            "upper_lip": [
                ("curveto_r", 10, -2, 25, -4, 35, -2)
            ],
            "lower_lip": [
                ("curveto_r", -5, 3, -20, 6, -35, 4)
            ],
            "corners": [
                ("curveto_r", 2, 1, 2, 3, 1, 4),
                ("curveto_r", -2, -1, -2, -3, 0, -5)
            ]
        }
    ),
    "surprised": MouthShape(
        closed_shape={
            "start_x": 302,
            "start_y": 307.5,
            "curves": [
                ("curveto_r", 5, -3, 10, -3, 15, 0),
                ("curveto_r", 3, 3, 3, 6, 0, 9),
                ("curveto_r", -5, 3, -10, 3, -15, 0),
                ("curveto_r", -3, -3, -3, -6, 0, -9)
            ]
        },
        talking_shape={
            "start_x": 296,
            "start_y": 308,
            "upper_lip": [
                ("curveto_r", 6, -6, 18, -6, 24, 0)
            ],
            "lower_lip": [
                ("curveto_r", -6, 4, -18, 4, -24, 0)
            ],
            "corners": [
                ("curveto_r", 4, 4, 4, 8, 0, 12),
                ("curveto_r", -4, -4, -4, -8, 0, -12)
            ]
        }
    ),
    "angry": MouthShape(
        closed_shape={
            "start_x": 293,
            "start_y": 310,
            "curves": [
                ("curveto_r", 10, -2, 22, -1, 34, -2),
                ("curveto_r", 2, 0, 2, 1, 1, 2),
                ("curveto_r", -10, 2, -22, 3, -34, 1),
                ("curveto_r", -2, -1, -2, -2, -1, -2)
            ]
        },
        talking_shape={
            "start_x": 293,
            "start_y": 310,
            "upper_lip": [
                ("curveto_r", 10, -1, 25, 0, 35, -1)
            ],
            "lower_lip": [
                ("curveto_r", -5, 3, -25, 3, -35, 1)
            ],
            "corners": [
                ("curveto_r", 2, 0, 2, 1, 1, 2),
                ("curveto_r", -2, 0, -2, -1, 0, -2)
            ]
        }
    ),
    "excited": MouthShape(
        closed_shape={
            "start_x": 290,
            "start_y": 306,
            "curves": [
                ("curveto_r", 12, 8, 26, 12, 40, 6),
                ("curveto_r", 2, -2, 1, -4, 0, -4),
                ("horizontal", -40)
            ]
        },
        talking_shape={
            "start_x": 291,
            "start_y": 307,
            "upper_lip": [
                ("curveto_r", 10, 5, 25, 8, 38, 5)
            ],
            "lower_lip": [
                ("curveto_r", 0, 2, -15, 8, -38, 8)
            ],
            "corners": [
                ("curveto_r", 2, 0, 3, -1, 3, -3),
                ("curveto_r", -3, -2, -3, -4, 0, -7)
            ]
        }
    ),
    "shy": MouthShape(
        closed_shape={
            "start_x": 295,
            "start_y": 307,
            "curves": [
                ("curveto_r", 8, 3, 18, 4, 28, 2),
                ("curveto_r", 1, 0, 1, -1, 0, -1),
                ("horizontal", -28)
            ]
        },
        talking_shape={
            "start_x": 295,
            "start_y": 307,
            "upper_lip": [
                ("curveto_r", 8, 1, 18, 2, 28, 1)
            ],
            "lower_lip": [
                ("curveto_r", -5, 2, -15, 2, -28, 1)
            ],
            "corners": [
                ("curveto_r", 2, 0, 2, 1, 1, 2),
                ("curveto_r", -2, 0, -2, -1, 0, -2)
            ]
        }
    ),
    "sleepy": MouthShape(
        closed_shape={
            "start_x": 295,
            "start_y": 309,
            "curves": [
                ("curveto_r", 10, 0, 22, 1, 30, 0)
            ]
        },
        talking_shape={
            "start_x": 293,
            "start_y": 309,
            "upper_lip": [
                ("curveto_r", 10, 0, 25, 1, 35, 0)
            ],
            "lower_lip": [
                ("curveto_r", -5, 2, -25, 2, -35, 0)
            ],
            "corners": [
                ("curveto_r", 1, 0, 1, 1, 0, 2),
                ("curveto_r", -1, 0, -1, -1, 0, -2)
            ]
        }
    ),
    "shocked": MouthShape(
        closed_shape={
            "start_x": 300,
            "start_y": 305,
            "curves": [
                ("curveto_r", 6, -5, 12, -5, 18, 0),
                ("curveto_r", 4, 5, 4, 10, 0, 15),
                ("curveto_r", -6, 5, -12, 5, -18, 0),
                ("curveto_r", -4, -5, -4, -10, 0, -15)
            ]
        },
        talking_shape={
            "start_x": 295,
            "start_y": 305,
            "upper_lip": [
                ("curveto_r", 6, -6, 22, -6, 28, 0)
            ],
            "lower_lip": [
                ("curveto_r", -8, 10, -20, 10, -28, 0)
            ],
            "corners": [
                ("curveto_r", 4, 5, 4, 10, 0, 15),
                ("curveto_r", -4, -5, -4, -10, 0, -15)
            ]
        }
    ),
    "smug": MouthShape(
        closed_shape={
            "start_x": 293,
            "start_y": 307,
            "curves": [
                ("curveto_r", 8, 2, 16, 5, 34, 2),
                ("curveto_r", 2, -1, 0, -2, 0, -2),
                ("horizontal", -34)
            ]
        },
        talking_shape={
            "start_x": 293,
            "start_y": 307,
            "upper_lip": [
                ("curveto_r", 8, 2, 16, 5, 34, 2)
            ],
            "lower_lip": [
                ("curveto_r", -10, 3, -24, 3, -34, 0)
            ],
            "corners": [
                ("curveto_r", 2, 0, 2, -1, 0, -2),
                ("curveto_r", -2, 0, -2, 1, 0, 2)
            ]
        }
    ),
    "crying": MouthShape(
        closed_shape={
            "start_x": 293,
            "start_y": 315,
            "curves": [
                ("curveto_r", 10, -6, 22, -8, 34, -5),
                ("curveto_r", 2, 1, 1, 2, 0, 2),
                ("horizontal", -34)
            ]
        },
        talking_shape={
            "start_x": 293,
            "start_y": 315,
            "upper_lip": [
                ("curveto_r", 10, -4, 22, -6, 34, -3)
            ],
            "lower_lip": [
                ("curveto_r", -10, -4, -22, -6, -34, -3)
            ],
            "corners": [
                ("curveto_r", 2, 1, 1, 2, 0, 2),
                ("curveto_r", -2, 1, -1, 2, 0, 2)
            ]
        }
    ),
    "confused": MouthShape(
        closed_shape={
            "start_x": 293,
            "start_y": 309,
            "curves": [
                ("curveto_r", 5, -1, 15, 0, 25, -2),
                ("curveto_r", 5, 1, 5, 2, 5, 3),
                ("horizontal", -30)
            ]
        },
        talking_shape={
            "start_x": 293,
            "start_y": 309,
            "upper_lip": [
                ("curveto_r", 5, -1, 15, 0, 25, -2)
            ],
            "lower_lip": [
                ("curveto_r", -5, 3, -15, 4, -25, 2)
            ],
            "corners": [
                ("curveto_r", 3, 0, 5, 1, 5, 3),
                ("curveto_r", -3, 0, -5, -1, -5, -3)
            ]
        }
    ),
    "thinking": MouthShape(
        closed_shape={
            "start_x": 303,
            "start_y": 309,
            "curves": [
                ("curveto_r", 0, 0, 10, 0, 15, 0),
                ("curveto_r", 0, 0, 0, 0, 0, 0),
                ("horizontal", -15)
            ]
        },
        talking_shape={
            "start_x": 303,
            "start_y": 309,
            "upper_lip": [
                ("curveto_r", 0, 0, 10, 0, 15, 0)
            ],
            "lower_lip": [
                ("curveto_r", -5, 2, -10, 2, -15, 0)
            ],
            "corners": [
                ("curveto_r", 0, 0, 0, 0, 0, 0),
                ("curveto_r", 0, 0, 0, 0, 0, 0)
            ]
        }
    ),
    "bored": MouthShape(
        closed_shape={
            "start_x": 295,
            "start_y": 310,
            "curves": [
                ("curveto_r", 10, 0, 20, 0, 30, 0)
            ]
        },
        talking_shape={
            "start_x": 295,
            "start_y": 310,
            "upper_lip": [
                ("curveto_r", 10, 0, 20, 0, 30, 0)
            ],
            "lower_lip": [
                ("curveto_r", -10, 2, -20, 2, -30, 0)
            ],
            "corners": [
                ("curveto_r", 0, 0, 0, 1, 0, 1),
                ("curveto_r", 0, 0, 0, -1, 0, -1)
            ]
        }
    ),
    "winking": MouthShape(
        closed_shape={
            "start_x": 293,
            "start_y": 307.5,
            "curves": [
                ("curveto_r", 6, 4, 16, 7, 28, 3),
                ("curveto_r", 2, -1, 1, -2, 0, -2),
                ("horizontal", -28)
            ]
        },
        talking_shape={
            "start_x": 293,
            "start_y": 307.5,
            "upper_lip": [
                ("curveto_r", 6, 4, 16, 7, 28, 3)
            ],
            "lower_lip": [
                ("curveto_r", -8, 3, -20, 3, -28, 0)
            ],
            "corners": [
                ("curveto_r", 2, -1, 1, -2, 0, -2),
                ("curveto_r", -2, 1, -1, 2, 0, 2)
            ]
        }
    ),
    "laughing": MouthShape(
        closed_shape={
            "start_x": 290,
            "start_y": 306,
            "curves": [
                ("curveto_r", 12, 10, 28, 15, 40, 10),
                ("curveto_r", 0, -5, -5, -10, -10, -12),
                ("curveto_r", -10, 0, -20, 0, -30, 0)
            ]
        },
        talking_shape={
            "start_x": 290,
            "start_y": 306,
            "upper_lip": [
                ("curveto_r", 12, 5, 28, 10, 40, 5)
            ],
            "lower_lip": [
                ("curveto_r", -12, 10, -28, 10, -40, 0)
            ],
            "corners": [
                ("curveto_r", 0, 0, 0, 0, 0, 0),
                ("curveto_r", 0, 0, 0, 0, 0, 0)
            ],
            "inner_detail": {
                "color": "#FF6B6B",
                "curves": [
                    ("curveto_r", 10, 1, 20, 2, 30, 1),
                    ("curveto_r", 3, 2, 2, 4, -1, 5),
                    ("curveto_r", -8, 1, -22, 0, -28, -2),
                    ("curveto_r", -2, -2, -1, -4, 1, -5)
                ]
            }
        }
    ),
}

# Emotion definitions
EMOTIONS = {
    "neutral": EmotionData(
        name="neutral",
        eyebrow_type="normal",
        eye_type="normal",
        mouth_type="normal"
    ),
    "happy": EmotionData(
        name="happy",
        eyebrow_type="normal",
        eye_type="happy",
        mouth_type="happy",
        eye_height_adjust=5,
        iris_offset_y=2
    ),
    "sad": EmotionData(
        name="sad",
        eyebrow_type="sad",
        eye_type="sad",
        mouth_type="sad",
        eye_height_adjust=2,
        iris_offset_y=3
    ),
    "surprised": EmotionData(
        name="surprised",
        eyebrow_type="surprised",
        eye_type="surprised",
        mouth_type="surprised",
        eye_height_adjust=-10,
        iris_offset_y=-5
    ),
    "angry": EmotionData(
        name="angry",
        eyebrow_type="angry",
        eye_type="angry",
        mouth_type="angry",
        eye_height_adjust=8,
        eye_width_adjust=-5,
        iris_offset_x=-5,
        special_effects=["vein_mark"]
    ),
    "excited": EmotionData(
        name="excited",
        eyebrow_type="excited",
        eye_type="excited",
        mouth_type="excited",
        eye_height_adjust=-15,
        eye_width_adjust=10,
        iris_offset_y=-5,
        special_effects=["sweat_drop"]
    ),
    "shy": EmotionData(
        name="shy",
        eyebrow_type="shy",
        eye_type="shy",
        mouth_type="shy",
        eye_height_adjust=3,
        eye_width_adjust=-3,
        iris_offset_x=5,
        iris_offset_y=8,
        special_effects=["blush"]
    ),
    "sleepy": EmotionData(
        name="sleepy",
        eyebrow_type="sleepy",
        eye_type="sleepy",
        mouth_type="sleepy",
        eye_height_adjust=15,
        eye_width_adjust=-8,
        iris_offset_y=5,
        blink_adjust=0.5
    ),
    "shocked": EmotionData(
        name="shocked",
        eyebrow_type="shocked",
        eye_type="surprised",
        mouth_type="shocked",
        eye_height_adjust=-15,
        eye_width_adjust=12,
        iris_offset_y=-6,
        special_effects=["sweat_drop"]
    ),
    "smug": EmotionData(
        name="smug",
        eyebrow_type="smug",
        eye_type="happy",
        mouth_type="smug",
        eye_height_adjust=7,
        eye_width_adjust=-4,
        iris_offset_x=3,
        iris_offset_y=2
    ),
    "crying": EmotionData(
        name="crying",
        eyebrow_type="crying",
        eye_type="sad",
        mouth_type="crying",
        eye_height_adjust=4,
        iris_offset_y=5,
        special_effects=["tears"]
    ),
    "confused": EmotionData(
        name="confused",
        eyebrow_type="confused",
        eye_type="normal",
        mouth_type="confused",
        iris_offset_x=3,
        iris_offset_y=-3,
        special_effects=["swirl_mark"]
    ),
    "thinking": EmotionData(
        name="thinking",
        eyebrow_type="thinking",
        eye_type="normal",
        mouth_type="thinking",
        eye_height_adjust=0,
        iris_offset_x=0,
        iris_offset_y=-8,
    ),
    "bored": EmotionData(
        name="bored",
        eyebrow_type="bored",
        eye_type="sleepy",
        mouth_type="bored",
        eye_height_adjust=10,
        eye_width_adjust=-5,
        iris_offset_y=3,
        blink_adjust=0.3
    ),
    "winking": EmotionData(
        name="winking",
        eyebrow_type="winking",
        eye_type="happy",
        mouth_type="winking",
        eye_height_adjust=2,
        iris_offset_y=1,
        special_effects=["wink"]
    ),
    "laughing": EmotionData(
        name="laughing",
        eyebrow_type="laughing",
        eye_type="happy",
        mouth_type="laughing",
        eye_height_adjust=15,  # Nearly closed from laughing
        eye_width_adjust=5,
        blink_adjust=0.7
    ),
}

def get_emotion_data(emotion_name):
    """Get the emotion data for a given emotion name"""
    return EMOTIONS.get(emotion_name, EMOTIONS["neutral"])

def add_emotion(name, eyebrow_type, eye_type, mouth_type, **kwargs):
    """Add a new emotion to the system"""
    EMOTIONS[name] = EmotionData(
        name=name,
        eyebrow_type=eyebrow_type,
        eye_type=eye_type,
        mouth_type=mouth_type,
        **kwargs
    )

def get_available_emotions():
    """Return a list of all available emotion names"""
    return list(EMOTIONS.keys())