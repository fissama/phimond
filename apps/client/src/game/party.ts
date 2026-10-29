import type { Character, Pet } from '@phimond/protocol';

export const MAX_PARTY = 3;

/**
 * Đội hình mang theo (con chính đứng đầu). Server gửi `party`; bản/tài khoản cũ chưa có thì dùng
 * con đang theo rồi các linh thú còn lại theo thứ tự sở hữu (cùng luật `EffectiveParty` ở server).
 */
export function partyOf(ch: Character): Pet[] {
  const alive = ch.pets.filter((p) => !p.retired);
  const byId = new Map(alive.map((p) => [p.id, p]));
  const out: Pet[] = [];
  const add = (p: Pet | undefined) => {
    if (p && !out.includes(p) && out.length < MAX_PARTY) out.push(p);
  };
  add(byId.get(ch.active_pet_id));
  if (ch.party.length) ch.party.forEach((id) => add(byId.get(id)));
  else alive.forEach(add);
  return out;
}
