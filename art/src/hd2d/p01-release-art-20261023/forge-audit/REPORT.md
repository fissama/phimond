# Sprite Forge audit — 2026-10-23

Repo commit: `5324342fdfab72430f4e9604f3fe427009f8596d` (v0.4.0). Chỉ kiểm tra, không sinh ảnh, không sửa sprite nguồn.

Giữ nguyên ngưỡng mặc định. Chỉ bật side-view leg test cho dải ngang; dải lên/xuống không thể dùng bộ suy luận near/far từ chiều ngang. Không dùng kết quả số để thay quyền duyệt của Claude.

| Asset | Kết quả | WARN / FAIL / chưa chứng minh |
|---|---|---|
| player-female.run-down | warn | torso_drift: warn |
| player-female.run-up | warn | torso_drift: warn |
| player-female.run | fail | leg_alternation: fail, torso_drift: warn |
| player-male.run-down | warn | torso_drift: warn, seam: warn |
| player-male.run-up | warn | torso_drift: warn |
| player-male.run | warn | leg_alternation: needs-visual-review, torso_drift: warn |
| walker-baker.run-down | warn | torso_drift: warn |
| walker-baker.run-up | warn | torso_drift: warn |
| walker-baker.run | warn | leg_alternation: warn, torso_drift: warn |
| walker-boy.run-down | warn | torso_drift: warn |
| walker-boy.run-up | warn | torso_drift: warn |
| walker-boy.run | warn | leg_alternation: warn, torso_drift: warn |
| walker-elder.run-down | warn | identity_residual: warn, near_duplicates: warn, torso_drift: warn |
| walker-elder.run-up | warn | torso_drift: warn |
| walker-elder.run | warn | leg_alternation: warn, torso_drift: warn |
| walker-girl.run-down | warn | torso_drift: warn |
| walker-girl.run-up | warn | torso_drift: warn, seam: warn |
| walker-girl.run | warn | leg_alternation: warn, torso_drift: warn |
| walker-guard.run-up | warn | near_duplicates: warn, torso_drift: warn |
| walker-guard.run | warn | leg_alternation: warn, torso_drift: warn |
| walker-traveller.run-down | warn | near_duplicates: warn, torso_drift: warn |
| walker-traveller.run-up | warn | near_duplicates: warn |
| walker-traveller.run | fail | identity_head_ratio: fail, leg_alternation: fail, torso_drift: warn |

## Nguyên văn từng cảnh báo

### player-female.run-down

```json
[
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 6.2,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 92.0,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  }
]
```

### player-female.run-up

```json
[
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 17.95,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 96.4,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  }
]
```

### player-female.run

```json
[
  {
    "id": "leg_alternation",
    "status": "fail",
    "value": [
      "near",
      "near",
      "unclear",
      "near",
      "near",
      "near",
      "near",
      "near"
    ],
    "threshold": "lead differs between i and i+n/2",
    "verdict": "duplicated half-cycle: the same leg leads in both halves",
    "pairs": [
      [
        0,
        4,
        true
      ],
      [
        1,
        5,
        true
      ],
      [
        3,
        7,
        true
      ]
    ],
    "mode": "auto-luminance",
    "near_leading": 7,
    "unclear": 1,
    "half_cycle": {
      "pairs": [
        {
          "pair": [
            0,
            4
          ],
          "iou_best_shift": 0.8765
        },
        {
          "pair": [
            1,
            5
          ],
          "iou_best_shift": 0.8523
        },
        {
          "pair": [
            2,
            6
          ],
          "iou_best_shift": 0.7882
        },
        {
          "pair": [
            3,
            7
          ],
          "iou_best_shift": 0.7039
        }
      ],
      "adjacent_iou_median": 0.7364,
      "half_cycle_iou_median": 0.8202
    },
    "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
  },
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 5.16,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 92.3,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  }
]
```

### player-male.run-down

```json
[
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 5.03,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 95.5,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  },
  {
    "id": "seam",
    "status": "warn",
    "value": 1.7,
    "threshold": 1.5,
    "transitions": [
      [
        7,
        0
      ],
      [
        3,
        4
      ]
    ],
    "note": "largest frame-to-frame change over the median step; review these joins first"
  }
]
```

