import tkinter as tk
from tkinter import filedialog
from colors import colors
from PIL import Image
import math

# Base colors with hex
base_colors = {
    "Cinnabar": "#e54545",
    "Burnt_Sienna": "#e57a45",
    "Anzac": "#e5b045",
    "Confetti": "#e5e545",
    "Conifer": "#b0e545",
    "Atlantis": "#7ae545",
    "Pastel_Green": "#45e545",
    "Shamrock": "#45e57a",
    "Turquoise": "#45e5b0",
    "Turquoise_Blue": "#45e5e5",
    "Picton_Blue": "#45b0e5",
    "Havelock_Blue": "#457ae5",
    "Royal_Blue": "#4545e5",
    "Purple_Royal_Blue": "#7a45e5",
    "Purple_Heart": "#b045e5",
    "Medium_Purple": "#e545e5",
    "Cerise": "#e545b0",
    "Mandy": "#e5457a",

    "Tonys_Pink": "#e58a89",
    "Tumbleweed": "#e5a889",
    "Putty": "#e5c789",
    "Yellow_Yellow_Green": "#e5e589",
    "Yellow_Green": "#c7e589",
    "Granny_Smith_Apple": "#a8e589",
    "Light_Pastel_Green": "#8ae589",
    "Algae_Green": "#8ae5a8",
    "Light_Riptide": "#8ae5c7",
    "Riptide": "#8ae5e5",
    "Cornflower":"#8ac7e5",
    "Portage": "#8aa8e5",
    "Dull_Lavender": "#8a8ae5",
    "Cold_Purple": "#a88ae5",
    "Lavender": "#c78ae5",
    "Orchid": "#e58ae5",
    "Shocking": "#e58ac7",
    "Carissma": "#e58aa8"
}

# Grayscale colors from white to black
grayscale_colors = {
    "White": "#FFFFFF",
    "Mercury": "#E5E5E5",
    "Silver": "#C0C0C0",
    "Silver_Chalice": "#ACACAC",
    "Dusty_Gray": "#B0B0B0",
    "Suva_Gray": "#888888",
    "Dove_Gray": "#696969",
    "Emperor": "#555555",
    "Mine_Shaft": "#333333",
    "Black": "#000000"
}





def darken_color(hex_color, factor):
    # Remove # and convert to RGB
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    # Multiply by factor
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    # Ensure within 0-255
    r = min(255, max(0, r))
    g = min(255, max(0, g))
    b = min(255, max(0, b))
    # Convert back to hex
    return f"#{r:02x}{g:02x}{b:02x}"

# Generate tkinter_colors with dark variants
tkinter_colors = {}
for base_name, hex_val in base_colors.items():
    tkinter_colors[base_name] = hex_val
    tkinter_colors[f"Dark{base_name}"] = darken_color(hex_val, 0.66)
    tkinter_colors[f"DeepDark{base_name}"] = darken_color(hex_val, 0.33)

# Add grayscale colors without dark variants
for gray_name, hex_val in grayscale_colors.items():
    tkinter_colors[gray_name] = hex_val

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def find_closest_color(pixel_rgb):
    """Find the closest color in the palette to the given RGB pixel"""
    min_distance = float('inf')
    closest_color = None

    for color_name, hex_val in tkinter_colors.items():
        palette_rgb = hex_to_rgb(hex_val)
        # Calculate Euclidean distance in RGB space
        distance = math.sqrt(
            (pixel_rgb[0] - palette_rgb[0]) ** 2 +
            (pixel_rgb[1] - palette_rgb[1]) ** 2 +
            (pixel_rgb[2] - palette_rgb[2]) ** 2
        )
        if distance < min_distance:
            min_distance = distance
            closest_color = color_name

    return closest_color

# Fixed canvas size
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 1000

# Default values
PART_TYPE = 6
DEFAULT_SKIN = 0
DEFAULT_GRID_ROTATION = 0
DEFAULT_FLIP_VALUE = 0

