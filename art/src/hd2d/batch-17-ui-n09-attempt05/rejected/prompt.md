# N09 chat frame redraw — attempt 05

Edited the existing chat frame into a 768×176 overlay. Requested dark teal and antique gold language, with only the narrow border and small corners visible. The entire interior and exterior must be transparent; no fill, tabs, text, checkerboard, anti-aliasing, blur, or partial alpha.

References: batch-15 chat-frame candidate, chat-tab-normal candidate, chat-tab-selected candidate.

Outcome: rejected. The image model returned a 2172×724 image (3:1 rather than the required 768×176), with 256 alpha values and 60,861 RGBA colors. Do not resize, crop, or install as N09.
