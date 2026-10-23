/** Đuổi theo đích theo hàm mũ, độc lập nhịp khung hình: bước ô và nhịp dt thay đổi không còn làm hình giật cục. */
export function follow(cur: number, target: number, dt: number, rate: number): number {
  return cur + (target - cur) * (1 - Math.exp(-dt * rate));
}

/** Tiến về đích với mức đổi tối đa mỗi lần gọi. */
export function approach(cur: number, target: number, maxDelta: number): number {
  return cur < target ? Math.min(target, cur + maxDelta) : Math.max(target, cur - maxDelta);
}

/**
 * Tốc độ của người đi bộ: tăng dần lúc xuất phát, giảm dần khi gần đích (`remaining` là số ô còn lại),
 * thay vì đang đứng bỗng đi hết tốc rồi khựng lại khi tới nơi — nguyên nhân cảm giác "lướt".
 */
export function walkSpeed(cur: number, top: number, remaining: number, dt: number, accel = 5): number {
  const brake = Math.sqrt(Math.max(0, 2 * accel * remaining)); // tốc độ tối đa còn dừng kịp
  return approach(cur, Math.max(0.35, Math.min(top, brake)), accel * dt);
}