# Initial grid size
grid_size = 20
cell_size = CANVAS_WIDTH // grid_size

# Variables for offset
offset_x = 0
offset_y = 0

# Grid to store colors
grid = []

# Selected color
selected_color = "Cinnabar"  # Default color

# Drawing tool: "pencil" or "rectangle"
drawing_tool = "pencil"

# Variables for rectangle drawing
rect_start = None  # (x, y) tuple for rectangle start point

# Zoom and pan variables
zoom_factor = 1.0
min_zoom = 0.1
max_zoom = 5.0
view_x = 0  # Horizontal pan offset
view_y = 0  # Vertical pan offset

def init_grid(size):
    global grid, cell_size
    grid = [[None for _ in range(size)] for _ in range(size)]
    cell_size = CANVAS_WIDTH // size
    draw_grid_lines()

def draw_grid_lines():
    canvas.delete("grid_line")
    for i in range(grid_size + 1):
        # Vertical lines
        x = i * cell_size
        canvas.create_line(x, 0, x, CANVAS_HEIGHT, fill="#CCCCCC", width=1, tags="grid_line")
        # Horizontal lines
        y = i * cell_size
        canvas.create_line(0, y, CANVAS_WIDTH, y, fill="#CCCCCC", width=1, tags="grid_line")

def draw_pixel(event):
    global rect_start
    # Convert screen coordinates to grid coordinates considering zoom and pan
    scaled_cell_size = int(cell_size * zoom_factor)
    if scaled_cell_size < 1:
        scaled_cell_size = 1

    grid_x = int((event.x + view_x) / scaled_cell_size)
    grid_y = int((event.y + view_y) / scaled_cell_size)

    if 0 <= grid_x < grid_size and 0 <= grid_y < grid_size:
        if drawing_tool == "pencil":
            if event.state & 0x100:  # Left button pressed (Button1)
                if selected_color:
                    grid[grid_y][grid_x] = selected_color
                    tk_color = tkinter_colors.get(selected_color, "black")
                    screen_x = int(grid_x * scaled_cell_size - view_x)
                    screen_y = int(grid_y * scaled_cell_size - view_y)
                    canvas.create_rectangle(screen_x, screen_y, screen_x + scaled_cell_size, screen_y + scaled_cell_size, fill=tk_color, outline="")
            elif event.state & 0x400:  # Right button pressed (Button3)
                grid[grid_y][grid_x] = None
                screen_x = int(grid_x * scaled_cell_size - view_x)
                screen_y = int(grid_y * scaled_cell_size - view_y)
                canvas.create_rectangle(screen_x, screen_y, screen_x + scaled_cell_size, screen_y + scaled_cell_size, fill="#DAD8D8", outline="#CCCCCC")
        elif drawing_tool == "rectangle":
            if event.state & 0x400:  # Right button pressed (Button3) - erase mode
                grid[grid_y][grid_x] = None
                screen_x = int(grid_x * scaled_cell_size - view_x)
                screen_y = int(grid_y * scaled_cell_size - view_y)
                canvas.create_rectangle(screen_x, screen_y, screen_x + scaled_cell_size, screen_y + scaled_cell_size, fill="#DAD8D8", outline="")

def flood_fill(x, y, target_color, replacement_color):
    """Flood fill algorithm to fill connected areas of the same color"""
    if target_color == replacement_color:
        return
    if target_color is None:
        return

    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if cx < 0 or cx >= grid_size or cy < 0 or cy >= grid_size:
            continue
        if grid[cy][cx] != target_color:
            continue

        grid[cy][cx] = replacement_color

        # Draw the cell
        if replacement_color is None:
            # Erase - draw background color
            canvas.create_rectangle(cx * cell_size, cy * cell_size, (cx + 1) * cell_size, (cy + 1) * cell_size, fill="#DAD8D8", outline="#CCCCCC")
        else:
            # Fill with color
            tk_color = tkinter_colors.get(replacement_color, "black")
            canvas.create_rectangle(cx * cell_size, cy * cell_size, (cx + 1) * cell_size, (cy + 1) * cell_size, fill=tk_color, outline="")

        # Add adjacent cells to stack
        stack.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])

