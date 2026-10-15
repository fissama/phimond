# P12 Stage 4 — Ma trận NPC nguồn APK 3.2 (44 slot, vai trò gốc chỉ là suy đoán; roster thiết kế: P12-S4-npc-roster.md)

Mỗi dòng là một object trong container `AllNpc` có collider + script. **Vai trò là suy đoán từ tên object**, không đọc được từ script (IL2CPP, không có type tree). Tọa độ là đơn vị thế giới Unity (x,y), đã gộp hierarchy. `active=false` = đối tượng ẩn trong scene, script bật sau.

Sprite là tên sprite trong APK, chưa ánh xạ sang asset game.


## summoning_hall_main_hall  (4 NPC)

Scene có 4 nhóm `poke*` ở (-3.15, -0.22), mỗi nhóm 2 sprite: `pokeLinhThe` (linh thể), `pokeThu` (thú), `pokeThucVat` (thực vật), `pokeSau` (sâu/côn trùng) → bản gốc có **4** lựa chọn pet khởi đầu; thiết kế Phimond đã chốt 3 (Thực vật / Côn trùng / Thú), bỏ Linh thể.

| Object | Vai trò (suy đoán) | Sprite | Vị trí (x,y) | Active |
|---|---|---|---|---|
| `Npc` | chưa rõ | 1 | -5.32, 0.36 | ẩn |
| `Npc (2)` | chưa rõ | 1 | -5.32, 0.36 | ẩn |
| `Npc (1)` | chưa rõ | Dự án mới (29) | -5.32, 0.36 | ẩn |
| `Npc (3)` | chưa rõ | 1 | -5.32, 0.36 | ẩn |

## city_square  (7 NPC)

| Object | Vai trò (suy đoán) | Sprite | Vị trí (x,y) | Active |
|---|---|---|---|---|
| `thaythuoc (3)` | thầy thuốc (hồi máu?) | 71 | -11.23, 0.32 | có |
| `thaythuoc (5)` | thầy thuốc (hồi máu?) | 71 | -9.51, 0.04 | có |
| `thaythuoc (2)` | thầy thuốc (hồi máu?) | 59 | -8.23, -2.79 | có |
| `TTTD (3)` | chưa rõ (viết tắt) | 69 | -6.12, -0.06 | có |
| `TTTD (2)` | chưa rõ (viết tắt) | 78 | -2.44, -2.09 | có |
| `thaythuoc` | thầy thuốc (hồi máu?) | 6 | 0.12, 0.6 | có |
| `TTTD` | chưa rõ (viết tắt) | 26 | 6.28, -1.66 | có |

## city_market  (3 NPC)

| Object | Vai trò (suy đoán) | Sprite | Vị trí (x,y) | Active |
|---|---|---|---|---|
| `Npc (1)` | chưa rõ | 5 | 65.31, 0.05 | có |
| `Npc (2)` | chưa rõ | 8 | 68.39, 0.05 | có |
| `Npc (3)` | chưa rõ | 7 | 80.49, 0.28 | có |

## city_palace_gate  (1 NPC)

| Object | Vai trò (suy đoán) | Sprite | Vị trí (x,y) | Active |
|---|---|---|---|---|
| `guild (1)` | bang hội | 79 | 30.91, -0.16 | có |

## city_royal_palace  (3 NPC)

| Object | Vai trò (suy đoán) | Sprite | Vị trí (x,y) | Active |
|---|---|---|---|---|
| `TTTD (1)` | chưa rõ (viết tắt) | 77 | 35.45, 17.8 | có |
| `guild` | bang hội | 83 | 40.51, 17.44 | có |
| `thaythuoc (4)` | thầy thuốc (hồi máu?) | 71 | 43.75, 17.56 | có |

## city_activity_hall  (1 NPC)

| Object | Vai trò (suy đoán) | Sprite | Vị trí (x,y) | Active |
|---|---|---|---|---|
| `guild (2)` | bang hội | 79 | -0.53, 16.07 | có |

