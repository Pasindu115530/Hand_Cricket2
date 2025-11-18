import cv2
import mediapipe as mp
import time
import math
import tkinter as tk
import random
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np

# Global game state variables
game_state = "WELCOME"
player_choice = None
player_score = 0
computer_score = 0
target_score = 0
current_innings = 1
last_player_gesture = None
last_computer_gesture = None
game_active = True
balls_bowled = 0
camera_active = False

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

def calculate_distance(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def detect_gesture(landmarks):
    """Detect hand gesture and return number (1-6) or None"""
    # Finger State Checks
    index_is_up = landmarks[8].y < landmarks[6].y and landmarks[8].y < landmarks[5].y
    middle_is_up = landmarks[12].y < landmarks[10].y and landmarks[12].y < landmarks[9].y
    ring_is_up = landmarks[16].y < landmarks[14].y and landmarks[16].y < landmarks[13].y
    pinky_is_up = landmarks[20].y < landmarks[18].y and landmarks[20].y < landmarks[17].y

    index_is_down = landmarks[8].y > landmarks[6].y
    middle_is_down = landmarks[12].y > landmarks[10].y
    ring_is_down = landmarks[16].y > landmarks[14].y
    pinky_is_down = landmarks[20].y > landmarks[18].y

    thumb_is_dis = landmarks[17].x - landmarks[5].x
    thumb_is_dis_with_17 = landmarks[17].x - landmarks[4].x
    thumb_is_in = abs(thumb_is_dis) > abs(thumb_is_dis_with_17)
    thumb_is_out = abs(thumb_is_dis) < abs(thumb_is_dis_with_17)

    # Gesture Recognition Logic
    result_1_1 = index_is_up and middle_is_down and ring_is_down and pinky_is_down and thumb_is_in
    result_1_2 = index_is_down and middle_is_up and ring_is_down and pinky_is_down and thumb_is_in
    result_1_3 = index_is_down and middle_is_down and ring_is_up and pinky_is_down and thumb_is_in
    result_1_4 = index_is_down and middle_is_down and ring_is_down and pinky_is_up and thumb_is_in

    result_2_1 = index_is_up and middle_is_up and ring_is_down and pinky_is_down and thumb_is_in
    result_2_2 = index_is_up and middle_is_down and ring_is_up and pinky_is_down and thumb_is_in
    result_2_3 = index_is_up and middle_is_down and ring_is_down and pinky_is_up and thumb_is_in
    result_2_4 = index_is_down and middle_is_up and ring_is_up and pinky_is_down and thumb_is_in
    result_2_5 = index_is_down and middle_is_up and ring_is_down and pinky_is_up and thumb_is_in
    result_2_6 = index_is_down and middle_is_down and ring_is_up and pinky_is_up and thumb_is_in
    result_2_7 = index_is_up and middle_is_down and ring_is_down and pinky_is_down and thumb_is_out
    result_2_8 = index_is_down and middle_is_up and ring_is_down and pinky_is_down and thumb_is_out
    result_2_9 = index_is_down and middle_is_down and ring_is_up and pinky_is_down and thumb_is_out
    result_2_10 = index_is_down and middle_is_down and ring_is_down and pinky_is_up and thumb_is_out

    result_3_1 = index_is_up and middle_is_up and ring_is_up and pinky_is_down and thumb_is_in
    result_3_2 = index_is_up and middle_is_up and ring_is_down and pinky_is_up and thumb_is_in
    result_3_3 = index_is_up and middle_is_down and ring_is_up and pinky_is_up and thumb_is_in
    result_3_4 = index_is_down and middle_is_up and ring_is_up and pinky_is_up and thumb_is_in
    result_3_5 = index_is_up and middle_is_up and ring_is_down and pinky_is_down and thumb_is_out
    result_3_6 = index_is_up and middle_is_down and ring_is_up and pinky_is_down and thumb_is_out
    result_3_7 = index_is_up and middle_is_down and ring_is_down and pinky_is_up and thumb_is_out
    result_3_8 = index_is_down and middle_is_up and ring_is_up and pinky_is_down and thumb_is_out
    result_3_9 = index_is_down and middle_is_up and ring_is_down and pinky_is_up and thumb_is_out
    result_3_10 = index_is_down and middle_is_down and ring_is_up and pinky_is_up and thumb_is_out

    result_4_1 = index_is_up and middle_is_up and ring_is_up and pinky_is_up and thumb_is_in
    result_4_2 = index_is_down and middle_is_up and ring_is_up and pinky_is_up and thumb_is_out
    result_4_3 = index_is_up and middle_is_down and ring_is_up and pinky_is_up and thumb_is_out
    result_4_4 = index_is_up and middle_is_up and ring_is_down and pinky_is_up and thumb_is_out
    result_4_5 = index_is_up and middle_is_up and ring_is_up and pinky_is_down and thumb_is_out
    result_5_1 = index_is_up and middle_is_up and ring_is_up and pinky_is_up and thumb_is_out

    result_6_1 = (index_is_down and middle_is_down and ring_is_down and pinky_is_down and thumb_is_out)
    # result_7 = index_is_down and middle_is_down and ring_is_down and pinky_is_down and thumb_is_in

    if result_1_1 or result_1_2 or result_1_3 or result_1_4:
        return 1
    elif result_2_1 or result_2_2 or result_2_3 or result_2_4 or result_2_5 or result_2_6 or result_2_7 or result_2_8 or result_2_9 or result_2_10:
        return 2
    elif result_3_1 or result_3_2 or result_3_3 or result_3_4 or result_3_5 or result_3_6 or result_3_7 or result_3_8 or result_3_9 or result_3_10:
        return 3
    elif result_4_1 or result_4_2 or result_4_3 or result_4_4 or result_4_5:
        return 4
    elif result_5_1:
        return 5
    elif result_6_1:
        return 6
    # elif result_7:
    #     return 7
    
    return None

def update_game_logic(player_gesture, img):
    global game_state, player_score, computer_score, target_score, current_innings
    global last_player_gesture, last_computer_gesture, game_active, balls_bowled, camera_active
    
    if player_gesture is None or player_gesture == last_player_gesture or player_gesture == 7:
        return
    
    last_player_gesture = player_gesture
    computer_gesture = random.randint(1, 6)
    last_computer_gesture = computer_gesture
    balls_bowled += 1
    
    # Display both numbers with beautiful styling
    cv2.putText(img, f"Player: {player_gesture}", (50, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
    cv2.putText(img, f"Computer: {computer_gesture}", (50, 90), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 100, 255), 3)
    
    # Check if OUT (same number)
    if player_gesture == computer_gesture:
        cv2.putText(img, "OUT!", (img.shape[1]//2 - 80, img.shape[0]//2), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        
        if game_state == "FIRST_INNINGS":
            if player_choice == "BAT":
                target_score = player_score + 1
                cv2.putText(img, f"Target: {target_score}", (img.shape[1]//2 - 100, img.shape[0]//2 + 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)
            else:
                target_score = computer_score + 1
                cv2.putText(img, f"Target: {target_score}", (img.shape[1]//2 - 100, img.shape[0]//2 + 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)
            
            game_state = "SECOND_INNINGS"
            current_innings = 2
            # Show transition message for 3 seconds
            cv2.imshow('Hand Cricket', img)
            cv2.waitKey(3000)
            
        else:  # SECOND_INNINGS - GAME OVER
            game_active = False
            camera_active = False  # Stop camera loop
            return "GAME_OVER"
            
    else:
        # Add runs to appropriate score
        if game_state == "FIRST_INNINGS":
            if player_choice == "BAT":
                print(player_gesture)
                player_score += player_gesture
            else:
                print(computer_gesture)
                computer_score += computer_gesture
        else:  # SECOND_INNINGS
            if player_choice == "BAT":
                print(computer_gesture)
                computer_score += computer_gesture
                if computer_score >= target_score:
                    game_active = False
                    camera_active = False  # Stop camera loop
                    return "GAME_OVER"
            else:
                print(player_gesture)   
                player_score += player_gesture
                if player_score >= target_score:
                    game_active = False
                    camera_active = False  # Stop camera loop
                    return "GAME_OVER"
    
    return "CONTINUE"

def draw_scoreboard(img):
    """Enhanced scoreboard with beautiful design"""
    # Add semi-transparent background for scoreboard
    overlay = img.copy()
    cv2.rectangle(overlay, (0, 0), (400, 200), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)
    
    # Game state with color coding
    state_color = (255, 255, 0) if game_state == "FIRST_INNINGS" else (0, 255, 255)
    cv2.putText(img, f"Innings: {current_innings}", (20, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, state_color, 2)
    
    if game_state == "FIRST_INNINGS":
        if player_choice == "BAT":
            cv2.putText(img, f"Player Score: {player_score}", (20, 70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img, "You are Batting", (20, 110), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 100), 2)
        else:
            cv2.putText(img, f"Computer Score: {computer_score}", (20, 70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 100), 2)
            cv2.putText(img, "You are Bowling", (20, 110), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 100, 100), 2)
    elif game_state == "SECOND_INNINGS":
        cv2.putText(img, f"Target: {target_score}", (20, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(img, f"Player: {player_score} | Computer: {computer_score}", 
                    (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)

def reset_game():
    global game_state, player_score, computer_score, target_score, current_innings
    global last_player_gesture, last_computer_gesture, game_active, balls_bowled, camera_active
    
    game_state = "WELCOME"
    player_score = 0
    computer_score = 0
    target_score = 0
    current_innings = 1
    last_player_gesture = None
    last_computer_gesture = None
    game_active = True
    balls_bowled = 0
    camera_active = False

def run_camera_loop():
    global game_active, camera_active
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open camera!")
        return
    
    camera_active = True
    pTime = time.time()
    
    while camera_active:
        success, img = cap.read()
        if not success:
            print("Error: Could not read frame.")
            break
        
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        
        current_gesture = None
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Enhanced hand drawing with better colors
                mp_draw.draw_landmarks(
                    img, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_draw.DrawingSpec(color=(0, 255, 0), thickness=3, circle_radius=4),
                    mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=3)
                )
                current_gesture = detect_gesture(hand_landmarks.landmark)
        
        if game_state in ["FIRST_INNINGS", "SECOND_INNINGS"] and game_active:
             if current_gesture :
                result = update_game_logic(current_gesture, img)
                if result == "GAME_OVER":
                    # Show final result on camera for 2 seconds
                    determine_winner_display(img)
                    cv2.imshow('Hand Cricket', img)
                    cv2.waitKey(2000)
                    break
        
        draw_scoreboard(img)
        
        if current_gesture:
            gesture_text = f"Gesture: {current_gesture}"
            cv2.putText(img, gesture_text, (img.shape[1] - 250, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        
        # Enhanced FPS display
        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (img.shape[1] - 150, 80), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        
        # Beautiful instructions
        if game_state == "WELCOME":
            cv2.putText(img, "Choose BAT or BOWL in the GUI", (img.shape[1]//2 - 180, img.shape[0] - 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        elif game_state in ["FIRST_INNINGS", "SECOND_INNINGS"]:
            cv2.putText(img, "Show hand gesture (1-6)", (img.shape[1]//2 - 150, img.shape[0] - 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(img, "Press 'Q' to quit", (img.shape[1]//2 - 100, img.shape[0] - 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
        cv2.imshow('Hand Cricket', img)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            camera_active = False
            break
        
        # Auto-close when game reaches result state
        if not game_active and game_state == "SECOND_INNINGS":
            cv2.waitKey(2000)
            break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    # Show result screen in GUI after camera closes
    if not game_active:
        show_result_screen()

def determine_winner_display(img):
    """Display winner on the camera screen before closing"""
    if player_choice == "BAT":  
        if computer_score >= target_score:
            winner = "Computer"
        else:
            winner = "Player"
    else:  
        if player_score >= target_score:
            winner = "Player"
        else:
            winner = "Computer"
    
    if winner == "Player":
        color = (0, 255, 0)  # Green
    else:
        color = (0, 0, 255)  # Red
    
    # Add semi-transparent background for result
    overlay = img.copy()
    cv2.rectangle(overlay, (0, img.shape[0]//2 - 100), (img.shape[1], img.shape[0]//2 + 100), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)
    
    cv2.putText(img, "GAME OVER!", (img.shape[1]//2 - 150, img.shape[0]//2 - 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
    cv2.putText(img, f"Winner: {winner}!", (img.shape[1]//2 - 120, img.shape[0]//2 + 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)
    cv2.putText(img, f"Final: {player_score}-{computer_score}", (img.shape[1]//2 - 100, img.shape[0]//2 + 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

# Beautiful GUI Functions
def create_styled_button(parent, text, command, bg_color, hover_color, width=20):
    """Create a beautiful styled button with hover effects"""
    button = tk.Button(
        parent,
        text=text,
        font=("Arial", 14, "bold"),
        bg=bg_color,
        fg="white",
        padx=20,
        pady=12,
        width=width,
        command=command,
        relief="flat",
        bd=0,
        cursor="hand2"
    )
    
    def on_enter(e):
        button.config(bg=hover_color)
    
    def on_leave(e):
        button.config(bg=bg_color)
    
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    
    return button

def start_batting():
    global game_state, player_choice
    player_choice = "BAT"
    game_state = "FIRST_INNINGS"
    hide_welcome_screen()
    run_camera_loop()

def start_bowling():
    global game_state, player_choice
    player_choice = "BOWL"
    game_state = "FIRST_INNINGS"
    hide_welcome_screen()
    run_camera_loop()

def hide_welcome_screen():
    for widget in window.winfo_children():
        widget.destroy()

def show_welcome_screen():
    reset_game()
    create_beautiful_welcome_screen()

def create_beautiful_welcome_screen():
    # Main container
    main_frame = tk.Frame(window, bg='#1a5276')
    main_frame.pack(fill='both', expand=True)
    
    # Header
    header_frame = tk.Frame(main_frame, bg='#1a5276', height=150)
    header_frame.pack(fill='x', pady=(30, 20))
    header_frame.pack_propagate(False)
    
    title_label = tk.Label(
        header_frame,
        text="🏏 HAND CRICKET 🏏",
        font=("Arial", 32, "bold"),
        bg='#1a5276',
        fg='white',
        pady=20
    )
    title_label.pack(expand=True)
    
    sub_label = tk.Label(
        header_frame,
        text="Experience Cricket Like Never Before!",
        font=("Arial", 16),
        bg='#1a5276',
        fg='#f39c12',
        pady=10
    )
    sub_label.pack()
    
    # Content frame
    content_frame = tk.Frame(main_frame, bg='#2c3e50')
    content_frame.pack(expand=True, fill='both', padx=40, pady=30)
    
    # Instructions with beautiful styling
    instructions_frame = tk.Frame(content_frame, bg='#2c3e50')
    instructions_frame.pack(pady=20)
    
    instructions = [
        "🎯 Show hand gestures (1-6 fingers) to score runs",
        "⚡ Same number as computer = OUT!",
        "🏆 Two innings: Set target and chase it",
        "🎮 First to beat the target wins the match!"
    ]
    
    for i, instruction in enumerate(instructions):
        label = tk.Label(
            instructions_frame,
            text=instruction,
            font=("Arial", 13, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1',
            justify='left',
            pady=8
        )
        label.pack(anchor='w')
    
    # Start button
    button_frame = tk.Frame(content_frame, bg='#2c3e50')
    button_frame.pack(pady=40)
    
    start_btn = create_styled_button(
        button_frame,
        "🚀 START GAME",
        show_bat_bowl,
        '#e74c3c',
        '#c0392b',
        width=25
    )
    start_btn.pack(pady=15)
    
    # Footer
    footer_label = tk.Label(
        main_frame,
        text="Made with HandCricket using OpenCV & MediaPipe By Menda",
        font=("Arial", 10, "italic"),
        bg='#1a5276',
        fg='#bdc3c7',
        pady=15
    )
    footer_label.pack(side='bottom')

def show_bat_bowl():
    for widget in window.winfo_children():
        widget.destroy()
    
    # Beautiful role selection screen
    main_frame = tk.Frame(window, bg='#34495e')
    main_frame.pack(fill='both', expand=True)
    
    # Header
    header_frame = tk.Frame(main_frame, bg='#34495e', height=120)
    header_frame.pack(fill='x', pady=(40, 20))
    header_frame.pack_propagate(False)
    
    title_label = tk.Label(
        header_frame,
        text="Choose Your Role",
        font=("Arial", 28, "bold"),
        bg='#34495e',
        fg='white',
        pady=10
    )
    title_label.pack()
    
    sub_label = tk.Label(
        header_frame,
        text="Will you bat first or bowl first?",
        font=("Arial", 16),
        bg='#34495e',
        fg='#f39c12',
        pady=5
    )
    sub_label.pack()
    
    # Buttons container
    button_frame = tk.Frame(main_frame, bg='#34495e')
    button_frame.pack(expand=True, pady=50)
    
    # Batting button
    bat_btn = create_styled_button(
        button_frame,
        "🦇 BAT FIRST",
        start_batting,
        '#27ae60',
        '#219652',
        width=25
    )
    bat_btn.pack(pady=20)
    
    # Bowling button
    bowl_btn = create_styled_button(
        button_frame,
        "🎯 BOWL FIRST",
        start_bowling,
        '#e67e22',
        '#d35400',
        width=25
    )
    bowl_btn.pack(pady=20)
    
    # Back button
    back_btn = create_styled_button(
        button_frame,
        "⬅️ GO BACK",
        show_welcome_screen,
        '#95a5a6',
        '#7f8c8d',
        width=25
    )
    back_btn.pack(pady=20)

def show_result_screen():

    cv2.destroyAllWindows()
    for widget in window.winfo_children():
        widget.destroy()
    
    # Determine winner
    if player_choice == "BAT":  
        if computer_score < target_score:
            winner = "Player"
        else:
            winner = "Computer"
    else:  
        if player_score < target_score:
            winner = "Computer"
        else:
            winner = "Player"
    
    # Beautiful result screen
    main_frame = tk.Frame(window, bg='#2c3e50')
    main_frame.pack(fill='both', expand=True)
    
    # Result color and emoji
    result_color = '#27ae60' if winner == "Player" else '#e74c3c'
    winner_emoji = "🎉" if winner == "Player" else "😔"
    player_emoji = "👤" 
    computer_emoji = "💻"
    
    # Header
    header_frame = tk.Frame(main_frame, bg='#2c3e50')
    header_frame.pack(fill='x', pady=(40, 20))
    
    result_label = tk.Label(
        header_frame,
        text=f"{winner_emoji} MATCH COMPLETED {winner_emoji}",
        font=("Arial", 24, "bold"),
        bg='#2c3e50',
        fg=result_color,
        pady=10
    )
    result_label.pack()
    
    # Score display frame
    score_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=3)
    score_frame.pack(pady=20, padx=60, fill='x')
    
    # Target
    target_label = tk.Label(
        score_frame,
        text=f"🎯 TARGET: {target_score} runs",
        font=("Arial", 18, "bold"),
        bg='#34495e',
        fg='#f39c12',
        pady=15
    )
    target_label.pack()
    
    # Scores
    scores_label = tk.Label(
        score_frame,
        text=f"{player_emoji} Player: {player_score}   |   {computer_emoji} Computer: {computer_score}",
        font=("Arial", 16, "bold"),
        bg='#34495e',
        fg='#ecf0f1',
        pady=15
    )
    scores_label.pack()
    
    # Winner announcement
    winner_frame = tk.Frame(main_frame, bg='#2c3e50')
    winner_frame.pack(pady=30)
    
    winner_label = tk.Label(
        winner_frame,
        text=f"🏆 CHAMPION: {winner.upper()}! 🏆",
        font=("Arial", 22, "bold"),
        bg='#2c3e50',
        fg=result_color,
        pady=10
    )
    winner_label.pack()
    
    # Buttons frame
    button_frame = tk.Frame(main_frame, bg='#2c3e50')
    button_frame.pack(pady=40)
    
    def restart_game():
        """Properly restart the game by destroying result screen and showing welcome"""
        # Destroy all widgets in the current window
        for widget in window.winfo_children():
            widget.destroy()
        # Reset game state
        
        # Show welcome screen
        show_welcome_screen()
    
    # Play Again button
    play_again_btn = create_styled_button(
        button_frame,
        "🔄 PLAY AGAIN",
        restart_game,
        '#27ae60',
        '#219652',
        width=20
    )
    play_again_btn.pack(pady=15)
    
    # Exit button
    exit_btn = create_styled_button(
        button_frame,
        "🚪 EXIT GAME",
        window.quit,
        '#e74c3c',
        '#c0392b',
        width=20
    )
    exit_btn.pack(pady=15)

# Create main window
window = tk.Tk()
window.title("Hand Cricket - Ultimate Gesture Game")
window.geometry("700x750")
window.configure(bg='#1a5276')
window.resizable(False, False)

# Center the window on screen
window.eval('tk::PlaceWindow . center')

# Start with welcome screen
show_welcome_screen()

# Start the application
window.mainloop()