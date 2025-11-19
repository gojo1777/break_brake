/// Sprite-based truck renderer
/// Loads and renders pre-rendered 3D truck sprites
library;

import 'package:flame/components.dart';
import 'package:flame/sprite.dart';
import 'dart:math' as math;

/// Renders a truck using a pre-rendered sprite sheet
/// Sprite sheet contains 16 rotation angles in a 4x4 grid
class TruckSpriteRenderer extends SpriteAnimationGroupComponent {
  final String spritePath;
  static const int numAngles = 16;
  static const int spriteSize = 512;
  static const int gridCols = 4;
  static const int gridRows = 4;

  TruckSpriteRenderer({
    required this.spritePath,
    required Vector2 size,
  }) : super(size: size);

  @override
  Future<void> onLoad() async {
    await super.onLoad();
    // Sprite rendering will be added in the next step
  }

  /// Get the sprite frame index (0-15) based on rotation angle
  /// Angle 0 is rear view, rotating clockwise
  static int getFrameIndexForAngle(double angleRadians) {
    // Normalize angle to 0-2π range
    double normalizedAngle = angleRadians % (2 * math.pi);
    if (normalizedAngle < 0) normalizedAngle += 2 * math.pi;

    // Convert to sprite index (0-15)
    // Each sprite represents 22.5 degrees (360/16)
    final degreesPerFrame = 360.0 / numAngles;
    final degrees = normalizedAngle * 180 / math.pi;

    // Offset by 90 degrees so angle 0 (pointing up) maps to frame 4
    // Frame 0 is rear view, frame 4 is right view, frame 8 is front view, etc.
    final offsetDegrees = (degrees + 90) % 360;

    final frameIndex = ((offsetDegrees / degreesPerFrame).round()) % numAngles;
    return frameIndex;
  }

  /// Get sprite position in the sprite sheet for a given frame index
  static Vector2 getFramePosition(int frameIndex) {
    final col = frameIndex % gridCols;
    final row = frameIndex ~/ gridCols;
    return Vector2(col * spriteSize.toDouble(), row * spriteSize.toDouble());
  }
}
