# 🚛 PHASE 1: Kenworth W900 Production Implementation
## Getting Your First Production-Quality Truck In-Game

**Goal**: Replace placeholder rectangle truck with photorealistic Kenworth W900
**Timeline**: Today (setup + integration)
**Success Metric**: Production truck renders in-game at 60+ FPS

---

## 📋 STEP-BY-STEP IMPLEMENTATION

### Step 1: Blender Setup (30 minutes)

#### 1.1 - Install Blender
**Download**: https://www.blender.org/download/ (use 4.0+)

**Install Location**: `C:\Program Files\Blender Foundation\Blender 4.0\`

**Verify Installation**:
```bash
# Open command prompt
cd "C:\Program Files\Blender Foundation\Blender 4.0"
blender --version
```

#### 1.2 - Create Project Structure
```bash
# Create directories for truck rendering
mkdir C:\Users\rober\Git\break_brake\assets_source
mkdir C:\Users\rober\Git\break_brake\assets_source\trucks
mkdir C:\Users\rober\Git\break_brake\assets_source\trucks\kenworth_w900
mkdir C:\Users\rober\Git\break_brake\assets_source\trucks\kenworth_w900\renders
mkdir C:\Users\rober\Git\break_brake\assets_source\trucks\kenworth_w900\sprite_sheets
```

---

### Step 2: Source Kenworth W900 Model (1-2 hours)

#### Option A: Purchase Model (FASTEST - Recommended)

**TurboSquid Search**:
- URL: https://www.turbosquid.com/Search/3D-Models/kenworth-w900
- Look for:
  - "Game Ready" tag
  - Low-poly or mid-poly (under 50k polygons)
  - Includes textures
  - FBX or OBJ format
  - Price: $50-150

**CGTrader Search**:
- URL: https://www.cgtrader.com/3d-models?keywords=kenworth+w900
- Same criteria as TurboSquid
- Often better prices

**Sketchfab Search**:
- URL: https://sketchfab.com/search?q=kenworth+w900&type=models
- Some free models available
- Check commercial license

**What to Download**:
- FBX or OBJ file format (Blender compatible)
- Textures included (diffuse, normal, metallic maps)
- Tractor only (no trailer - we render separately)

**Save Location**: `C:\Users\rober\Git\break_brake\assets_source\trucks\kenworth_w900\model.fbx`

#### Option B: Use Free Placeholder Model (FASTEST START)

While searching for the perfect paid model, let's use a placeholder to test the pipeline:

**Free Truck Models**:
1. **Free3D.com**: https://free3d.com/3d-models/truck
2. **CGTrader Free**: https://www.cgtrader.com/free-3d-models/car/truck
3. **Poly Pizza**: https://poly.pizza/ (search "truck")

**Note**: Use free model for testing, then swap with purchased W900 later

#### Option C: Commission Custom Model

**Fiverr Search**: "3D truck model game ready"
- Budget: $200-500
- Turnaround: 3-7 days
- Specify: Kenworth W900, game-ready, low-poly, PBR textures

**Not recommended for TODAY** - Use Option A or B to get started now

---

### Step 3: Blender Rendering Script (1 hour)

#### 3.1 - Create Rendering Script

**File**: `C:\Users\rober\Git\break_brake\assets_source\render_truck.py`

```python
"""
Blender Truck Rendering Script
Renders truck at 16 rotation angles for top-down game view
Usage: blender --background --python render_truck.py
"""

import bpy
import math
import os

# Configuration
OUTPUT_DIR = "C:/Users/rober/Git/break_brake/assets_source/trucks/kenworth_w900/renders"
TRUCK_OBJECT_NAME = "Truck"  # Change this to match your imported model name
NUM_ANGLES = 16
RESOLUTION = 512  # 512x512 per frame (Ultra quality)
TRANSPARENT_BG = True

# Camera settings (top-down view with slight angle)
CAMERA_HEIGHT = 10.0  # meters above truck
CAMERA_DISTANCE = 15.0  # meters away from truck
CAMERA_ANGLE = 65.0  # degrees from horizontal (65° = slight top-down)

def setup_scene():
    """Configure scene settings for optimal rendering"""
    scene = bpy.context.scene

    # Render settings
    scene.render.engine = 'CYCLES'  # Use Cycles for quality
    scene.cycles.samples = 128  # Good quality, reasonable speed
    scene.cycles.use_denoising = True  # Clean output
    scene.render.resolution_x = RESOLUTION
    scene.render.resolution_y = RESOLUTION
    scene.render.resolution_percentage = 100

    # Output settings
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'  # Transparent background
    scene.render.film_transparent = TRANSPARENT_BG

    # Use GPU if available
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
    bpy.context.scene.cycles.device = 'GPU'

    print("✅ Scene configured for rendering")

