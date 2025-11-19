"""
Sprite Sheet Packer for Kenworth W900L
Packs 16 rendered angles into a single 4x4 sprite sheet
"""

from PIL import Image
import os

# Configuration
INPUT_DIR = r"C:\Users\rober\Git\break_brake\assets_source\trucks\kenworth_w900\renders"
OUTPUT_DIR = r"C:\Users\rober\Git\break_brake\assets\images\trucks"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "kenworth_w900_pristine.png")

FRAME_SIZE = 512
COLS = 4
ROWS = 4
NUM_FRAMES = 16

def pack_sprite_sheet():
    """Pack 16 individual frames into a 2048x2048 sprite sheet"""
    print("\nKENWORTH W900L SPRITE SHEET PACKER")
    print("=" * 60)

    # Calculate sprite sheet dimensions
    sheet_width = FRAME_SIZE * COLS
    sheet_height = FRAME_SIZE * ROWS

    print(f"Individual frame size: {FRAME_SIZE}x{FRAME_SIZE}")
    print(f"Sprite sheet size: {sheet_width}x{sheet_height}")
    print(f"Total frames: {NUM_FRAMES} (arranged in {ROWS}x{COLS} grid)")

    # Create blank sprite sheet with transparency
    sprite_sheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))

    # Pack each frame into the sprite sheet
    for i in range(NUM_FRAMES):
        frame_path = os.path.join(INPUT_DIR, f"kenworth_w900_pristine_{i:02d}.png")

        # Check if frame exists
        if not os.path.exists(frame_path):
            print(f"WARNING: Frame {i} not found at {frame_path}")
            continue

        # Load frame
        frame = Image.open(frame_path)

        # Calculate position in grid
        col = i % COLS
        row = i // COLS
        x = col * FRAME_SIZE
        y = row * FRAME_SIZE

        # Paste frame into sprite sheet
        sprite_sheet.paste(frame, (x, y))

        print(f"Packed frame {i:02d} at position ({col}, {row}) -> pixel ({x}, {y})")

    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Save sprite sheet
    print(f"\nSaving sprite sheet to: {OUTPUT_FILE}")
    sprite_sheet.save(OUTPUT_FILE, 'PNG', optimize=True)

    # Check file size
    if os.path.exists(OUTPUT_FILE):
        size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
        print(f"Sprite sheet saved successfully!")
        print(f"File size: {size_mb:.2f} MB")
        print(f"Dimensions: {sheet_width}x{sheet_height}")
        print(f"Format: PNG with transparency (RGBA)")

        print("\n" + "=" * 60)
        print("SPRITE SHEET PACKING COMPLETE!")
        print("\nNext steps:")
        print("1. Verify sprite sheet looks correct")
        print("2. Integrate into Flame game (TruckComponent)")
        print("3. Test sprite rotation and rendering")
        print("4. Measure performance (60+ FPS target)")
    else:
        print("ERROR: Failed to save sprite sheet!")

def main():
    pack_sprite_sheet()

if __name__ == "__main__":
    main()
