# Blender Rendering Quick Reference

## Quick Commands for Next Trucks

### Peterbilt 379
```bash
# 1. Update setup script with new model path
# Edit setup_truck_scene.py line 13:
TRUCK_MODEL_PATH = r"C:\Users\rober\Git\break_brake\assets_source\trucks\peterbilt_379\source\Peterbilt 379.fbx"
OUTPUT_SCENE_PATH = r"C:\Users\rober\Git\break_brake\assets_source\trucks\peterbilt_379\peterbilt_scene.blend"

# 2. Setup scene
"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe" --background --python "C:\Users\rober\Git\break_brake\assets_source\setup_truck_scene.py"

# 3. Update render script paths (lines 11-12)
OUTPUT_DIR = r"C:\Users\rober\Git\break_brake\assets_source\trucks\peterbilt_379\renders"

# 4. Render all angles
"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe" --background "C:\Users\rober\Git\break_brake\assets_source\trucks\peterbilt_379\peterbilt_scene.blend" --python "C:\Users\rober\Git\break_brake\assets_source\render_truck_16_angles.py"

# 5. Update pack script paths (lines 12-13)
INPUT_DIR = r"C:\Users\rober\Git\break_brake\assets_source\trucks\peterbilt_379\renders"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "peterbilt_379_pristine.png")

# 6. Pack sprite sheet
python "C:\Users\rober\Git\break_brake\assets_source\pack_sprite_sheet.py"
```

### Kenworth T2000
```bash
# Same process, just update paths:
TRUCK_MODEL_PATH = r"C:\Users\rober\Git\break_brake\assets_source\trucks\kenworth_t2000\source\Kenworth T2000.fbx"
OUTPUT_SCENE_PATH = r"C:\Users\rober\Git\break_brake\assets_source\trucks\kenworth_t2000\kenworth_t2000_scene.blend"
OUTPUT_DIR = r"C:\Users\rober\Git\break_brake\assets_source\trucks\kenworth_t2000\renders"
OUTPUT_FILE = "kenworth_t2000_pristine.png"
```

### Freightliner Argosy
```bash
# Same process:
TRUCK_MODEL_PATH = r"C:\Users\rober\Git\break_brake\assets_source\trucks\freightliner_argosy\source\Freight_Argosy_B282 - low poly.obj"
OUTPUT_SCENE_PATH = r"C:\Users\rober\Git\break_brake\assets_source\trucks\freightliner_argosy\freightliner_scene.blend"
OUTPUT_DIR = r"C:\Users\rober\Git\break_brake\assets_source\trucks\freightliner_argosy\renders"
OUTPUT_FILE = "freightliner_argosy_pristine.png"
```

---

## File Paths to Update

### setup_truck_scene.py
- **Line 13**: `TRUCK_MODEL_PATH`
- **Line 14**: `OUTPUT_SCENE_PATH`

### render_truck_16_angles.py
- **Line 11**: `OUTPUT_DIR`
- **Line 12**: `TRUCK_NAME` (optional, for logging)

### pack_sprite_sheet.py
- **Line 12**: `INPUT_DIR`
- **Line 13**: `OUTPUT_DIR`
- **Line 14**: `OUTPUT_FILE`

---

## Batch Rendering Script (RECOMMENDED)

Create this script to render all trucks at once:

