import tkinter as tk
from tkinter import scrolledtext
import random

# Global state variable for nested logic
chat_state = "main"

def get_bot_response(user_input):
    global chat_state
    
    # 1. UNIVERSAL COMMANDS
    if any(word in user_input for word in ['exit', 'quit', 'bye', 'shutdown', 'log off']):
        return "Executing graceful shutdown. Don't forget to push your commits to GitHub. Ciao!"
    elif 'help' in user_input or 'status' in user_input:
        return "I am Dalhi AI. I can discuss software logic, Arduino hardware, or routing protocols. Try asking me about 'BGP'."

    # 2. NESTED LOGIC
    if chat_state == "study":
        chat_state = "main"  
        if 'software' in user_input or 'intelligent' in user_input:
            return "Ça marche. Loading up software and intelligent systems models. Let's hope your logic is bug-free today."
        elif 'networking' in user_input or 'routing' in user_input:
            return "Networking it is. Which protocol? I can help you review RIP, OSPF, IS-IS, EIGRP, or BGP."
        elif 'hardware' in user_input or 'arduino' in user_input:
            return "Ah, hardware. Please don't fry the transistors this time. Let me know if you need wiring schematics."
        else:
            return "That wasn't one of the options. Focus! We are going back to the main menu."

    # 3. MAIN LOGIC
    elif any(word in user_input for word in ['study', 'learn', 'review', 'prepare']):
        chat_state = "study"
        return "Studying? Alright, genius. Are we optimizing software, configuring routing protocols, or wiring up some hardware today?"
    elif any(word in user_input for word in ['hello', 'hi', 'hey', 'salam', 'bonjour']):
        return "Salam! Systems active and ready. What are we building or debugging today?"
    elif 'arduino' in user_input or 'uno' in user_input:
        return "For the Arduino Uno, ensure your PWM pins are correctly mapped. Do you need help controlling a DC motor or an SG90 servomotor?"
    elif 'bgp' in user_input:
        return "BGP (Border Gateway Protocol) is the backbone of the internet. Watch out for eBGP vs iBGP peering rules."
    elif 'ospf' in user_input:
        return "OSPF uses link-state logic. Always double-check your wildcard masks and area assignments."
    else:
        return "Error 404: Logic not found. I might need more context for that."

# --- Animation & UI Logic ---

robot_dx = 2 # Speed and direction of the robot

def animate_robot():
    """Moves the robot across the canvas and creates a blinking LED effect."""
    global robot_dx
    
    # Get dynamic width of the canvas
    c_width = robot_canvas.winfo_width()
    if c_width < 10: 
        c_width = 600 # Fallback width before window renders
        
    coords = robot_canvas.coords("body")
    if coords:
        x1, y1, x2, y2 = coords
        # Reverse direction if it hits the edges
        if x2 >= c_width or x1 <= 0:
            robot_dx = -robot_dx
            
        # Move all parts of the robot
        robot_canvas.move("robot_grp", robot_dx, 0)
        
        # Randomly blink the antenna LED
        if random.random() > 0.85:
            colors = ["#ff0055", "#00ff41", "#121212"]
            robot_canvas.itemconfig("led", fill=random.choice(colors))
            
    # Loop the animation every 30 milliseconds (~30 FPS)
    root.after(30, animate_robot)

def send_message(event=None):
    user_input = user_entry.get().strip().lower()
    if not user_input:
        return
    
    # 1. Print User Message
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "You: " + user_input + "\n", "user")
    user_entry.delete(0, tk.END) 
    chat_window.yview(tk.END)
    
    # 2. Make Robot "Think" (Eyes turn green)
    robot_canvas.itemconfig("eye", fill="#00ff41")
    
    # 3. Simulate processing delay
    root.after(600, lambda: process_response(user_input))

def process_response(user_input):
    """Generates the response and returns the robot to its default state."""
    response = get_bot_response(user_input)
    
    chat_window.insert(tk.END, "Dalhi AI: " + response + "\n\n", "bot")
    chat_window.config(state=tk.DISABLED) 
    chat_window.yview(tk.END) 
    
    # Eyes return to resting blue
    robot_canvas.itemconfig("eye", fill="#00bfff")
    
    # Auto-shutdown logic
    if any(word in user_input for word in ['exit', 'quit', 'bye', 'shutdown']):
        root.after(1500, root.destroy) 

# --- GUI Setup ---
root = tk.Tk()
root.title("Dalhi AI Interface")
root.geometry("600x750")
root.configure(bg="#121212") 

# --- Dynamic Robot Canvas ---
robot_canvas = tk.Canvas(root, height=70, bg="#121212", highlightthickness=0)
robot_canvas.pack(fill=tk.X, pady=(10, 0))

# Drawing the 2D Robot (Grouped by "robot_grp" tag)
# Antenna
robot_canvas.create_line(40, 25, 40, 5, fill="#00ff41", width=2, tags=("robot_grp", "antenna"))
robot_canvas.create_oval(35, 0, 45, 10, fill="#ff0055", outline="", tags=("robot_grp", "led"))
# Head/Body
robot_canvas.create_rectangle(20, 25, 60, 65, fill="#2d2d2d", outline="#00ff41", width=2, tags=("robot_grp", "body"))
# Eyes
robot_canvas.create_rectangle(28, 35, 36, 43, fill="#00bfff", outline="", tags=("robot_grp", "eye"))
robot_canvas.create_rectangle(44, 35, 52, 43, fill="#00bfff", outline="", tags=("robot_grp", "eye"))
# Mouth
robot_canvas.create_line(30, 55, 50, 55, fill="#ffffff", width=2, tags=("robot_grp", "mouth"))

# Chat Display Area
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 12), bg="#1e1e1e", fg="#e0e0e0", bd=0, padx=10, pady=10)
chat_window.tag_config("user", foreground="#00bfff") 
chat_window.tag_config("bot", foreground="#00ff41")  
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

chat_window.insert(tk.END, "Dalhi AI: Salam! Systems booted and ready. Type 'help' to see what I know.\n\n", "bot")
chat_window.config(state=tk.DISABLED)

# Text Entry Box
user_entry = tk.Entry(root, font=("Consolas", 14), bg="#2d2d2d", fg="#ffffff", insertbackground="white", bd=1)
user_entry.pack(padx=10, pady=(0, 10), fill=tk.X, ipady=5)
user_entry.bind("<Return>", send_message)

# Start the animation loop before running the window
animate_robot()
root.mainloop()