def on_canvas_click(event):
    global rect_start
    if drawing_tool == "rectangle":
        # Convert screen coordinates to grid coordinates considering zoom and pan
        scaled_cell_size = int(cell_size * zoom_factor)
        if scaled_cell_size < 1:
            scaled_cell_size = 1

        grid_x = int((event.x + view_x) / scaled_cell_size)
        grid_y = int((event.y + view_y) / scaled_cell_size)

        if 0 <= grid_x < grid_size and 0 <= grid_y < grid_size:
            # Check which button was pressed
            is_right_click = (hasattr(event, 'num') and event.num == 3) or (event.state & 0x400)

            if is_right_click:
                # Right click - erase single cell like pencil
                grid[grid_y][grid_x] = None
                screen_x = int(grid_x * scaled_cell_size - view_x)
                screen_y = int(grid_y * scaled_cell_size - view_y)
                canvas.create_rectangle(screen_x, screen_y, screen_x + scaled_cell_size, screen_y + scaled_cell_size, fill="#DAD8D8", outline="#CCCCCC")
            else:
                # Left click - rectangle drawing
                if rect_start is None:
                    rect_start = (grid_x, grid_y)
                    # Show start point visually
                    canvas.delete("rect_start_point")
                    screen_x = int(grid_x * scaled_cell_size - view_x)
                    screen_y = int(grid_y * scaled_cell_size - view_y)
                    canvas.create_rectangle(screen_x, screen_y, screen_x + scaled_cell_size, screen_y + scaled_cell_size, outline="red", width=2, tags="rect_start_point")
                else:
                    # Draw rectangle from rect_start to current point
                    x1, y1 = rect_start
                    x2, y2 = grid_x, grid_y
                    # Normalize coordinates
                    x_start, x_end = sorted([x1, x2])
                    y_start, y_end = sorted([y1, y2])

                    for yy in range(y_start, y_end + 1):
                        for xx in range(x_start, x_end + 1):
                            grid[yy][xx] = selected_color
                            tk_color = tkinter_colors.get(selected_color, "black")
                            screen_x = int(xx * scaled_cell_size - view_x)
                            screen_y = int(yy * scaled_cell_size - view_y)
                            canvas.create_rectangle(screen_x, screen_y, screen_x + scaled_cell_size, screen_y + scaled_cell_size, fill=tk_color, outline="")
                    rect_start = None
                    canvas.delete("rect_start_point")

def select_tool(tool_name):
    global drawing_tool, rect_start
    drawing_tool = tool_name
    rect_start = None
    # Clear start point visual when tool changes
    canvas.delete("rect_start_point")

def select_color(color_name):
    global selected_color
    selected_color = color_name
    update_status_display()

# Add UI for tool selection
def add_tool_buttons():
    tool_frame = tk.Frame(controls_frame)
    tool_frame.grid(row=5, column=0, pady=10)
    pencil_btn = tk.Button(tool_frame, text="Pencil", command=lambda: select_tool("pencil"))
    pencil_btn.grid(row=0, column=0, padx=5)
    rect_btn = tk.Button(tool_frame, text="Rectangle", command=lambda: select_tool("rectangle"))
    rect_btn.grid(row=0, column=1, padx=5)
    # Add status label for showing selected tool and color
    global status_label
    status_label = tk.Label(controls_frame, text="", anchor="w")
    status_label.grid(row=6, column=0, sticky="w", pady=5)
    update_status_display()



def update_status_display():
    status_text = f"Selected Tool: {drawing_tool.capitalize()} | Selected Color: {selected_color if selected_color else 'None'}"
    status_label.config(text=status_text)