def setup_camera():
    """Position camera for top-down game view"""
    # Get or create camera
    if 'Camera' in bpy.data.objects:
        cam = bpy.data.objects['Camera']
    else:
        cam_data = bpy.data.cameras.new('Camera')
        cam = bpy.data.objects.new('Camera', cam_data)
        bpy.context.scene.collection.objects.link(cam)

    # Position camera
    cam.location = (0, -CAMERA_DISTANCE, CAMERA_HEIGHT)
    cam.rotation_euler = (math.radians(CAMERA_ANGLE), 0, 0)

    # Set as active camera
    bpy.context.scene.camera = cam

    # Adjust camera settings
    cam.data.lens = 50  # 50mm lens (realistic perspective)
    cam.data.clip_end = 1000  # Far clipping plane

    print(f"✅ Camera positioned at {cam.location}")

def setup_lighting():
    """Create 3-point lighting setup"""
    # Remove default lights
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        if obj.type == 'LIGHT':
            obj.select_set(True)
    bpy.ops.object.delete()

    # Key light (main light from front-left)
    key_light = bpy.data.lights.new('KeyLight', 'SUN')
    key_light.energy = 5.0
    key_obj = bpy.data.objects.new('KeyLight', key_light)
    bpy.context.scene.collection.objects.link(key_obj)
    key_obj.location = (-10, -10, 15)
    key_obj.rotation_euler = (math.radians(45), 0, math.radians(-45))

    # Fill light (softer light from right)
    fill_light = bpy.data.lights.new('FillLight', 'AREA')
    fill_light.energy = 200
    fill_light.size = 10
    fill_obj = bpy.data.objects.new('FillLight', fill_light)
    bpy.context.scene.collection.objects.link(fill_obj)
    fill_obj.location = (10, -5, 8)
    fill_obj.rotation_euler = (math.radians(60), 0, math.radians(45))

    # Rim light (backlight for edge definition)
    rim_light = bpy.data.lights.new('RimLight', 'SPOT')
    rim_light.energy = 300
    rim_obj = bpy.data.objects.new('RimLight', rim_light)
    bpy.context.scene.collection.objects.link(rim_obj)
    rim_obj.location = (0, 10, 12)
    rim_obj.rotation_euler = (math.radians(120), 0, 0)

    print("✅ 3-point lighting setup complete")

def center_truck(truck):
    """Center truck at origin for rotation"""
    # Set origin to center of geometry
    bpy.context.view_layer.objects.active = truck
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

    # Move to world origin
    truck.location = (0, 0, 0)
    truck.rotation_euler = (0, 0, 0)

    print(f"✅ Truck '{truck.name}' centered at origin")

def render_angles(truck):
    """Render truck at 16 rotation angles"""
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Render each angle
    for i in range(NUM_ANGLES):
        # Calculate rotation angle
        angle_degrees = i * (360 / NUM_ANGLES)
        angle_radians = math.radians(angle_degrees)

        # Rotate truck (Z-axis for top-down rotation)
        truck.rotation_euler.z = angle_radians

        # Set output path
        output_path = os.path.join(OUTPUT_DIR, f"kenworth_w900_pristine_{i:02d}.png")
        bpy.context.scene.render.filepath = output_path

        # Render!
        print(f"Rendering angle {i+1}/{NUM_ANGLES} ({angle_degrees}°)...")
        bpy.ops.render.render(write_still=True)

        print(f"✅ Saved: {output_path}")

    print(f"\n🎉 All {NUM_ANGLES} angles rendered successfully!")

