# Optional MIT Lab 2 rotation-order proof

Let `R0 = Rx(90°)`, `R1 = Ry(180°)`, and `R2 = Rx(-30°)`. A rotation about a fixed world axis pre-multiplies the current orientation. Applying `R0`, then `R1`, then `R2` therefore yields `Rfinal = R2 R1 R0`.

A rotation about a moving body axis post-multiplies the current orientation. Applying the same rotations in reverse order, `R2`, then `R1`, then `R0`, yields `I R2 R1 R0 = R2 R1 R0`. The argument applies to any finite sequence of rotations about any axes and angles because each intrinsic step appends on the right while each extrinsic step prepends on the left.