def export_commands():
    commands = []
    commands.append('#multiline')

    # Find rectangular areas for /fill commands
    processed = [[False for _ in range(grid_size)] for _ in range(grid_size)]

    for y in range(grid_size):
        for x in range(grid_size):
            if grid[y][x] and not processed[y][x]:
                color_name = grid[y][x]
                skin = None

                # Handle dark and very dark color variants
                if color_name.startswith("DeepDark"):
                    # Very dark variant: base color ID + 72
                    base_name = color_name[8:]  # Remove "DeepDark" prefix
                    base_skin = colors.get(base_name)
                    if base_skin is not None:
                        skin = base_skin + 72
                elif color_name.startswith("Dark"):
                    # Dark variant: base color ID + 36
                    base_name = color_name[4:]  # Remove "Dark" prefix
                    base_skin = colors.get(base_name)
                    if base_skin is not None:
                        skin = base_skin + 36
                else:
                    # Regular color or grayscale
                    skin = colors.get(color_name)
                    if skin is None:
                        from colors import colors_from_white_to_black
                        skin = colors_from_white_to_black.get(color_name, DEFAULT_SKIN)

                # Find the largest rectangle of the same color
                max_width = 1
                max_height = 1

                # Check how far we can extend horizontally
                for w in range(1, grid_size - x + 1):
                    if x + w > grid_size:
                        break
                    can_extend = True
                    for yy in range(y, min(y + max_height, grid_size)):
                        if yy >= grid_size or grid[yy][x + w - 1] != color_name or processed[yy][x + w - 1]:
                            can_extend = False
                            break
                    if not can_extend:
                        break
                    max_width = w

                # Check how far we can extend vertically
                for h in range(1, grid_size - y + 1):
                    if y + h > grid_size:
                        break
                    can_extend = True
                    for xx in range(x, min(x + max_width, grid_size)):
                        if xx >= grid_size or grid[y + h - 1][xx] != color_name or processed[y + h - 1][xx]:
                            can_extend = False
                            break
                    if not can_extend:
                        break
                    max_height = h

                # Mark all cells in this rectangle as processed
                for yy in range(y, y + max_height):
                    for xx in range(x, x + max_width):
                        processed[yy][xx] = True

                # Flip y and add offset
                out_x1 = x + offset_x
                out_y1 = -(y + offset_y)
                out_x2 = (x + max_width - 1) + offset_x
                out_y2 = -((y + max_height - 1) + offset_y)

                # Use /fill for rectangles, /setpart for single cells
                if max_width > 1 or max_height > 1:
                    command = f"/fill {out_x1} {out_y1} {out_x2} {out_y2} {PART_TYPE} {skin} {DEFAULT_GRID_ROTATION} {DEFAULT_FLIP_VALUE}"
                else:
                    command = f"/setpart {out_x1} {out_y1} {PART_TYPE} {skin} {DEFAULT_GRID_ROTATION} {DEFAULT_FLIP_VALUE}"
                commands.append(command)

    output = "\n".join(commands)
    with open("output.txt", "w") as f:
        f.write(output)
    # Copy to clipboard
    root.clipboard_clear()
    root.clipboard_append(output)
    print("Commands exported to output.txt and copied to clipboard")

def update_canvas_size():
    global grid_size, canvas, grid
    try:
        new_size = int(size_entry.get())
        if new_size <= 0 or new_size > 1000:
            print("Size must be between 1 and 1000")
            return
        grid_size = new_size
        # Clear canvas first, then reinitialize grid
        canvas.delete("all")
        init_grid(grid_size)
        redraw_canvas()
    except ValueError:
        print("Invalid size input")

def update_offset():
    global offset_x, offset_y
    try:
        offset_x = int(offset_x_entry.get())
        offset_y = int(offset_y_entry.get())
        print(f"Offset set to x={offset_x}, y={offset_y}")
    except ValueError:
        print("Invalid offset input")

# Zoom and pan functions
def zoom_in():
    global zoom_factor
    if zoom_factor < max_zoom:
        zoom_factor *= 1.2
        if zoom_factor > max_zoom:
            zoom_factor = max_zoom
        redraw_canvas()