def main():
    """Main rendering pipeline"""
    print("\n🚛 KENWORTH W900 RENDERING PIPELINE")
    print("=" * 50)

    # Find truck object
    if TRUCK_OBJECT_NAME not in bpy.data.objects:
        print(f"❌ ERROR: Truck object '{TRUCK_OBJECT_NAME}' not found!")
        print(f"Available objects: {list(bpy.data.objects.keys())}")
        return

    truck = bpy.data.objects[TRUCK_OBJECT_NAME]
    print(f"✅ Found truck object: {truck.name}")

    # Setup pipeline
    setup_scene()
    setup_camera()
    setup_lighting()
    center_truck(truck)

    # Render
    render_angles(truck)

    print("\n✅ RENDERING COMPLETE!")
    print(f"Output location: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
```

**Save this file**, we'll use it once we have the 3D model.

#### 3.2 - Test Rendering Script

Once you have a truck model imported into Blender:

```bash
# Run from command line
cd "C:\Program Files\Blender Foundation\Blender 4.0"
blender "C:\Users\rober\Git\break_brake\assets_source\trucks\kenworth_w900\truck_scene.blend" --background --python "C:\Users\rober\Git\break_brake\assets_source\render_truck.py"
```

**Expected Output**: 16 PNG files in `renders/` folder, numbered 00-15

---

### Step 4: Manual Blender Workflow (Alternative to Script)

If you prefer working in Blender GUI:

#### 4.1 - Import Model
1. Open Blender
2. File → Import → FBX/OBJ
3. Navigate to your downloaded model
4. Import

#### 4.2 - Position for Rendering
1. Select truck
2. Press `N` to open properties panel
3. Set Location: X=0, Y=0, Z=0
4. Set Rotation: X=0°, Y=0°, Z=0°
5. Press `S` to scale if needed (truck should fill ~70% of frame)

#### 4.3 - Setup Camera
1. Select Camera (or Add → Camera if none exists)
2. Press `N` → View tab → Lock Camera to View
3. Position camera for top-down angle:
   - Location: X=0, Y=-15, Z=10
   - Rotation: X=65°, Y=0°, Z=0°
4. Adjust until truck fills frame nicely

#### 4.4 - Setup Lighting
1. Delete default light (select, press X, confirm)
2. Add → Light → Sun (key light)
   - Location: X=-10, Y=-10, Z=15
   - Energy: 5.0
3. Add → Light → Area (fill light)
   - Location: X=10, Y=-5, Z=8
   - Energy: 200, Size: 10
4. Add → Light → Spot (rim light)
   - Location: X=0, Y=10, Z=12
   - Energy: 300

#### 4.5 - Render Settings
1. Render Properties panel (camera icon)
2. Render Engine: Cycles
3. Device: GPU Compute (if available)
4. Samples: 128
5. Denoise: ON

6. Output Properties panel:
   - Resolution: 512x512
   - File Format: PNG
   - Color: RGBA (for transparency)
7. Film → Transparent: ON

#### 4.6 - Manual Rendering (16 angles)
For each angle (0°, 22.5°, 45°, 67.5°, 90°, 112.5°, 135°, 157.5°, 180°, 202.5°, 225°, 247.5°, 270°, 292.5°, 315°, 337.5°):

1. Select truck
2. Press `R` (rotate), `Z` (Z-axis), type angle value, Enter
3. Render → Render Image (F12)
4. Image → Save As → `kenworth_w900_pristine_00.png` (increment number)
5. Repeat for all 16 angles

**Note**: This is tedious! Script is much faster, but this works if script has issues.

---

### Step 5: Create Sprite Sheet (30 minutes)

Once you have 16 rendered PNG files, we need to pack them into a sprite sheet.

#### 5.1 - Install ImageMagick (for automated packing)

**Download**: https://imagemagick.org/script/download.php#windows
- Get Windows installer
- Install to default location
- Check "Add to PATH"

**Verify**:
```bash
magick --version
```

#### 5.2 - Pack Sprite Sheet

**Create script**: `C:\Users\rober\Git\break_brake\assets_source\pack_sprite_sheet.py`

```python
"""
Pack 16 rendered angles into a single sprite sheet
4 columns x 4 rows = 16 frames
"""

from PIL import Image
import os

INPUT_DIR = "C:/Users/rober/Git/break_brake/assets_source/trucks/kenworth_w900/renders"
OUTPUT_FILE = "C:/Users/rober/Git/break_brake/assets/images/trucks/kenworth_w900_pristine.png"
FRAME_SIZE = 512  # Each frame is 512x512
COLS = 4
ROWS = 4

def pack_sprite_sheet():
    """Pack 16 frames into 4x4 grid"""
    # Create output image (2048x2048 for 4x4 grid of 512x512)
    sheet_width = FRAME_SIZE * COLS
    sheet_height = FRAME_SIZE * ROWS
    sprite_sheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))

    # Load and paste each frame
    for i in range(16):
        # Load frame
        frame_path = os.path.join(INPUT_DIR, f"kenworth_w900_pristine_{i:02d}.png")
        if not os.path.exists(frame_path):
            print(f"❌ Missing frame: {frame_path}")
            continue

        frame = Image.open(frame_path)

        # Calculate position in grid
        col = i % COLS
        row = i // COLS
        x = col * FRAME_SIZE
        y = row * FRAME_SIZE

        # Paste into sprite sheet
        sprite_sheet.paste(frame, (x, y))
        print(f"✅ Packed frame {i:02d} at ({col}, {row})")

    # Save sprite sheet
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    sprite_sheet.save(OUTPUT_FILE, 'PNG', optimize=True)
    print(f"\n🎉 Sprite sheet saved: {OUTPUT_FILE}")
    print(f"Size: {sheet_width}x{sheet_height} pixels")