### player-male.run-up

```json
[
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 9.39,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 95.0,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  }
]
```

### player-male.run

```json
[
  {
    "id": "leg_alternation",
    "status": "needs-visual-review",
    "value": [
      "near",
      "unclear",
      "unclear",
      "unclear",
      "unclear",
      "unclear",
      "near",
      "near"
    ],
    "threshold": "lead differs between i and i+n/2",
    "verdict": "unknown: no pair of half-cycle frames shows a clear NEAR/FAR lead",
    "pairs": [],
    "mode": "auto-luminance",
    "near_leading": 3,
    "unclear": 5,
    "half_cycle": {
      "pairs": [
        {
          "pair": [
            0,
            4
          ],
          "iou_best_shift": 0.7389
        },
        {
          "pair": [
            1,
            5
          ],
          "iou_best_shift": 0.8127
        },
        {
          "pair": [
            2,
            6
          ],
          "iou_best_shift": 0.7249
        },
        {
          "pair": [
            3,
            7
          ],
          "iou_best_shift": 0.6381
        }
      ],
      "adjacent_iou_median": 0.6967,
      "half_cycle_iou_median": 0.7319
    },
    "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
  },
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 9.23,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 87.8,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  }
]
```

### walker-baker.run-down

```json
[
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 11.4,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 98.3,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  }
]
```

### walker-baker.run-up

```json
[
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 4.56,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 95.3,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  }
]
```

### walker-baker.run

```json
[
  {
    "id": "leg_alternation",
    "status": "warn",
    "value": [
      "near",
      "far",
      "near",
      "near",
      "far",
      "far",
      "unclear",
      "near"
    ],
    "threshold": "lead differs between i and i+n/2",
    "verdict": "mixed: some half-cycle pairs repeat the lead",
    "pairs": [
      [
        0,
        4,
        false
      ],
      [
        1,
        5,
        true
      ],
      [
        3,
        7,
        true
      ]
    ],
    "mode": "auto-luminance",
    "near_leading": 4,
    "unclear": 1,
    "half_cycle": {
      "pairs": [
        {
          "pair": [
            0,
            4
          ],
          "iou_best_shift": 0.7981
        },
        {
          "pair": [
            1,
            5
          ],
          "iou_best_shift": 0.802
        },
        {
          "pair": [
            2,
            6
          ],
          "iou_best_shift": 0.765
        },
        {
          "pair": [
            3,
            7
          ],
          "iou_best_shift": 0.8352
        }
      ],
      "adjacent_iou_median": 0.7584,
      "half_cycle_iou_median": 0.8001
    },
    "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
  },
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 4.66,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 100.1,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  }
]
```

### walker-boy.run-down

```json
[
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 7.9,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 95.7,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  }
]
```

### walker-boy.run-up

```json
[
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 9.67,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 98.8,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  }
]
```

### walker-boy.run

```json
[
  {
    "id": "leg_alternation",
    "status": "warn",
    "value": [
      "near",
      "near",
      "far",
      "far",
      "far",
      "near",
      "far",
      "near"
    ],
    "threshold": "lead differs between i and i+n/2",
    "verdict": "mixed: some half-cycle pairs repeat the lead",
    "pairs": [
      [
        0,
        4,
        false
      ],
      [
        1,
        5,
        true
      ],
      [
        2,
        6,
        true
      ],
      [
        3,
        7,
        false
      ]
    ],
    "mode": "auto-luminance",
    "near_leading": 4,
    "unclear": 0,
    "half_cycle": {
      "pairs": [
        {
          "pair": [
            0,
            4
          ],
          "iou_best_shift": 0.7443
        },
        {
          "pair": [
            1,
            5
          ],
          "iou_best_shift": 0.745
        },
        {
          "pair": [
            2,
            6
          ],
          "iou_best_shift": 0.7713
        },
        {
          "pair": [
            3,
            7
          ],
          "iou_best_shift": 0.8275
        }
      ],
      "adjacent_iou_median": 0.6749,
      "half_cycle_iou_median": 0.7581
    },
    "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
  },
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 2.17,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 98.0,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  }
]
```