def zoom_out():
    global zoom_factor
    if zoom_factor > min_zoom:
        zoom_factor /= 1.2
        if zoom_factor < min_zoom:
            zoom_factor = min_zoom
        redraw_canvas()

def reset_zoom():
    global zoom_factor, view_x, view_y
    zoom_factor = 1.0
    view_x = 0
    view_y = 0
    redraw_canvas()

def pan_canvas(dx, dy):
    global view_x, view_y
    view_x += dx
    view_y += dy
    redraw_canvas()

def redraw_canvas():
    """Redraw the entire canvas with current zoom and pan settings"""
    canvas.delete("all")

    # Calculate scaled cell size
    scaled_cell_size = int(cell_size * zoom_factor)
    if scaled_cell_size < 1:
        scaled_cell_size = 1

    # Draw background cells (like erased cells)
    for y in range(grid_size):
        for x in range(grid_size):
            screen_x = int(x * scaled_cell_size - view_x)
            screen_y = int(y * scaled_cell_size - view_y)
            # Only draw if visible on screen
            if (screen_x + scaled_cell_size >= 0 and screen_x <= CANVAS_WIDTH and
                screen_y + scaled_cell_size >= 0 and screen_y <= CANVAS_HEIGHT):
                canvas.create_rectangle(
                    screen_x, screen_y,
                    screen_x + scaled_cell_size, screen_y + scaled_cell_size,
                    fill="#DAD8D8", outline="#CCCCCC"
                )

    # Draw grid lines
    canvas.delete("grid_line")
    for i in range(grid_size + 1):
        # Vertical lines
        x = int(i * scaled_cell_size - view_x)
        if 0 <= x <= CANVAS_WIDTH:
            canvas.create_line(x, 0, x, CANVAS_HEIGHT, fill="#CCCCCC", width=1, tags="grid_line")
        # Horizontal lines
        y = int(i * scaled_cell_size - view_y)
        if 0 <= y <= CANVAS_HEIGHT:
            canvas.create_line(0, y, CANVAS_WIDTH, y, fill="#CCCCCC", width=1, tags="grid_line")

    # Draw outer border
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, outline="black", width=2, tags="grid_line")

    # Draw filled cells
    for y in range(grid_size):
        for x in range(grid_size):
            if grid[y][x]:
                color = tkinter_colors.get(grid[y][x], "black")
                screen_x = int(x * scaled_cell_size - view_x)
                screen_y = int(y * scaled_cell_size - view_y)

                # Only draw if visible on screen
                if (screen_x + scaled_cell_size >= 0 and screen_x <= CANVAS_WIDTH and
                    screen_y + scaled_cell_size >= 0 and screen_y <= CANVAS_HEIGHT):
                    canvas.create_rectangle(
                        screen_x, screen_y,
                        screen_x + scaled_cell_size, screen_y + scaled_cell_size,
                        fill=color, outline=""
                    )

    # Draw rectangle start point if active
    if rect_start:
        start_x, start_y = rect_start
        screen_x = int(start_x * scaled_cell_size - view_x)
        screen_y = int(start_y * scaled_cell_size - view_y)
        canvas.create_rectangle(
            screen_x, screen_y,
            screen_x + scaled_cell_size, screen_y + scaled_cell_size,
            outline="red", width=2, tags="rect_start_point"
        )

# Create main window
root = tk.Tk()
root.title("BPPaint")

# Main frame
main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0)

# Controls frame on left
controls_frame = tk.Frame(main_frame)
controls_frame.grid(row=0, column=0, padx=10, pady=10)

# Color buttons
color_frame = tk.Frame(controls_frame)
color_frame.grid(row=0, column=0, pady=10)

# Grayscale colors from white to black
grayscale_colors = ["White", "Mercury", "Silver", "Silver_Chalice", "Dusty_Gray", "Suva_Gray", "Dove_Gray", "Emperor", "Mine_Shaft", "Black"]

