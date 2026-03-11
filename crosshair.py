import os
import sys

def print_crosshair():
    """Print a crosshair at the center of the console"""
    # Get terminal size
    try:
        rows, cols = os.popen('mode con').read().split('\n')[3].split()
        cols = int(cols)
        rows = int(rows)
    except:
        # Fallback for different systems
        cols = 80
        rows = 24
    
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    center_row = rows // 2
    center_col = cols // 2
    
    # Create crosshair
    for i in range(rows):
        line = ""
        for j in range(cols):
            if i == center_row and j == center_col:
                line += "+"  # Center point
            elif i == center_row:
                line += "-"  # Horizontal line
            elif j == center_col:
                line += "|"  # Vertical line
            else:
                line += " "
        print(line)

if __name__ == "__main__":
    print_crosshair()
    input("\nPress Enter to exit...")
