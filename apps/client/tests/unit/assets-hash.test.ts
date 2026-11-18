import { describe, expect, it } from 'vitest';
import { hashedName, rewriteCssUrls } from '../../vite-hash-public.ts';
import { unhashedUrl } from '../../src/assetUrl.ts';

// AD1: tên băm ổn định theo nội dung, CSS trỏ đúng tên băm, và lùi được về tên gốc.
describe('băm tên asset', () => {
  it('cùng nội dung → cùng tên; khác nội dung → khác tên; giữ hậu tố idle/run', () => {
    const a = hashedName('hd2d/player-male.idle.png', Buffer.from('a'));
    expect(a).toMatch(/^hd2d\/player-male\.idle\.[0-9a-f]{10}\.png$/);
    expect(hashedName('hd2d/player-male.idle.png', Buffer.from('a'))).toBe(a);
    expect(hashedName('hd2d/player-male.idle.png', Buffer.from('b'))).not.toBe(a);
  });

  it('CSS: chỉ thay url có trong manifest, giữ dấu nháy', () => {
    const m = { 'ui/ui-minimap.png': 'ui/ui-minimap.0123456789.png' };
    expect(rewriteCssUrls("a{border-image:url('../ui/ui-minimap.png') 52}", m)).toBe("a{border-image:url('../ui/ui-minimap.0123456789.png') 52}");
    expect(rewriteCssUrls('b{background:url(../ui/other.png)}', m)).toBe('b{background:url(../ui/other.png)}');
  });

  it('lùi về tên gốc', () => {
    expect(unhashedUrl('./hd2d/bush-01.3fa9c1d2e4.png')).toBe('./hd2d/bush-01.png');
    expect(unhashedUrl('./hd2d/player-male.idle.3fa9c1d2e4.png')).toBe('./hd2d/player-male.idle.png');
    expect(unhashedUrl('./hd2d/bush-01.png')).toBe('./hd2d/bush-01.png');
  });
});