### walker-elder.run-down

```json
[
  {
    "id": "identity_residual",
    "status": "warn",
    "value": {
      "0": null,
      "1": 1.0,
      "2": 1.58,
      "3": 0.98,
      "4": 1.27,
      "5": 0.86,
      "6": 0.98,
      "7": 1.26
    },
    "threshold": 1.5,
    "frames": [
      2
    ],
    "note": "head match residual over the median: face or costume drift"
  },
  {
    "id": "near_duplicates",
    "status": "warn",
    "value": [
      [
        1,
        5
      ],
      [
        2,
        6
      ]
    ],
    "threshold": 0.95,
    "note": "pairs with best-shift silhouette IoU at or above the threshold and similar colours"
  },
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 9.95,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 94.7,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  }
]
```

### walker-elder.run-up

```json
[
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 3.54,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 95.7,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  }
]
```

### walker-elder.run

```json
[
  {
    "id": "leg_alternation",
    "status": "warn",
    "value": [
      "near",
      "near",
      "far",
      "far",
      "near",
      "near",
      "near",
      "far"
    ],
    "threshold": "lead differs between i and i+n/2",
    "verdict": "mixed: some half-cycle pairs repeat the lead",
    "pairs": [
      [
        0,
        4,
        true
      ],
      [
        1,
        5,
        true
      ],
      [
        2,
        6,
        false
      ],
      [
        3,
        7,
        true
      ]
    ],
    "mode": "auto-luminance",
    "near_leading": 5,
    "unclear": 0,
    "half_cycle": {
      "pairs": [
        {
          "pair": [
            0,
            4
          ],
          "iou_best_shift": 0.8709
        },
        {
          "pair": [
            1,
            5
          ],
          "iou_best_shift": 0.8078
        },
        {
          "pair": [
            2,
            6
          ],
          "iou_best_shift": 0.782
        },
        {
          "pair": [
            3,
            7
          ],
          "iou_best_shift": 0.8586
        }
      ],
      "adjacent_iou_median": 0.6246,
      "half_cycle_iou_median": 0.8332
    },
    "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
  },
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 6.85,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 70.8,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  }
]
```

### walker-girl.run-down

```json
[
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 6.32,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 95.8,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  }
]
```

### walker-girl.run-up

```json
[
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 5.79,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 94.8,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  },
  {
    "id": "seam",
    "status": "warn",
    "value": 1.51,
    "threshold": 1.5,
    "transitions": [
      [
        7,
        0
      ]
    ],
    "note": "largest frame-to-frame change over the median step; review these joins first"
  }
]
```

### walker-girl.run

```json
[
  {
    "id": "leg_alternation",
    "status": "warn",
    "value": [
      "near",
      "near",
      "far",
      "near",
      "far",
      "near",
      "near",
      "near"
    ],
    "threshold": "lead differs between i and i+n/2",
    "verdict": "mixed: some half-cycle pairs repeat the lead",
    "pairs": [
      [
        0,
        4,
        false
      ],
      [
        1,
        5,
        true
      ],
      [
        2,
        6,
        false
      ],
      [
        3,
        7,
        true
      ]
    ],
    "mode": "auto-luminance",
    "near_leading": 6,
    "unclear": 0,
    "half_cycle": {
      "pairs": [
        {
          "pair": [
            0,
            4
          ],
          "iou_best_shift": 0.7684
        },
        {
          "pair": [
            1,
            5
          ],
          "iou_best_shift": 0.8474
        },
        {
          "pair": [
            2,
            6
          ],
          "iou_best_shift": 0.7706
        },
        {
          "pair": [
            3,
            7
          ],
          "iou_best_shift": 0.7773
        }
      ],
      "adjacent_iou_median": 0.7217,
      "half_cycle_iou_median": 0.7739
    },
    "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
  },
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 3.48,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 100.8,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  }
]
```

### walker-guard.run-up

```json
[
  {
    "id": "near_duplicates",
    "status": "warn",
    "value": [
      [
        1,
        5
      ]
    ],
    "threshold": 0.95,
    "note": "pairs with best-shift silhouette IoU at or above the threshold and similar colours"
  },
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 7.63,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 100.2,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  }
]
```

