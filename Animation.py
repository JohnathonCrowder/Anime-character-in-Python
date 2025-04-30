import turtle  # Import turtle module directly for exception handling
import turtle as pp  # Also keep the pp alias
import time
import math
import random
from character_drawing import *
from emotions import get_emotion_data, get_available_emotions

# Constants
ANIMATION_SPEED = 0  # 0 is fastest for animations

# Global control variable
running = False

# States for animation
talking = False
emotion = "neutral"  # Will dynamically update based on available emotions

# Modified drawing function
def draw_character(offset_x=0, offset_y=0, breath_offset=0, blink_factor=0, talk_factor=0):
    # Base offset affects the whole character
    total_offset_y = offset_y + breath_offset
    
    # Draw body parts from back to front
    draw_coat(total_offset_y)
    draw_jacket_inside(total_offset_y)
    draw_clothes(total_offset_y)
    draw_neck(total_offset_y)
    draw_collar(total_offset_y)
    draw_tie(total_offset_y)
    
    # Draw face parts
    draw_face(offset_x, total_offset_y)
    draw_hair(offset_x, total_offset_y)
    draw_eyebrows(offset_x, total_offset_y, emotion)
    draw_eyes(offset_x, total_offset_y, blink_factor, emotion)
    draw_nose_mouth(offset_x, total_offset_y, talk_factor, emotion)
    
    # Draw special effects based on emotion
    emotion_data = get_emotion_data(emotion)
    for effect in emotion_data.special_effects:
        if effect == "blush":
            blush_intensity = 0.7 + 0.3 * math.sin(time.time() * 1.5)
            draw_blush(offset_x, total_offset_y, blush_intensity)
        elif effect == "sweat_drop" and random.random() < 0.05:
            draw_sweat_drop(offset_x, total_offset_y)
        elif effect == "vein_mark" and random.random() < 0.03:
            draw_vein_mark(offset_x, total_offset_y)
        elif effect == "swirl_mark" and random.random() < 0.07:
            draw_swirl_mark(offset_x, total_offset_y)

# Emotion control functions
def set_emotion(new_emotion):
    global emotion
    try:
        # Validate the emotion exists
        if new_emotion in get_available_emotions():
            emotion = new_emotion
            print(f"Emotion changed to: {emotion}")
        else:
            print(f"Warning: Unknown emotion '{new_emotion}'")
    except Exception as e:
        print(f"Error changing emotion: {e}")

# Keyboard control functions
def toggle_talking():
    global talking
    talking = not talking
    print(f"Talking: {talking}")

def set_neutral():
    set_emotion("neutral")

def set_happy():
    set_emotion("happy")

def set_sad():
    set_emotion("sad")

def set_surprised():
    set_emotion("surprised")

def set_angry():
    set_emotion("angry")

def set_excited():
    set_emotion("excited")

def set_shy():
    set_emotion("shy")

def set_sleepy():
    set_emotion("sleepy")

def exit_program():
    global running
    running = False
    try:
        pp.bye()
    except:
        pass

# Setup close handler
def on_close():
    global running
    running = False
    try:
        pp.bye()
    except:
        pass

# Create safe emotion key handlers
def setup_emotion_keys():
    """Set up keyboard controls for all available emotions"""
    emotions = get_available_emotions()
    
    # Create individual functions for each emotion instead of using lambda
    def make_emotion_handler(emotion_name):
        def handler():
            set_emotion(emotion_name)
        return handler
    
    # Bind each emotion to a number key
    for i, emotion_name in enumerate(emotions):
        if i < 10:  # Limit to 0-9 keys
            if i == 9:
                key = "0"
            else:
                key = str(i + 1)
            pp.onkey(make_emotion_handler(emotion_name), key)

