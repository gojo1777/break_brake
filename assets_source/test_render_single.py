"""
Test Render - Single Angle of Kenworth W900L
Renders just angle 0 (front view) to verify quality
"""

import bpy
import os

# Configuration
OUTPUT_DIR = r"C:\Users\rober\Git\break_brake\assets_source\trucks\kenworth_w900\renders"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "kenworth_w900_pristine_00_TEST.png")

def main():
    print("\n🎨 KENWORTH W900L TEST RENDER")
    print("=" * 50)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Set output path
    bpy.context.scene.render.filepath = OUTPUT_FILE

    print(f"📂 Output: {OUTPUT_FILE}")
    print(f"📐 Resolution: {bpy.context.scene.render.resolution_x}x{bpy.context.scene.render.resolution_y}")
    print(f"🎥 Camera: {bpy.context.scene.camera.name}")

    # Find the truck (should be centered at origin already)
    truck_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
    print(f"🚛 Found {len(truck_objects)} mesh objects")

    # Render!
    print("\n🎬 RENDERING... (this will take 2-3 minutes)")
    print("⏳ Please wait...")

    bpy.ops.render.render(write_still=True)

    print(f"\n✅ TEST RENDER COMPLETE!")
    print(f"📁 Saved to: {OUTPUT_FILE}")
    print(f"📊 File size: {os.path.getsize(OUTPUT_FILE) / 1024:.1f} KB")

    # Verify file exists
    if os.path.exists(OUTPUT_FILE):
        print("\n🎉 SUCCESS! Render file created successfully!")
        print("\n📝 Next steps:")
        print("1. Check the render image to verify quality")
        print("2. If good → render all 16 angles")
        print("3. Create sprite sheet")
        print("4. Integrate into game!")
    else:
        print("\n❌ ERROR: Render file not found!")

if __name__ == "__main__":
    main()