### walker-guard.run

```json
[
  {
    "id": "leg_alternation",
    "status": "warn",
    "value": [
      "near",
      "near",
      "near",
      "near",
      "near",
      "far",
      "far",
      "near"
    ],
    "threshold": "lead differs between i and i+n/2",
    "verdict": "mixed: some half-cycle pairs repeat the lead",
    "pairs": [
      [
        0,
        4,
        true
      ],
      [
        1,
        5,
        false
      ],
      [
        2,
        6,
        false
      ],
      [
        3,
        7,
        true
      ]
    ],
    "mode": "auto-luminance",
    "near_leading": 6,
    "unclear": 0,
    "half_cycle": {
      "pairs": [
        {
          "pair": [
            0,
            4
          ],
          "iou_best_shift": 0.6364
        },
        {
          "pair": [
            1,
            5
          ],
          "iou_best_shift": 0.6654
        },
        {
          "pair": [
            2,
            6
          ],
          "iou_best_shift": 0.7594
        },
        {
          "pair": [
            3,
            7
          ],
          "iou_best_shift": 0.6523
        }
      ],
      "adjacent_iou_median": 0.6481,
      "half_cycle_iou_median": 0.6588
    },
    "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
  },
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 10.79,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 78.5,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  }
]
```

### walker-traveller.run-down

```json
[
  {
    "id": "near_duplicates",
    "status": "warn",
    "value": [
      [
        1,
        4
      ],
      [
        2,
        6
      ],
      [
        2,
        7
      ],
      [
        3,
        5
      ]
    ],
    "threshold": 0.95,
    "note": "pairs with best-shift silhouette IoU at or above the threshold and similar colours"
  },
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 3.6,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 100.8,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  }
]
```

### walker-traveller.run-up

```json
[
  {
    "id": "near_duplicates",
    "status": "warn",
    "value": [
      [
        3,
        7
      ]
    ],
    "threshold": 0.95,
    "note": "pairs with best-shift silhouette IoU at or above the threshold and similar colours"
  }
]
```

### walker-traveller.run

```json
[
  {
    "id": "identity_head_ratio",
    "status": "fail",
    "value": {
      "0": 1.0,
      "1": 1.0,
      "2": 0.94,
      "3": 1.0,
      "4": 1.0,
      "5": 1.0,
      "6": 1.0,
      "7": 1.0
    },
    "threshold": [
      0.95,
      1.05
    ],
    "frames": [
      2
    ],
    "note": "head scale against the median frame (frame 0 template)"
  },
  {
    "id": "leg_alternation",
    "status": "fail",
    "value": [
      "near",
      "near",
      "near",
      "near",
      "near",
      "near",
      "near",
      "near"
    ],
    "threshold": "lead differs between i and i+n/2",
    "verdict": "duplicated half-cycle: the same leg leads in both halves",
    "pairs": [
      [
        0,
        4,
        true
      ],
      [
        1,
        5,
        true
      ],
      [
        2,
        6,
        true
      ],
      [
        3,
        7,
        true
      ]
    ],
    "mode": "auto-luminance",
    "near_leading": 8,
    "unclear": 0,
    "half_cycle": {
      "pairs": [
        {
          "pair": [
            0,
            4
          ],
          "iou_best_shift": 0.8178
        },
        {
          "pair": [
            1,
            5
          ],
          "iou_best_shift": 0.8364
        },
        {
          "pair": [
            2,
            6
          ],
          "iou_best_shift": 0.8424
        },
        {
          "pair": [
            3,
            7
          ],
          "iou_best_shift": 0.7963
        }
      ],
      "adjacent_iou_median": 0.7832,
      "half_cycle_iou_median": 0.8271
    },
    "fix": "regenerate frames 4-7 with NEAR and FAR swapped (attach frames 0-3 and the guide)"
  },
  {
    "id": "torso_drift",
    "status": "warn",
    "value": 4.09,
    "threshold": 2.0,
    "method": "trunk",
    "median_x": 79.7,
    "note": "range of the torso x in game px; scale_frames --root-lock torso-x removes it"
  }
]
```
