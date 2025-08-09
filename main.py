import tkinter as tk
import random
from PIL import Image, ImageTk, ImageSequence

# Window & sizes
WIDTH, HEIGHT = 800, 600
GAME_W, GAME_H = 500, 350

# Game settings
CLICK_LIMIT = 20
click_count = 0
button_x = random.randint(50, GAME_W - 50)
button_y = random.randint(50, GAME_H - 50)

# Emoji list (variety)
EMOJIS = ["😊", "😂", "😜", "🤩", "😎", "🥳", "🤡", "🙃", "😱", "😴", "🤔", "😇"]

# Create main window
root = tk.Tk()
root.title("🎯 Clickine Thedi – Invisible Button")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)
root.configure(bg="#1E2A38")

# Background canvas (emoji layer) - placed first so it's at the back
bg_canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#1E2A38", highlightthickness=0)
bg_canvas.pack(fill="both", expand=True)

# Foreground main frame (placed above bg_canvas)
main_frame = tk.Frame(root, bg="#1E2A38")
# center the main frame roughly near top
main_frame.place(relx=0.5, rely=0.05, anchor="n")

# Header
header = tk.Label(
    main_frame,
    text="🔍 Find the Invisible Button!",
    font=("Helvetica", 24, "bold"),
    fg="#F9DC5C",
    bg="#1E2A38",
    pady=6
)
header.pack()

# Status message
status = tk.StringVar(value="Click anywhere to begin your search...")
status_label = tk.Label(
    main_frame,
    textvariable=status,
    wraplength=600,
    font=("Helvetica", 16),
    fg="#FFFFFF",
    bg="#1E2A38",
    pady=8
)
status_label.pack()

# Game canvas inside main_frame
game_canvas = tk.Canvas(main_frame, width=GAME_W, height=GAME_H, bg="#3A506B", bd=0, highlightthickness=0)
game_canvas.pack(pady=12)

# Ensure main_frame is above the background canvas
main_frame.lift()

# ========== Emoji particle system ==========
particles = []  # each is dict {id, speed, size}

def spawn_emoji():
    """Create a new emoji text on bg_canvas at random x, with random speed/size."""
    x = random.randint(10, WIDTH - 10)
    size = random.randint(14, 30)  # font size
    emoji = random.choice(EMOJIS)
    # choose a font that supports emoji (Windows: Segoe UI Emoji)
    font = ("Segoe UI Emoji", size)
    item_id = bg_canvas.create_text(x, -20, text=emoji, font=font, fill="#F9DC5C")
    speed = random.uniform(1.5, 5.0)
    particles.append({"id": item_id, "speed": speed})
    # spawn next emoji at a random interval
    root.after(random.randint(120, 420), spawn_emoji)

def animate_emojis():
    """Move all emoji particles down; remove if below screen."""
    remove_list = []
    for p in particles:
        bg_canvas.move(p["id"], 0, p["speed"])
        coords = bg_canvas.coords(p["id"])
        if coords:
            _, y = coords
            if y > HEIGHT + 30:
                remove_list.append(p)
    # remove off-screen particles
    for p in remove_list:
        try:
            bg_canvas.delete(p["id"])
        except Exception:
            pass
        if p in particles:
            particles.remove(p)
    # schedule next frame
    root.after(30, animate_emojis)

# Start emoji spawn & animation
spawn_emoji()
animate_emojis()

# ========== Load GIF frames for ending ==========
gif_frames = []
try:
    gif = Image.open("suraj.gif")
    for frame in ImageSequence.Iterator(gif):
        # Resize to game canvas size to fit nicely
        frame = frame.convert("RGBA").resize((GAME_W, GAME_H), Image.LANCZOS)
        gif_frames.append(ImageTk.PhotoImage(frame))
except FileNotFoundError:
    gif_frames = []
    print("Warning: 'suraj.gif' not found. Ending GIF will be skipped.")

gif_item = None  # canvas image id for the gif
def show_fullscreen_gif_on_game_canvas():
    """Animate the loaded gif frames on the game canvas (if available)."""
    global gif_item
    if not gif_frames:
        return
    # create image at top-left of game_canvas
    gif_item = game_canvas.create_image(0, 0, anchor="nw", image=gif_frames[0])
    def animate(i=0):
        if gif_item is None:
            return
        game_canvas.itemconfig(gif_item, image=gif_frames[i])
        root.after(100, lambda: animate((i + 1) % len(gif_frames)))
    animate(0)

# ========== Game click logic ==========
def on_game_click(event):
    global click_count
    click_count += 1
    dx = abs(event.x - button_x)
    dy = abs(event.y - button_y)

    if dx < 20 and dy < 20:
        status.set("🔥 You're very close! But not quite there...")
    elif dx < 50 and dy < 50:
        status.set("✨ You are almost near... Keep going!")
    else:
        status.set(f"🖱️ Attempt {click_count}: Still searching...")

    if click_count >= CLICK_LIMIT:
        status_label.config(font=("Helvetica", 18, "bold italic"), fg="#FF6B6B")
        status.set("🤡 Oops! You have just wasted the precious time of your life 🫣... ഇനിയെങ്കിലും ഒന്ന് എണീറ്റു പോടേ..!! 🫵")
        game_canvas.unbind("<Button-1>")
        show_fullscreen_gif_on_game_canvas()

# Bind clicks on game canvas (use widget-relative coordinates)
game_canvas.bind("<Button-1>", on_game_click)

# ========== Run the application ==========
root.mainloop()