if __name__ == "__main__":
    pack_sprite_sheet()
```

**Run it**:
```bash
python C:\Users\rober\Git\break_brake\assets_source\pack_sprite_sheet.py
```

**Output**: `assets/images/trucks/kenworth_w900_pristine.png` (2048x2048 sprite sheet)

#### 5.3 - Manual Packing (if script doesn't work)

Use any image editing software:
1. Create 2048x2048 canvas
2. Import all 16 frames
3. Arrange in 4x4 grid (top-left = 0°, continues clockwise)
4. Export as PNG with transparency

---

### Step 6: Integrate into Flame Game (1-2 hours)

Now we replace the rectangle rendering with sprite-based rendering!

#### 6.1 - Create Sprite Loading System

**File**: `lib/components/truck/truck_sprite_renderer.dart`

```dart
import 'package:flame/components.dart';
import 'package:flame/sprite.dart';
import 'dart:math';

/// Handles loading and rendering truck sprites with rotation
class TruckSpriteRenderer {
  static const int NUM_ANGLES = 16;
  static const double ANGLE_INCREMENT = 2 * pi / NUM_ANGLES;

  late SpriteSheet spriteSheet;
  late List<Sprite> rotationSprites;
  bool isLoaded = false;

  /// Load sprite sheet for a specific truck model and damage state
  Future<void> load({
    required String truckModel,
    required String damageState, // 'pristine', 'light', 'medium', 'heavy', 'destroyed'
    required Vector2 spriteSize,
  }) async {
    final String spritePath = 'trucks/${truckModel}_$damageState.png';

    // Load sprite sheet (4x4 grid = 16 frames)
    spriteSheet = SpriteSheet(
      image: await Flame.images.load(spritePath),
      srcSize: spriteSize,
    );

    // Extract individual rotation sprites
    rotationSprites = [];
    for (int row = 0; row < 4; row++) {
      for (int col = 0; col < 4; col++) {
        final sprite = spriteSheet.getSprite(row, col);
        rotationSprites.add(sprite);
      }
    }

    isLoaded = true;
  }

  /// Get the appropriate sprite for a given rotation angle
  Sprite getSpriteForAngle(double angleRadians) {
    if (!isLoaded || rotationSprites.isEmpty) {
      throw StateError('Sprites not loaded! Call load() first.');
    }

    // Normalize angle to 0-2π range
    double normalizedAngle = angleRadians % (2 * pi);
    if (normalizedAngle < 0) normalizedAngle += 2 * pi;

    // Calculate which sprite index to use
    int spriteIndex = ((normalizedAngle / ANGLE_INCREMENT) + 0.5).floor() % NUM_ANGLES;

    return rotationSprites[spriteIndex];
  }

  /// Render truck sprite at current rotation
  void render(Canvas canvas, Vector2 position, double angleRadians, Vector2 size) {
    if (!isLoaded) return;

    final sprite = getSpriteForAngle(angleRadians);

    // Render sprite centered at position
    sprite.render(
      canvas,
      position: position - size / 2, // Center sprite
      size: size,
    );
  }
}
```

#### 6.2 - Update TruckComponent

Modify `lib/components/truck/truck_component.dart`:

```dart
import 'package:break_brake/components/truck/truck_sprite_renderer.dart';

class TruckComponent extends PositionComponent with CollisionCallbacks {
  // ... existing fields ...

  // NEW: Sprite renderer
  late TruckSpriteRenderer spriteRenderer;
  bool useSprites = true; // Toggle for testing

  @override
  Future<void> onLoad() async {
    super.onLoad();

    // Initialize sprite renderer
    spriteRenderer = TruckSpriteRenderer();
    await spriteRenderer.load(
      truckModel: 'kenworth_w900',
      damageState: 'pristine',
      spriteSize: Vector2(512, 512), // Size of each frame in sprite sheet
    );

    // ... rest of existing onLoad code ...
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);