# Main animation loop
def animate():
    global talking, running
    running = True
    
    # Animation parameters
    blink_interval = random.randint(50, 150)  # Frames between blinks
    breath_speed = 0.03
    head_move_speed = 0.02
    talk_counter = 0
    
    try:
        pp.tracer(0)  # Turn off animation during drawing
        pp.setup(WIDTH, HEIGHT, 0, 0)
        pp.speed(ANIMATION_SPEED)
        pp.hideturtle()
        
        # Set up keyboard controls
        pp.listen()
        pp.onkey(toggle_talking, "t")     # Press 't' to make character talk
        pp.onkey(set_neutral, "n")        # Press 'n' for neutral
        pp.onkey(set_happy, "h")          # Press 'h' for happy
        pp.onkey(set_sad, "s")            # Press 's' for sad
        pp.onkey(set_surprised, "o")      # Press 'o' for surprised
        pp.onkey(set_angry, "a")          # Press 'a' for angry
        pp.onkey(set_excited, "e")        # Press 'e' for excited
        pp.onkey(set_shy, "y")            # Press 'y' for shy
        pp.onkey(set_sleepy, "z")         # Press 'z' for sleepy
        pp.onkey(exit_program, "Escape")  # Press Escape to quit
        
        # Add number keys for emotions - safely
        setup_emotion_keys()
        
        frame = 0
        while running:
            try:
                pp.clear()
                
                # Calculate animation factors
                blink_factor = 0
                if frame % blink_interval < 10:  # Blink lasts 10 frames
                    blink_factor = math.sin(frame % 10 * math.pi / 10)
                
                # Adjust blink interval periodically
                if frame % blink_interval == 0:
                    blink_interval = random.randint(50, 150)
                
                breath_offset = 2 * math.sin(frame * breath_speed)
                head_offset_x = 2 * math.sin(frame * head_move_speed)
                head_offset_y = 1 * math.sin(frame * head_move_speed * 0.7)
                
                # Random talking animation
                if not talking and frame % 200 == 0:
                    talking = random.random() < 0.3  # 30% chance to start talking
                    talk_counter = 60 if talking else 0
                
                talk_factor = 0
                if talking:
                    # More natural talking motion with varying speeds
                    if talk_counter <= 0:
                        talk_counter = random.randint(20, 40)  # Random talk duration
                    
                    if talk_counter % 10 < 3:
                        # Quick opening
                        talk_factor = 0.8 * math.sin(talk_counter * 0.5)
                    elif talk_counter % 10 < 7:
                        # Hold open
                        talk_factor = 0.7 + 0.1 * math.sin(talk_counter * 0.2)
                    else:
                        # Quick closing
                        talk_factor = 0.3 * math.sin(talk_counter * 0.4)
                    
                    # Add small random variations for natural movement
                    talk_factor += random.uniform(-0.05, 0.05)
                    talk_factor = max(0, min(1, talk_factor))  # Keep between 0 and 1
                    
                    talk_counter -= 1
                    if talk_counter <= 0 and random.random() < 0.7:  # 70% chance to stop talking
                        talking = False
                
                # Draw full character with animation
                draw_character(head_offset_x, head_offset_y, breath_offset, blink_factor, talk_factor)
                
                # Display controls
                pp.penup()
                pp.goto(-WIDTH/2 + 10, -HEIGHT/2 + 35)
                pp.pencolor("black")
                pp.write("Controls: t=talk, n=neutral, h=happy, s=sad, o=surprised", font=("Arial", 10, "normal"))
                pp.goto(-WIDTH/2 + 10, -HEIGHT/2 + 20)
                pp.write("          a=angry, e=excited, y=shy, z=sleepy, ESC=exit", font=("Arial", 10, "normal"))
                
                # Display available emotion numbers
                emotions_list = get_available_emotions()
                number_controls = []
                for i, emotion_name in enumerate(emotions_list[:9]):
                    number_controls.append(f"{i+1}={emotion_name}")
                if len(emotions_list) > 9:
                    number_controls.append(f"0={emotions_list[9]}")
                
                pp.goto(-WIDTH/2 + 10, -HEIGHT/2 + 5)
                pp.write(f"Number keys: {', '.join(number_controls[:5])}", font=("Arial", 8, "normal"))
                if len(number_controls) > 5:
                    pp.goto(-WIDTH/2 + 10, -HEIGHT/2 - 5)
                    pp.write(f"            {', '.join(number_controls[5:])}", font=("Arial", 8, "normal"))
                
                pp.goto(-WIDTH/2 + 10, -HEIGHT/2 - 20)
                pp.write(f"Current emotion: {emotion}", font=("Arial", 10, "bold"))
                
                if talking:
                    pp.goto(WIDTH/2 - 100, -HEIGHT/2 + 5)
                    pp.write("TALKING", font=("Arial", 10, "bold"))
                
                pp.update()
                frame += 1
                time.sleep(0.033)  # ~30fps
                
            except turtle.Terminator:
                print("Window closed")
                running = False
                break
            except Exception as e:
                print(f"Error in animation loop: {e}")
                import traceback
                traceback.print_exc()  # Print the full error traceback
                running = False
                break
                
    except turtle.Terminator:
        print("Window closed during setup")
    except Exception as e:
        print(f"Setup error: {e}")
        import traceback
        traceback.print_exc()

# Main execution
if __name__ == "__main__":
    try:
        # Print available emotions
        print("Available emotions:", ", ".join(get_available_emotions()))
        print("Starting animation...")
        
        # Prevent automatic closing
        screen = pp.Screen()
        screen._root.protocol("WM_DELETE_WINDOW", on_close)
        
        # Start animation
        animate()
        
        # Keep the program running until window is closed
        try:
            pp.mainloop()
        except turtle.Terminator:
            print("Program terminated")
        except Exception as e:
            print(f"Mainloop error: {e}")
            import traceback
            traceback.print_exc()
    except Exception as e:
        print(f"Startup error: {e}")
        import traceback
        traceback.print_exc()