# Separate colors into normal, dark, very dark, and grayscale
normal_colors = [c for c in tkinter_colors if not c.startswith("Dark") and not c.startswith("Deep") and c not in grayscale_colors]
dark_colors = [c for c in tkinter_colors if c.startswith("Dark") and not c.startswith("Deep")]
very_dark_colors = [c for c in tkinter_colors if c.startswith("Deep")]
grayscale = [c for c in tkinter_colors if c in grayscale_colors]

def add_color_buttons(color_list, row):
    for col, color_name in enumerate(color_list):
        btn = tk.Button(color_frame, text="", command=lambda c=color_name: select_color(c),activebackground=tkinter_colors.get(color_name, "white"), bg=tkinter_colors.get(color_name, "white"))
        btn.grid(row=row, column=col, padx=2, pady=2)

add_color_buttons(normal_colors, 0)
add_color_buttons(dark_colors, 1)
add_color_buttons(very_dark_colors, 2)
add_color_buttons(grayscale, 3)

# Erase button
erase_frame = tk.Frame(controls_frame)
erase_frame.grid(row=4, column=0, pady=10)
# Remove erase button as per user request
# erase_btn = tk.Button(erase_frame, text="Erase", command=lambda: select_color(None), bg="white", fg="black")
# erase_btn.grid(row=0, column=0)

# Add tool buttons
add_tool_buttons()

# Canvas size input
size_frame = tk.Frame(controls_frame)
size_frame.grid(row=1, column=0, pady=10)
tk.Label(size_frame, text="Canvas Size:").grid(row=0, column=0)
size_entry = tk.Entry(size_frame, width=5)
size_entry.insert(0, str(grid_size))
size_entry.grid(row=0, column=1)
size_btn = tk.Button(size_frame, text="Set Size", command=update_canvas_size)
size_btn.grid(row=0, column=2)

# Offset inputs
offset_frame = tk.Frame(controls_frame)
offset_frame.grid(row=2, column=0, pady=10)
tk.Label(offset_frame, text="Offset X:").grid(row=0, column=0)
offset_x_entry = tk.Entry(offset_frame, width=5)
offset_x_entry.insert(0, "0")
offset_x_entry.grid(row=0, column=1)
tk.Label(offset_frame, text="Offset Y:").grid(row=1, column=0)
offset_y_entry = tk.Entry(offset_frame, width=5)
offset_y_entry.insert(0, "0")
offset_y_entry.grid(row=1, column=1)
offset_btn = tk.Button(offset_frame, text="Set Offset", command=update_offset)
offset_btn.grid(row=2, column=0, columnspan=2)

# Export button
export_btn = tk.Button(controls_frame, text="Export Commands", command=export_commands)
export_btn.grid(row=3, column=0, pady=10)

# Add menu bar for file operations
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