    if (useSprites && spriteRenderer.isLoaded) {
      // NEW: Sprite-based rendering
      spriteRenderer.render(
        canvas,
        Vector2.zero(), // Position (relative to component)
        angle, // Current rotation angle
        size, // Component size
      );
    } else {
      // FALLBACK: Keep existing rectangle rendering for debugging
      _renderDebugShape(canvas);
    }
  }

  void _renderDebugShape(Canvas canvas) {
    // ... existing rectangle rendering code ...
    // Keep this for debugging/fallback
  }

  // ... rest of existing code ...
}
```

#### 6.3 - Test In-Game

Run the game:
```bash
cd C:\Users\rober\Git\break_brake
flutter run
```

**What to verify**:
- [ ] Sprite loads without errors
- [ ] Truck renders at correct size
- [ ] Rotation looks smooth (16 angles should be barely noticeable steps)
- [ ] Collision still works (hitbox unchanged)
- [ ] Performance is 60+ FPS

#### 6.4 - Troubleshooting

**If sprite doesn't appear**:
1. Check file path: `assets/images/trucks/kenworth_w900_pristine.png` exists
2. Check `pubspec.yaml` includes assets folder:
   ```yaml
   flutter:
     assets:
       - assets/images/trucks/
   ```
3. Run `flutter clean` and `flutter pub get`
4. Check console for loading errors

**If rotation looks wrong**:
- Verify sprite sheet layout (frame 0 = 0°, clockwise)
- Check angle calculation in `getSpriteForAngle()`

**If performance drops**:
- Reduce sprite resolution (use 256x256 instead of 512x512)
- Check device isn't overheating
- Profile with Flutter DevTools

---

### Step 7: Damage State System (Future)

Once pristine truck works, you'll add damage states:

**Damage States to Render**:
1. `kenworth_w900_pristine.png` (0-20% damage)
2. `kenworth_w900_light.png` (20-40% damage)
3. `kenworth_w900_medium.png` (40-60% damage)
4. `kenworth_w900_heavy.png` (60-80% damage)
5. `kenworth_w900_destroyed.png` (80-100% damage)

**Implementation**:
```dart
// In TruckComponent, update damage state
void updateDamageVisuals() {
  String damageState;
  if (currentDamage < 20) {
    damageState = 'pristine';
  } else if (currentDamage < 40) {
    damageState = 'light';
  } else if (currentDamage < 60) {
    damageState = 'medium';
  } else if (currentDamage < 80) {
    damageState = 'heavy';
  } else {
    damageState = 'destroyed';
  }

  // Reload sprite if damage state changed
  if (damageState != currentDamageState) {
    currentDamageState = damageState;
    spriteRenderer.load(
      truckModel: 'kenworth_w900',
      damageState: damageState,
      spriteSize: Vector2(512, 512),
    );
  }
}
```

**For today**: Focus on pristine state only!

---

## 🎯 TODAY'S SUCCESS CRITERIA

By end of today, you should have:

- [ ] Blender installed and tested
- [ ] Kenworth W900 3D model sourced (purchased or free placeholder)
- [ ] Rendering script created and tested
- [ ] 16 rotation angles rendered
- [ ] Sprite sheet packed
- [ ] Sprite integrated into Flame game
- [ ] Game runs with production truck at 60+ FPS
- [ ] Can still play game (steering, collision work)

---

## ⚠️ IMPORTANT NOTES

### Keep Existing Code Working
- Don't delete rectangle rendering yet!
- Use `useSprites` boolean toggle for easy A/B testing
- If sprites break, can instantly fall back to rectangles

### Performance First
- Start with 512x512 sprites (high quality)
- If FPS drops, reduce to 256x256
- Profile with Flutter DevTools to find bottlenecks

### Iterate Quickly
- Use free/cheap placeholder model first
- Test full pipeline
- Once proven, invest in high-quality model

---

## 📞 TROUBLESHOOTING CONTACTS

**If you get stuck**:

**Blender Issues**:
- Reddit: r/blender
- Blender Stack Exchange
- YouTube: "Blender game asset rendering tutorial"

**Flutter/Flame Sprite Issues**:
- Flame Discord: https://discord.gg/pxrBmy4
- Flutter Discord: https://discord.gg/flutter
- Stack Overflow tag: [flame] [flutter]

**3D Model Issues**:
- TurboSquid support (if purchased)
- r/3Dmodeling
- Check model compatibility with Blender version

---

## 🚀 NEXT STEPS AFTER TODAY

Once first truck works:

**Week 1**:
- Add damage states (5 states × 16 angles = 80 renders)
- Optimize sprite sheet size
- Test on actual device (not just emulator)

**Week 2**:
- Add remaining 4 trucks (Peterbilt, Freightliner, Volvo, International)
- Each truck = 5 damage states × 16 angles
- Reuse rendering script for all trucks

**Week 3**:
- Begin Phase 2 (trailers)
- Environment textures
- Traffic car sprites

---

**Let's get that Kenworth W900 looking AMAZING! 🚛✨**

Ready to start? What's your first step - installing Blender or searching for the 3D model?
