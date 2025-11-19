# 🎨 VISUAL UPGRADE ROADMAP
## From Prototype to Production Polish

**Target**: GTA mobile-quality visuals on high-end devices
**Timeline**: Phased approach - gameplay first, then progressive visual upgrades
**Status**: ✅ Phase 1 Complete - Production truck sprite rendering operational!

---

## 📊 RENDERING DECISION

### ✅ CHOSEN: Pre-rendered 3D Sprites (Option A)

**Technical Approach**:
- Create high-quality 3D models in Blender
- Render at 16 rotation angles (22.5° increments)
- Export as optimized sprite sheets
- Use Flame's sprite rendering system

**Why This Works**:
1. Flutter/Flame optimized for 2D sprite rendering
2. GTA Chinatown Wars / San Andreas mobile use this approach
3. Predictable 60-120 FPS performance
4. Better battery life than real-time 3D
5. Full artistic control (baked lighting, shadows, reflections)
6. Easier quality scaling for older devices

**Sprite Sheet Specs**:
- **Resolution per frame**: 512x512 pixels (ultra), 256x256 (high), 128x128 (medium)
- **Rotation angles**: 16 (can optimize to 8 for smaller vehicles)
- **Format**: PNG with alpha channel
- **Compression**: Optimized for mobile (use pngquant or similar)
- **Atlas packing**: Texture atlas for memory efficiency

---

## 🎯 PHASED IMPLEMENTATION STRATEGY

### ✅ Phase 0: Asset Pipeline Setup (COMPLETE - November 19, 2025)
**Goal**: Establish workflow for creating/importing production assets

- ✅ Set up Blender 4.5.3 LTS with project structure
- ✅ Created rendering scripts for 16-angle export (setup, test, render, pack)
- ✅ Tested sprite sheet generation (2048x2048, 382KB optimized)
- ✅ Integrated sprite into Flame game with TruckComponent
- 🔄 Performance verification pending (next session)

**Deliverable**: ✅ Working asset pipeline + Kenworth W900L production sprite

**Scripts Created**:
- `assets_source/setup_truck_scene.py` - Automated Blender scene setup
- `assets_source/test_render_single.py` - Single frame test renders
- `assets_source/render_truck_16_angles.py` - Batch render 16 angles
- `assets_source/pack_sprite_sheet.py` - Sprite sheet atlas packing

**Assets Created**:
- `assets/images/trucks/kenworth_w900_pristine.png` - Production sprite sheet

---

### ✅ Phase 1: Truck Visual Upgrade (PARTIALLY COMPLETE - November 19, 2025)
**Priority**: Player truck is what you see 100% of the time

#### ✅ 1.1 - 3D Model Creation/Sourcing (COMPLETE)
**Chosen Approach**: Free Sketchfab models from Korolv (Rig-n-Roll game assets)

**Models Acquired**:
1. ✅ **Kenworth W900L** - RENDERED & INTEGRATED (flagship truck)
2. ✅ **Peterbilt 379** - Downloaded, ready to render (classic icon)
3. ✅ **Kenworth T2000** - Downloaded, ready to render (modern)
4. ✅ **Freightliner Argosy B282** - Downloaded, ready to render (cab-over)
5. ⚠️ **Volvo VNL** - Not yet sourced
6. ⚠️ **International Lonestar** - Not yet sourced

**Assets Source**: Sketchfab (CC BY license) - Free high-quality truck models
- GLB/FBX formats with PBR textures
- 11-19MB per model
- Pre-rigged and textured

**Per-Truck Requirements**:
- Detailed cab exterior (grille, lights, mirrors, stacks)
- Proper UV mapping for textures
- Modular damage states (pristine, light, medium, heavy, destroyed)
- LOD levels (high detail for zoom, simplified for gameplay)

#### 1.2 - Truck Texturing
- **Base paint**: Solid colors (white, red, blue, black, custom)
- **Chrome materials**: Bumpers, grille, stacks, wheels
- **Weathering**: Road grime, rust, wear patterns
- **Damage textures**: Dents, scratches, rust holes
- **Decals**: Company logos, stripes, flames (customization)