def save_drawing():
    commands = []
    commands.append('#multiline')

    # Find rectangular areas for /fill commands
    processed = [[False for _ in range(grid_size)] for _ in range(grid_size)]

    for y in range(grid_size):
        for x in range(grid_size):
            if grid[y][x] and not processed[y][x]:
                color_name = grid[y][x]
                skin = None

                # Handle dark and very dark color variants
                if color_name.startswith("DeepDark"):
                    base_name = color_name[8:]
                    base_skin = colors.get(base_name)
                    if base_skin is not None:
                        skin = base_skin + 72
                elif color_name.startswith("Dark"):
                    base_name = color_name[4:]
                    base_skin = colors.get(base_name)
                    if base_skin is not None:
                        skin = base_skin + 36
                else:
                    skin = colors.get(color_name)
                    if skin is None:
                        from colors import colors_from_white_to_black
                        skin = colors_from_white_to_black.get(color_name, DEFAULT_SKIN)

                max_width = 1
                max_height = 1

                for w in range(1, grid_size - x + 1):
                    if x + w > grid_size:
                        break
                    can_extend = True
                    for yy in range(y, min(y + max_height, grid_size)):
                        if yy >= grid_size or grid[yy][x + w - 1] != color_name or processed[yy][x + w - 1]:
                            can_extend = False
                            break
                    if not can_extend:
                        break
                    max_width = w

                for h in range(1, grid_size - y + 1):
                    if y + h > grid_size:
                        break
                    can_extend = True
                    for xx in range(x, min(x + max_width, grid_size)):
                        if xx >= grid_size or grid[y + h - 1][xx] != color_name or processed[y + h - 1][xx]:
                            can_extend = False
                            break
                    if not can_extend:
                        break
                    max_height = h

                for yy in range(y, y + max_height):
                    for xx in range(x, x + max_width):
                        processed[yy][xx] = True

                out_x1 = x + offset_x
                out_y1 = -(y + offset_y)
                out_x2 = (x + max_width - 1) + offset_x
                out_y2 = -((y + max_height - 1) + offset_y)

                if max_width > 1 or max_height > 1:
                    command = f"/fill {out_x1} {out_y1} {out_x2} {out_y2} {PART_TYPE} {skin} {DEFAULT_GRID_ROTATION} {DEFAULT_FLIP_VALUE}"
                else:
                    command = f"/setpart {out_x1} {out_y1} {PART_TYPE} {skin} {DEFAULT_GRID_ROTATION} {DEFAULT_FLIP_VALUE}"
                commands.append(command)

    output = "\n".join(commands)

    # Save commands to file with grid size and offset in filename
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Save Drawing", initialfile=f"drawing.txt")
    if file_path:
        with open(file_path, "w") as f:
            f.write(output)
        print(f"Drawing saved to {file_path}")


def copy_to_clipboard():
    commands = []
    commands.append('#multiline')

    processed = [[False for _ in range(grid_size)] for _ in range(grid_size)]

    for y in range(grid_size):
        for x in range(grid_size):
            if grid[y][x] and not processed[y][x]:
                color_name = grid[y][x]
                skin = None

                if color_name.startswith("DeepDark"):
                    base_name = color_name[8:]
                    base_skin = colors.get(base_name)
                    if base_skin is not None:
                        skin = base_skin + 72
                elif color_name.startswith("Dark"):
                    base_name = color_name[4:]
                    base_skin = colors.get(base_name)
                    if base_skin is not None:
                        skin = base_skin + 36
                else:
                    skin = colors.get(color_name)
                    if skin is None:
                        from colors import colors_from_white_to_black
                        skin = colors_from_white_to_black.get(color_name, DEFAULT_SKIN)

                max_width = 1
                max_height = 1

                for w in range(1, grid_size - x + 1):
                    if x + w > grid_size:
                        break
                    can_extend = True
                    for yy in range(y, min(y + max_height, grid_size)):
                        if yy >= grid_size or grid[yy][x + w - 1] != color_name or processed[yy][x + w - 1]:
                            can_extend = False
                            break
                    if not can_extend:
                        break
                    max_width = w

                for h in range(1, grid_size - y + 1):
                    if y + h > grid_size:
                        break
                    can_extend = True
                    for xx in range(x, min(x + max_width, grid_size)):
                        if xx >= grid_size or grid[y + h - 1][xx] != color_name or processed[y + h - 1][xx]:
                            can_extend = False
                            break
                    if not can_extend:
                        break
                    max_height = h

                for yy in range(y, y + max_height):
                    for xx in range(x, x + max_width):
                        processed[yy][xx] = True

                out_x1 = x + offset_x
                out_y1 = -(y + offset_y)
                out_x2 = (x + max_width - 1) + offset_x
                out_y2 = -((y + max_height - 1) + offset_y)

                if max_width > 1 or max_height > 1:
                    command = f"/fill {out_x1} {out_y1} {out_x2} {out_y2} {PART_TYPE} {skin} {DEFAULT_GRID_ROTATION} {DEFAULT_FLIP_VALUE}"
                else:
                    command = f"/setpart {out_x1} {out_y1} {PART_TYPE} {skin} {DEFAULT_GRID_ROTATION} {DEFAULT_FLIP_VALUE}"
                commands.append(command)

    output = "\n".join(commands)
    root.clipboard_clear()
    root.clipboard_append(output)
    print("Commands copied to clipboard")

