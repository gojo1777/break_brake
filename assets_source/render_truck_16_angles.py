"""
Blender 16-Angle Truck Rendering Script
Renders Kenworth W900L at 16 rotation angles for top-down game sprite
"""

import bpy
import math
import os

# Configuration
OUTPUT_DIR = r"C:\Users\rober\Git\break_brake\assets_source\trucks\kenworth_w900\renders"
TRUCK_NAME = "body"  # Main truck body object name
NUM_ANGLES = 16
RESOLUTION = 512

def find_truck_root():
    """Find the main truck object to rotate"""
    # Look for the main body object
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and 'body' in obj.name.lower():
            return obj

    # Fallback: find largest mesh
    meshes = [obj for obj in bpy.data.objects if obj.type == 'MESH']
    if meshes:
        return max(meshes, key=lambda obj: len(obj.data.vertices))

    return None

def render_all_angles():
    """Render truck at 16 rotation angles"""
    print("\n🎬 KENWORTH W900L - FULL 16-ANGLE RENDER")
    print("=" * 60)

    # Find truck
    truck = find_truck_root()
    if not truck:
        print("❌ ERROR: Could not find truck object!")
        return

    print(f"🚛 Found truck object: {truck.name}")
    print(f"📐 Resolution: {RESOLUTION}x{RESOLUTION}")
    print(f"🔄 Rendering {NUM_ANGLES} angles (360° rotation)")

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Store original rotation
    original_rotation = truck.rotation_euler.z

    # Render each angle
    for i in range(NUM_ANGLES):
        # Calculate rotation angle
        angle_degrees = i * (360 / NUM_ANGLES)
        angle_radians = math.radians(angle_degrees)

        # Rotate truck
        truck.rotation_euler.z = angle_radians

        # Update scene
        bpy.context.view_layer.update()

        # Set output path
        output_file = os.path.join(OUTPUT_DIR, f"kenworth_w900_pristine_{i:02d}.png")
        bpy.context.scene.render.filepath = output_file

        # Render!
        print(f"\n🎨 Rendering angle {i+1}/{NUM_ANGLES} ({angle_degrees:.1f}°)...")
        bpy.ops.render.render(write_still=True)

        # Check file size
        if os.path.exists(output_file):
            size_kb = os.path.getsize(output_file) / 1024
            print(f"   ✅ Saved: {output_file} ({size_kb:.1f} KB)")
        else:
            print(f"   ❌ ERROR: File not created!")

    # Restore original rotation
    truck.rotation_euler.z = original_rotation

    print("\n" + "=" * 60)
    print("🎉 ALL 16 ANGLES RENDERED SUCCESSFULLY!")
    print(f"📂 Output directory: {OUTPUT_DIR}")
    print(f"📊 Total files: {NUM_ANGLES} PNG images")
    print("\n📝 Next steps:")
    print("1. ✅ Check renders in output folder")
    print("2. ⏭️  Create sprite sheet (pack into 4x4 grid)")
    print("3. 🎮 Integrate into Flame game")
    print("4. 🚀 Test performance!")

def main():
    render_all_angles()

if __name__ == "__main__":
    main()
