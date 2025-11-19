"""
Blender Setup Script for Kenworth W900L
Automatically imports truck, sets up camera and lighting, and prepares for rendering

Usage: blender --python setup_truck_scene.py
"""

import bpy
import math
import os

# Configuration
TRUCK_MODEL_PATH = r"C:\Users\rober\Git\break_brake\assets_source\trucks\kenworth_w900\source\Kenworth W900L.glb"
OUTPUT_SCENE_PATH = r"C:\Users\rober\Git\break_brake\assets_source\trucks\kenworth_w900\kenworth_scene.blend"

def clear_scene():
    """Delete all default objects"""
    print("🧹 Clearing default scene...")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Clear lights
    for light in bpy.data.lights:
        bpy.data.lights.remove(light)

    # Clear cameras
    for cam in bpy.data.cameras:
        bpy.data.cameras.remove(cam)

    print("✅ Scene cleared")

def import_truck():
    """Import the Kenworth W900L GLB model"""
    print(f"📥 Importing truck from: {TRUCK_MODEL_PATH}")

    if not os.path.exists(TRUCK_MODEL_PATH):
        print(f"❌ ERROR: Truck model not found at {TRUCK_MODEL_PATH}")
        return None

    # Import GLB file
    bpy.ops.import_scene.gltf(filepath=TRUCK_MODEL_PATH)

    # Get imported objects (they should be selected after import)
    imported_objects = bpy.context.selected_objects

    if not imported_objects:
        print("❌ ERROR: No objects imported!")
        return None

    print(f"✅ Imported {len(imported_objects)} objects")

    # Find the main truck object (usually the largest mesh)
    truck = max(imported_objects, key=lambda obj: len(obj.data.vertices) if obj.type == 'MESH' else 0)

    return truck

def setup_camera_topdown():
    """Setup camera for top-down game view"""
    print("📷 Setting up camera...")

    # Create camera
    cam_data = bpy.data.cameras.new('GameCamera')
    cam = bpy.data.objects.new('GameCamera', cam_data)
    bpy.context.scene.collection.objects.link(cam)

    # Position camera for top-down view with slight angle
    cam.location = (0, -20, 12)  # Behind and above
    cam.rotation_euler = (math.radians(65), 0, 0)  # Tilt down

    # Camera settings
    cam.data.lens = 50  # 50mm lens (realistic)
    cam.data.clip_end = 1000

    # Set as active camera
    bpy.context.scene.camera = cam

    print(f"✅ Camera positioned at {cam.location}")

    return cam

def setup_lighting():
    """Create 3-point lighting setup"""
    print("💡 Setting up 3-point lighting...")

    # Key light (main light from front-left)
    key_light_data = bpy.data.lights.new('KeyLight', 'SUN')
    key_light_data.energy = 5.0
    key_light = bpy.data.objects.new('KeyLight', key_light_data)
    bpy.context.scene.collection.objects.link(key_light)
    key_light.location = (-10, -10, 15)
    key_light.rotation_euler = (math.radians(45), 0, math.radians(-45))

    # Fill light (softer light from right)
    fill_light_data = bpy.data.lights.new('FillLight', 'AREA')
    fill_light_data.energy = 200
    fill_light_data.size = 10
    fill_light = bpy.data.objects.new('FillLight', fill_light_data)
    bpy.context.scene.collection.objects.link(fill_light)
    fill_light.location = (10, -5, 8)
    fill_light.rotation_euler = (math.radians(60), 0, math.radians(45))

    # Rim light (backlight for edge definition)
    rim_light_data = bpy.data.lights.new('RimLight', 'SPOT')
    rim_light_data.energy = 300
    rim_light = bpy.data.objects.new('RimLight', rim_light_data)
    bpy.context.scene.collection.objects.link(rim_light)
    rim_light.location = (0, 10, 12)
    rim_light.rotation_euler = (math.radians(120), 0, 0)

    print("✅ 3-point lighting created")

def center_truck_at_origin(truck):
    """Center truck at world origin"""
    if not truck:
        return

    print("🎯 Centering truck at origin...")

    # Set active object
    bpy.context.view_layer.objects.active = truck
    truck.select_set(True)

    # Set origin to geometry center
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

    # Move to world origin
    truck.location = (0, 0, 0)
    truck.rotation_euler = (0, 0, 0)

    print(f"✅ Truck centered at origin")

def configure_render_settings():
    """Setup render settings for sprite generation"""
    print("⚙️ Configuring render settings...")

    scene = bpy.context.scene

    # Render engine
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 128  # Good quality, reasonable speed
    scene.cycles.use_denoising = True

    # Resolution
    scene.render.resolution_x = 512
    scene.render.resolution_y = 512
    scene.render.resolution_percentage = 100

    # Output settings
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'  # Transparent background
    scene.render.film_transparent = True

    # Use GPU if available
    try:
        bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
        scene.cycles.device = 'GPU'
        print("✅ GPU rendering enabled")
    except:
        print("⚠️ GPU not available, using CPU")

    print("✅ Render settings configured")

def save_scene():
    """Save the Blender scene"""
    print(f"💾 Saving scene to: {OUTPUT_SCENE_PATH}")

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(OUTPUT_SCENE_PATH), exist_ok=True)

    # Save
    bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_SCENE_PATH)

    print("✅ Scene saved!")

def main():
    """Main setup pipeline"""
    print("\n🚛 KENWORTH W900L BLENDER SETUP")
    print("=" * 50)

    # Step 1: Clear scene
    clear_scene()

    # Step 2: Import truck
    truck = import_truck()
    if not truck:
        print("❌ FAILED: Could not import truck")
        return

    # Step 3: Center truck
    center_truck_at_origin(truck)

    # Step 4: Setup camera
    setup_camera_topdown()

    # Step 5: Setup lighting
    setup_lighting()

    # Step 6: Configure render settings
    configure_render_settings()

    # Step 7: Save scene
    save_scene()

    print("\n✅ SETUP COMPLETE!")
    print(f"📂 Scene saved to: {OUTPUT_SCENE_PATH}")
    print("\n📝 Next steps:")
    print("1. Open the scene in Blender GUI to verify it looks good")
    print("2. Run render_truck.py to generate 16 rotation sprites")
    print("3. Pack sprites into sprite sheet")
    print("4. Integrate into game!")

if __name__ == "__main__":
    main()