def import_png():
    """Import a PNG image and convert it to the grid"""
    file_path = filedialog.askopenfilename(
        title="Import PNG",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
    )
    if not file_path:
        return

    try:
        # Load the image
        image = Image.open(file_path)

        # Validate image size (max 256x256)
        if image.width > 256 or image.height > 256:
            print("Image is too large. Maximum size is 256x256 pixels.")
            return

        # Resize image to fit current grid_size
        resized_image = image.resize((grid_size, grid_size), Image.Resampling.LANCZOS)

        # Convert to RGB if necessary
        if resized_image.mode == 'RGBA':
            # Handle alpha transparency - composite on white background
            background = Image.new('RGB', resized_image.size, (255, 255, 255))
            background.paste(resized_image, mask=resized_image.split()[-1])
            resized_image = background
        elif resized_image.mode != 'RGB':
            resized_image = resized_image.convert('RGB')

        # Process each pixel and update grid
        for y in range(grid_size):
            for x in range(grid_size):
                pixel_rgb = resized_image.getpixel((x, y))
                closest_color = find_closest_color(pixel_rgb)
                grid[y][x] = closest_color

        # Redraw canvas
        redraw_canvas()

        print(f"Successfully imported PNG: {file_path}")

    except Exception as e:
        print(f"Error importing PNG: {e}")

file_menu.add_command(label="Save Drawing", command=save_drawing)
file_menu.add_command(label="Copy to Clipboard", command=copy_to_clipboard)
file_menu.add_command(label="Import PNG", command=import_png)

# Zoom and pan controls
zoom_pan_frame = tk.Frame(controls_frame)
zoom_pan_frame.grid(row=7, column=0, pady=10)

tk.Label(zoom_pan_frame, text="Zoom & Pan:").grid(row=0, column=0, columnspan=3, pady=5)

zoom_in_btn = tk.Button(zoom_pan_frame, text="Zoom In", command=zoom_in)
zoom_in_btn.grid(row=1, column=0, padx=2)

zoom_out_btn = tk.Button(zoom_pan_frame, text="Zoom Out", command=zoom_out)
zoom_out_btn.grid(row=1, column=1, padx=2)

reset_zoom_btn = tk.Button(zoom_pan_frame, text="Reset Zoom", command=reset_zoom)
reset_zoom_btn.grid(row=1, column=2, padx=2)

# Pan buttons
pan_up_btn = tk.Button(zoom_pan_frame, text="↑", command=lambda: pan_canvas(0, -50))
pan_up_btn.grid(row=2, column=1, pady=2)

pan_left_btn = tk.Button(zoom_pan_frame, text="←", command=lambda: pan_canvas(-50, 0))
pan_left_btn.grid(row=3, column=0, padx=2)

pan_right_btn = tk.Button(zoom_pan_frame, text="→", command=lambda: pan_canvas(50, 0))
pan_right_btn.grid(row=3, column=2, padx=2)

pan_down_btn = tk.Button(zoom_pan_frame, text="↓", command=lambda: pan_canvas(0, 50))
pan_down_btn.grid(row=4, column=1, pady=2)

# Canvas on right
canvas = tk.Canvas(main_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
canvas.grid(row=0, column=1)
canvas.bind("<B1-Motion>", draw_pixel)
canvas.bind("<B3-Motion>", draw_pixel)

# Bind canvas click for rectangle tool
canvas.bind("<Button-1>", on_canvas_click)
canvas.bind("<Button-3>", on_canvas_click)

# Bind ESC key to cancel rectangle creation
def cancel_rectangle(event):
    global rect_start
    if rect_start is not None:
        rect_start = None
        canvas.delete("rect_start_point")

root.bind("<Escape>", cancel_rectangle)

# Initialize grid after canvas is created
init_grid(grid_size)
redraw_canvas()

root.mainloop()