## city_pet_room  (4 NPC)

| Object | Vai trò (suy đoán) | Sprite | Vị trí (x,y) | Active |
|---|---|---|---|---|
| `Ong Poke` | Ông Poke (nhân vật) | 59 | -5.63, -14.05 | có |
| `Shop` | cửa hàng | 5 | -2.34, -14.03 | có |
| `LamMoi` | "làm mới" (chưa rõ) | 70 | 0.82, -14.06 | có |
| `ChucPhuc` | chúc phúc | 215 | 3.61, -14.06 | có |

## city_farm  (2 NPC)

| Object | Vai trò (suy đoán) | Sprite | Vị trí (x,y) | Active |
|---|---|---|---|---|
| `QuanLy` | quản lý (nông trại?) | 1 | -3.51, -25.71 | có |
| `Npc` | chưa rõ | 7 | -0.8, -25.77 | có |

## city_deathmatch_arena  (1 NPC)

| Object | Vai trò (suy đoán) | Sprite | Vị trí (x,y) | Active |
|---|---|---|---|---|
| `thaythuoc (1)` | thầy thuốc (hồi máu?) | 6 | 39.65, 39.66 | có |

## emerald_forest_main_woods  (4 NPC)

| Object | Vai trò (suy đoán) | Sprite | Vị trí (x,y) | Active |
|---|---|---|---|---|
| `Lisa` | chưa rõ | 68 | 4.78, 1.59 | có |
| `Npc` | chưa rõ | 6 | 8.39, 1.36 | có |
| `Skill` | kỹ năng | 7 | 11.95, 1.39 | có |
| `Shop` | cửa hàng | 5 | 15.13, 1.46 | có |

## emerald_forest_deep_woods  (1 NPC)

| Object | Vai trò (suy đoán) | Sprite | Vị trí (x,y) | Active |
|---|---|---|---|---|
| `Vesa` | chưa rõ | 62 | 45.18, 1.41 | có |

## treasure_beach_fishermen_beach  (4 NPC)

| Object | Vai trò (suy đoán) | Sprite | Vị trí (x,y) | Active |
|---|---|---|---|---|
| `Skill` | kỹ năng | 7 | -2.95, 1.91 | có |
| `Walter (1)` | chưa rõ | 6 | -0.02, 1.82 | có |
| `Gustin` | chưa rõ | 3 | 2.7, 1.8 | có |
| `Shop` | cửa hàng | 5 | 4.94, 1.66 | có |

## treasure_beach_east_beach  (1 NPC)

| Object | Vai trò (suy đoán) | Sprite | Vị trí (x,y) | Active |
|---|---|---|---|---|
| `Saja` | chưa rõ | 61 | 40.18, 1.94 | có |

## treasure_beach_deep_sea  (1 NPC)

| Object | Vai trò (suy đoán) | Sprite | Vị trí (x,y) | Active |
|---|---|---|---|---|
| `Walter` | chưa rõ | 77 | -9.92, -13.68 | có |

## treasure_beach_west_beach  (1 NPC)

| Object | Vai trò (suy đoán) | Sprite | Vị trí (x,y) | Active |
|---|---|---|---|---|
| `Ithaqua` | chưa rõ | 58 | -27.06, 1.47 | có |

## treasure_beach_prosperity_island  (0 NPC)

(không có NPC)


## middle_corridor_main_hall  (6 NPC)

| Object | Vai trò (suy đoán) | Sprite | Vị trí (x,y) | Active |
|---|---|---|---|---|
| `npc (1)` | chưa rõ | 7 | -5.15, 1.67 | có |
| `npc` | chưa rõ | 8 | -4.21, -1.96 | có |
| `Npc (1)` | chưa rõ | 5 | -2.39, 1.81 | có |
| `Logan` | chưa rõ | 68 | -0.23, -1.96 | có |
| `Npc` | chưa rõ | 6 | 0.71, 1.81 | có |
| `TTTD` | chưa rõ (viết tắt) | 26 | 3.05, 1.87 | có |