#### 1.3 - Damage States
Each truck needs 5 visual states:
1. **Pristine** (0-20% damage): Clean, shiny
2. **Light** (20-40%): Minor dents, scratches
3. **Medium** (40-60%): Dents, missing chrome, cracked windshield
4. **Heavy** (60-80%): Serious damage, smoke, bent frame
5. **Destroyed** (80-100%): Totaled, fire, barely drivable

**Implementation**: Blend between states based on damage percentage

#### 1.4 - Integration
- Replace `TruckComponent` rendering with sprite system
- Load appropriate sprite sheet based on truck model
- Select rotation angle based on truck heading
- Overlay damage effects (smoke particles, sparks)
- Test performance (target: 60 FPS minimum)

**Deliverable**: One fully-rendered truck (Kenworth W900) with all damage states

---

### Phase 2: Trailer Visual Upgrade (1-2 days)
**Priority**: Visible 100% of gameplay, less detail than truck

**Trailer Types** (7 total):
1. **53' Dry Van** (most common)
2. **Reefer** (refrigerated, has cooling unit)
3. **Flatbed** (open deck, cargo straps)
4. **Lowboy** (low-slung heavy hauler)
5. **Tanker** (cylindrical, liquid cargo)
6. **Doubles** (two trailers)
7. **Triples** (three trailers - chaos mode!)

**Per-Trailer Requirements**:
- 8 rotation angles (less critical than truck)
- Damage states (focus on bridge hit damage)
- Proper connection point for truck hitch
- Cargo variants (logs, steel, containers for flatbed)

**Special Trailer Features**:
- **Reefer**: Cooling unit on front, white paint, insulation explosion on bridge hit
- **Lowboy**: Very low to ground, heavy equipment cargo
- **Tanker**: Reflective metal, baffle marks, hazmat placards

**Deliverable**: All 7 trailer types rendered with basic damage states

---

### Phase 3: Environment Upgrade (2-3 days)
**Priority**: Foundation for visual polish

#### 3.1 - Road Surface
**Current**: Solid gray rectangle
**Target**: Photorealistic asphalt

**Implementation**:
- High-res asphalt texture (2048x2048) with wear patterns
- Repeating tile pattern (seamless)
- Normal mapping for depth (optional, may impact performance)
- Variations: Fresh asphalt, worn, cracked, patched