```python
# render_all_trucks.py
import subprocess
import os

trucks = [
    {
        'name': 'Peterbilt 379',
        'model': r'C:\Users\rober\Git\break_brake\assets_source\trucks\peterbilt_379\source\Peterbilt 379.fbx',
        'output_dir': r'C:\Users\rober\Git\break_brake\assets_source\trucks\peterbilt_379',
        'sprite_name': 'peterbilt_379_pristine.png'
    },
    {
        'name': 'Kenworth T2000',
        'model': r'C:\Users\rober\Git\break_brake\assets_source\trucks\kenworth_t2000\source\Kenworth T2000.fbx',
        'output_dir': r'C:\Users\rober\Git\break_brake\assets_source\trucks\kenworth_t2000',
        'sprite_name': 'kenworth_t2000_pristine.png'
    },
    {
        'name': 'Freightliner Argosy',
        'model': r'C:\Users\rober\Git\break_brake\assets_source\trucks\freightliner_argosy\source\Freight_Argosy_B282 - low poly.obj',
        'output_dir': r'C:\Users\rober\Git\break_brake\assets_source\trucks\freightliner_argosy',
        'sprite_name': 'freightliner_argosy_pristine.png'
    }
]

BLENDER_PATH = r"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"

for truck in trucks:
    print(f"\n{'='*60}")
    print(f"RENDERING: {truck['name']}")
    print(f"{'='*60}\n")

    # Setup scene
    print("1. Setting up Blender scene...")
    # TODO: Update setup script with truck paths, then run

    # Render angles
    print("2. Rendering 16 angles...")
    # TODO: Update render script, then run

    # Pack sprite sheet
    print("3. Packing sprite sheet...")
    # TODO: Update pack script, then run

    print(f"\nCOMPLETE: {truck['name']}")

print("\nALL TRUCKS RENDERED!")
```

---

## Testing Rendered Sprites

### Update TruckComponent.dart

After rendering a new truck, add it to the sprite loading:

```dart
// In TruckComponent class
static const Map<TruckType, String> _spritePaths = {
  TruckType.kenworthW900: 'trucks/kenworth_w900_pristine.png',
  TruckType.peterbilt379: 'trucks/peterbilt_379_pristine.png',
  TruckType.kenworthT680: 'trucks/kenworth_t2000_pristine.png',
  TruckType.freightlinerCascadia: 'trucks/freightliner_argosy_pristine.png',
};

@override
Future<void> onLoad() async {
  await super.onLoad();

  // Load sprite sheet for this truck type
  final spritePath = _spritePaths[truckModel.type];
  if (spritePath != null) {
    try {
      _spriteSheet = await game.images.load(spritePath);
      _useSpriteRendering = true;
    } catch (e) {
      print('Failed to load sprite: $spritePath');
      _useSpriteRendering = false;
    }
  }
}
```

---

## Performance Optimization

### For Traffic Vehicles (Smaller, Simpler)

Modify render settings for faster renders:

```python
# In configure_render_settings():
scene.cycles.samples = 64  # Half the samples (faster)
scene.render.resolution_x = 256  # Lower resolution
scene.render.resolution_y = 256

# Use 8 angles instead of 16:
NUM_ANGLES = 8
```

This gives:
- 2 seconds per frame (vs 4 seconds)
- 16 seconds total (vs 1 minute)
- 1024x1024 sprite sheet (vs 2048x2048)
- ~100KB file size (vs 382KB)

---

## Troubleshooting

### Blender Can't Find Model
- Check file path has correct backslashes
- Verify file exists with `dir` command
- Try absolute path instead of relative

### Import Fails
- GLB format is most reliable
- FBX sometimes needs manual axis conversion
- OBJ may need materials setup

### Renders Look Dark
- Increase key light energy (line 87: `key_light_data.energy = 5.0` → `10.0`)
- Add ambient lighting: `scene.world.use_nodes = True`

### Transparent Background Not Working
- Verify: `scene.render.film_transparent = True`
- Check output format is PNG (not JPG)
- Color mode must be RGBA (not RGB)

---

## Next Session Checklist

- [ ] Test Kenworth W900L in-game
- [ ] Measure FPS
- [ ] Render Peterbilt 379
- [ ] Render Kenworth T2000
- [ ] Render Freightliner Argosy
- [ ] Update TruckComponent with all sprite paths
- [ ] Test truck selection in garage

---

**Estimated Time**: ~5 minutes setup per truck, ~1 minute render time
**Total for 3 trucks**: ~20 minutes
