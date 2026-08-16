import random

def get_corner_positions():
    # 1. Map available corner names
    corner_names = ["top-left", "top-right", "bottom-left", "bottom-right"]
    
    # 2. Randomly select 3 corners without replacement
    chosen_corners = random.sample(corner_names, 3)
    
    # 3. Assign numbers 1, 2, and 3 to the chosen corners
    assignments = {
        1: chosen_corners[0],
        2: chosen_corners[1],
        3: chosen_corners[2]
    }
    
    return assignments

if __name__ == "__main__":
    positions = get_corner_positions()
    
    # Print the mapped output
    for num, corner in positions.items():
        print(f"Number {num}: {corner}")