**Lane Markings**:
- White dashed (lane dividers)
- Yellow solid (shoulder/center)
- Proper dimensions (4" wide, 10' dashes, 30' gaps per US standard)
- Faded/worn variations

**Road Debris**:
- Tire marks (black rubber streaks)
- Oil stains (dark spots)
- Reflectors (cat's eyes between lanes)
- Random litter (subtle)

#### 3.2 - Roadside Environment
**Shoulders**:
- Gravel texture (gray/brown stones)
- Grass beyond shoulder (darker green)
- Occasional reflector posts

**Background Scenery** (low priority, can be simple):
- Distant trees (dark silhouettes)
- Highway signs (overhead, roadside)
- Sky gradient (blue → lighter at horizon)

**Time of Day** (future enhancement):
- Day: Bright, high contrast
- Sunset: Orange/red tones, long shadows
- Night: Dark, headlight beams, reduced visibility

#### 3.3 - Integration
- Replace `RoadComponent` with textured rendering
- Tile textures efficiently (memory consideration)
- Test performance impact
- Add quality settings (High: detailed textures, Low: simplified)

**Deliverable**: Photorealistic road with lane markings and basic scenery

---

### Phase 4: Traffic & Obstacle Upgrade (2-3 days)
**Priority**: Primary destruction targets

#### 4.1 - Four-Wheeler Vehicles
**Current**: Colored rectangles (28-32px)
**Target**: Detailed 3D pre-rendered sprites

**Vehicle Types** (4-6 models):
1. **Sedan** (Toyota Camry style)
2. **SUV** (Tahoe/Explorer style)
3. **Sports Car** (Corvette/Mustang style)
4. **Minivan** (Soccer mom mobile)
5. **Pickup Truck** (F-150 style) [optional]
6. **Compact** (Honda Civic style) [optional]

**Per-Vehicle Requirements**:
- 8 rotation angles (sufficient for traffic)
- Color variations (red, blue, white, black, silver, yellow)
- Damage states:
  - Pristine (before hit)
  - Impact (moment of collision, compressed/deformed)
  - Wreckage (destroyed, post-collision)
- LOD: Lower detail than truck (they're smaller on screen)

**Deformation System**:
- Pre-render 3 deformation states:
  1. Front impact (crushed front)
  2. Side impact (door crushed)
  3. Totaled (all around damage)
- Blend/swap based on collision type

#### 4.2 - Destructible Obstacles
**Road Signs**:
- Speed limit signs (65, 55, 45 MPH)
- Warning signs (curve, bridge, construction)
- Mile markers
- Properly scaled (8-10 feet tall)
- Post + sign face
- Destruction: Sign flies off, post breaks

**Construction Barriers**:
- Orange concrete barriers (Jersey barriers)
- Plastic barrels (orange with reflective stripes)
- Cones (orange with white stripes)
- Realistic materials (concrete texture, plastic sheen)

**Low Bridge** (signature feature):
- Steel I-beam construction
- Warning signs approaching (1 mile, 1/2 mile, 500ft, 100ft)
- LED height display ("13'6" clearance")
- Flashing lights
- Massive structure (intimidating)

#### 4.3 - Integration
- Replace `CarComponent` rendering
- Implement deformation system
- Add destructible obstacle components
- Wire up low bridge collision
- Test destruction satisfaction factor

**Deliverable**: All traffic vehicles and obstacles with destruction states

---

### Phase 5: VFX & Particle Upgrade (1-2 days)
**Priority**: Enhance existing particle system with better visuals

**Current System**: ✅ Working particle emitter with sparks, debris, smoke, glass
**Upgrade**: Better visual quality while keeping existing logic

#### 5.1 - Particle Textures
**Replace simple shapes with textured sprites**:

**Sparks** ✨:
- Glowing streak texture
- Orange-yellow-white gradient
- Motion blur baked in
- HDR glow effect

**Debris** 🪨:
- Metal chunks (realistic rust, dents)
- Plastic pieces (shiny, varied colors)
- Rubber (tire chunks, black with tread)
- Variety of shapes/sizes

**Smoke** 💨:
- Volumetric smoke texture (gray wisps)
- Multiple frames for animation
- Expansion effect (grows over time)
- Alpha fade

**Glass** 💎:
- Realistic glass shards (sharp edges)
- Transparency with refraction tint
- Catches light (highlight effect)
- Various shard shapes

**Fire** 🔥 [NEW]:
- For heavily damaged vehicles
- Animated flame sprites (4-8 frames)
- Orange-red-yellow gradient
- Smoke particles spawn from fire

**Tire Smoke** 💨 [NEW]:
- For braking/spinning wheels
- White-gray smoke
- Trails behind vehicle
- Dissipates quickly

#### 5.2 - Screen Effects
**Motion Blur**:
- Directional blur at high speeds (>60 MPH)
- Subtle, doesn't obscure visibility
- Increases immersion

**Impact Flash**:
- White flash on heavy collision
- Very brief (0.1 sec)
- Intensity based on impact force

**Damage Vignette**:
- Screen edges darken as damage increases
- Red tint at critical damage
- Helps communicate danger

**Chromatic Aberration** [OPTIONAL]:
- RGB color separation on massive impacts
- Very brief (0.2 sec)
- Extreme impacts only (bridge hits)

#### 5.3 - Integration
- Create texture atlas for particle sprites
- Replace shape rendering with textured sprites
- Add new particle types (fire, tire smoke)
- Implement screen effects (shaders or overlays)
- Test performance impact

**Deliverable**: Enhanced particle system with realistic textures and screen effects

---

### Phase 6: HUD/UI Polish (1 day)
**Priority**: Make UI match new visual quality

**Current HUD**: Functional but basic

**Upgrades**:
- **Speedometer**:
  - Realistic gauge design (needle, numbers)
  - Redline zone at governor limit
  - MPH + KPH markings
  - Backlit at night

- **Damage Meter**:
  - Visual truck silhouette
  - Red zones show damaged areas
  - Animated warning pulse at critical damage

- **DP Counter**:
  - Bold numbers with glow effect
  - Popup animation on DP gain
  - Combo multiplier display

- **Career Stage Badge**:
  - Company Driver: Plain badge
  - Lease Operator: Chrome badge
  - Owner Operator: Gold chrome badge
  - Subtle glow effect

- **Minimap** [NEW]:
  - Top-right corner
  - Shows upcoming obstacles
  - Bridge warnings
  - Traffic density

**UI Style**:
- Trucker aesthetic (chrome, leather, diesel)
- CB radio inspiration
- Readable at high speeds
- Not cluttered

**Deliverable**: Polished HUD matching production quality

---

### Phase 7: Lighting & Post-Processing (1-2 days)
**Priority**: Final polish for cinematic feel

#### 7.1 - Dynamic Lighting
**Implementation Options**:
- **A) Pre-baked shadows** in sprites (easier, better performance)
- **B) Real-time shadows** using Flame overlays (more flexible, performance cost)

**Recommended**: Pre-baked shadows in sprites + simple real-time overlays for extreme effects

**Lighting Scenarios**:
1. **Day** (default):
   - Sun overhead (12-2pm position)
   - Short shadows
   - High contrast

2. **Sunset** [OPTIONAL]:
   - Orange-red light from side
   - Long shadows
   - Warm color grading

3. **Night** [OPTIONAL]:
   - Headlight beams (cones of light)
   - Streetlights (pools of light)
   - Reduced visibility

#### 7.2 - Camera Effects
**Existing**: ✅ Screen shake (working well)

**Add**:
- **Motion blur**: At high speeds
- **Depth of field**: Slight background blur (makes truck pop)
- **Color grading**: Subtle saturation boost (arcade feel)

#### 7.3 - Performance Optimization
- Quality presets:
  - **Ultra**: Full effects (S23 Ultra, iPhone 15 Pro)
  - **High**: Most effects, optimized textures
  - **Medium**: Simplified effects, compressed textures
  - **Low**: Minimal effects, lowest resolution assets

- Frame rate targets:
  - Ultra: 120 FPS
  - High: 90 FPS
  - Medium: 60 FPS
  - Low: 60 FPS (on older hardware)

**Deliverable**: Polished lighting and camera system with performance options

---

## 📦 ASSET CREATION WORKFLOW

### Recommended Pipeline:

#### For Vehicles (Truck, Trailer, Cars):
1. **Model** (Blender):
   - Create or purchase base 3D model
   - Refine details (grille, lights, chrome)
   - Create damage variations
   - UV unwrap for texturing

2. **Texture** (Substance Painter or Blender):
   - Base color maps
   - Metallic/roughness maps
   - Normal maps (for detail)
   - Damage/dirt overlays

3. **Render** (Blender):
   - Set up camera (top-down, ~30-45° angle)
   - Configure lighting (HDRI or 3-point)
   - Render 16 rotation angles (script this!)
   - Export PNG with alpha channel

4. **Post-Process** (ImageMagick or Photoshop batch):
   - Resize to target resolution
   - Optimize compression (pngquant)
   - Pack into texture atlas

5. **Import** (Flame):
   - Load sprite sheet
   - Configure animation (rotation angles)
   - Test in-game

#### For Environment (Roads, Obstacles):
1. **Texture** (Substance Designer or photo source):
   - Create seamless tiles
   - Variations for wear/damage
   - Export at multiple resolutions

2. **Import** (Flame):
   - Load as background tiles
   - Configure repeating pattern
   - Test performance

#### For Particles:
1. **Create** (Photoshop/After Effects):
   - Design particle sprites
   - Multiple variations per type
   - Alpha channel for transparency

2. **Pack** (TexturePacker):
   - Combine into atlas
   - Optimize for mobile

3. **Import** (Flame):
   - Replace existing particle rendering
   - Test spawn rates and performance

---

## 🎨 ASSET SOURCING OPTIONS

### 3D Models:
1. **TurboSquid** (https://www.turbosquid.com)
   - Search: "semi truck", "kenworth", "peterbilt"
   - Price: $50-300 per model
   - Quality: High, game-ready options available

2. **CGTrader** (https://www.cgtrader.com)
   - Similar to TurboSquid
   - Often better prices

3. **Sketchfab** (https://sketchfab.com)
   - Some free models (CC license)
   - Check license for commercial use

4. **Custom Commission**:
   - Fiverr/Upwork 3D artists
   - $200-500 per truck (full detail)
   - Specify: game-ready, low-poly, PBR textures

### Textures:
1. **Poly Haven** (https://polyhaven.com) - FREE!
   - Asphalt, concrete, metal
   - PBR materials
   - High resolution

2. **Quixel Megascans** (https://quixel.com/megascans)
   - Industry-standard textures
   - Free with Epic Games account
   - Road surfaces, weathering

3. **Substance Source** (subscription)
   - Procedural materials
   - Highly customizable

### Particle Textures:
1. **Create in Photoshop/Krita** (custom)
2. **Unity Asset Store** - Particle packs (check license)
3. **itch.io** - Game asset packs

---

## 🛠️ BLENDER RENDERING SETUP

### Camera Configuration:
```python
# Blender Python script for automated rendering
import bpy
import math

# Camera settings
cam = bpy.data.objects['Camera']
cam.location = (0, -15, 10)  # Top-down with angle
cam.rotation_euler = (math.radians(65), 0, 0)

# Render 16 angles
truck = bpy.data.objects['Truck']
for i in range(16):
    angle = i * 22.5  # 16 angles = 22.5° increments
    truck.rotation_euler.z = math.radians(angle)

    bpy.context.scene.render.filepath = f"/output/truck_{i:02d}.png"
    bpy.ops.render.render(write_still=True)
```

### Render Settings:
- **Resolution**: 512x512 per frame (Ultra), 256x256 (High)
- **Samples**: 256-512 (Cycles for quality)
- **File Format**: PNG with RGBA
- **Background**: Transparent
- **Lighting**: HDRI or 3-point setup
- **Output**: Sequentially numbered files

### Optimization:
- Use Cycles GPU rendering (faster)
- Denoising enabled (cleaner output)
- Render farm if available (faster turnaround)

---

## 📊 PERFORMANCE TARGETS

### Target Hardware Specs:

**High-End** (Ultra settings):
- Galaxy S23 Ultra (Snapdragon 8 Gen 2)
- iPhone 15 Pro (A17 Pro)
- 12GB+ RAM
- Target: 120 FPS

**Mid-Range** (High settings):
- Galaxy S21 (Snapdragon 888)
- iPhone 13 (A15)
- 8GB RAM
- Target: 90 FPS

**Budget** (Medium settings):
- Galaxy A54 (Exynos 1380)
- iPhone SE 3 (A15)
- 6GB RAM
- Target: 60 FPS

### Performance Budget:
- **Draw calls**: <100 per frame
- **Texture memory**: <512MB (High), <256MB (Medium)
- **Particle count**: <500 active particles
- **Physics updates**: 60 Hz (fixed timestep)

### Optimization Techniques:
1. **Sprite atlasing**: Pack textures to reduce draw calls
2. **Object pooling**: Reuse destroyed car sprites
3. **LOD system**: Lower detail sprites for distant objects
4. **Culling**: Don't render off-screen objects
5. **Quality scaling**: Auto-detect device and set appropriate quality

---

## 🎯 INTEGRATION STRATEGY

### Keep Existing Systems Intact:
✅ All game logic (`breaker_braker_game.dart`)
✅ Physics system (`TruckComponent`, `TrailerComponent`)
✅ Collision detection (Flame hitboxes)
✅ Haptic feedback (`HapticService`)
✅ Particle spawning logic (`CollisionParticle`)
✅ Screen shake (`ScreenShake`)
✅ State management (`GameStateProvider`)

### Replace Visual Layer Only:
- **Rendering code** in components (`render()` methods)
- **Sprite loading** (load sprite sheets instead of drawing shapes)
- **Particle textures** (use sprite textures instead of shapes)
- **Background** (textured road instead of solid color)
- **HUD graphics** (styled elements instead of basic text)

### Implementation Order:
1. Test integration with ONE truck (Kenworth W900)
2. Verify performance on target device
3. Add remaining trucks
4. Add trailers
5. Add environment
6. Add traffic/obstacles
7. Polish VFX
8. Final HUD/UI pass

### Rollback Plan:
- Keep current rendering code in separate branch
- If performance issues arise, can revert or adjust quality
- Git tags at each phase for easy rollback

---

## 📝 PHASE 0 ACTION ITEMS (IMMEDIATE)

### Today's Goals:
1. ✅ Review this roadmap
2. [ ] Decide on asset sourcing strategy:
   - Purchase 3D models vs commission vs create
   - Budget allocation
3. [ ] Set up Blender environment:
   - Install Blender 4.0+
   - Test rendering script
   - Verify output format works with Flame
4. [ ] Create test asset:
   - Single truck (Kenworth W900)
   - Single rotation angle
   - Integrate into game
   - Verify it renders correctly
5. [ ] Performance baseline:
   - Test current game FPS on target device
   - Establish performance budget

### Questions to Answer:
- **Budget**: How much to spend on 3D models?
  - DIY (free but time): ~40 hours per truck
  - Purchase ($50-150 each): ~2 hours integration per truck
  - Commission ($200-500 each): ~1 hour integration per truck

- **Timeline**: How fast do you want production quality?
  - Aggressive (2 weeks): Purchase/commission all assets
  - Moderate (1 month): Mix of purchase + custom work
  - Leisurely (2-3 months): DIY in Blender

- **Scope**: Full visual overhaul or phased?
  - Recommended: Phase 1 (trucks) first, test, then continue

---

## 🎬 NEXT STEPS

**RIGHT NOW**:
1. Discuss this roadmap
2. Choose asset sourcing strategy
3. Set Phase 0 goals

**THIS WEEK**:
1. Complete Phase 0 (asset pipeline setup)
2. Create one test truck sprite
3. Integrate and verify performance

**THIS MONTH**:
1. Complete Phase 1 (all trucks)
2. Complete Phase 2 (trailers)
3. Start Phase 3 (environment)

**FUTURE**:
1. Complete all phases
2. Soft launch with production visuals
3. Iterate based on player feedback

---

## 💰 BUDGET ESTIMATES

### Conservative (DIY Heavy):
- 3D models (purchase some): $500
- Textures (mostly free): $50
- Tools (Blender free, minor subscriptions): $100
- **Total**: ~$650 + significant time investment

### Moderate (Mix):
- 3D models (purchase most): $1,500
- Custom commissions (2-3 trucks): $1,000
- Textures (Quixel + custom): $200
- Tools/subscriptions: $200
- **Total**: ~$2,900

### Premium (Commission Everything):
- All 3D models commissioned: $3,000
- Professional texture artist: $1,500
- Tools/subscriptions: $300
- **Total**: ~$4,800

**Recommendation**: Start with **Moderate** approach
- Purchase base models ($1,500)
- Customize in Blender yourself
- Commission only if needed for specific details
- This balances cost, quality, and timeline

---

## ✅ SUCCESS METRICS

### Visual Quality:
- [ ] Trucks recognizable by model (W900 vs 379 vs Cascadia)
- [ ] Destruction feels satisfying
- [ ] Runs at 60+ FPS on target hardware
- [ ] Looks competitive with GTA mobile games

### Player Experience:
- [ ] Players understand what truck they're driving
- [ ] Damage is visually communicated clearly
- [ ] Environment feels like real highway
- [ ] Crashes are visceral and exciting

### Technical:
- [ ] Stable 60 FPS on Snapdragon 8 Gen 2 / A17 Pro
- [ ] <200MB app size with all assets
- [ ] Graceful quality scaling on older devices
- [ ] Battery life acceptable (>2 hours continuous play)

---

**Status**: Planning Complete - Ready for Phase 0
**Next Action**: Discuss roadmap, choose asset strategy, begin setup

---

*This is a MASSIVE upgrade. Take it one phase at a time. Focus on getting ONE truck looking amazing, then scale up.*
