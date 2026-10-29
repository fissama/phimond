import { petArt, petAtlas, petUrl } from '../render/assets.ts';

/** Ô vuông chân dung linh thú cắt từ atlas nhỏ (khung idle đầu tiên). */
export function PetPortrait({ species, size = 44, bust = false }: { species: string; size?: number; bust?: boolean }) {
  const atlas = petAtlas();
  const art = petArt(species);
  if (!atlas || !art) return <div class="portrait" style={{ width: size, height: size }} />;
  if (bust) {
    // Cắt phần thân trên: lấy khung idle đầu, ô vuông L quanh phần thân thật (bỏ khoảng trống quanh con thú).
    const cell = atlas.cell;
    const w = art.width[0]?.[0] ?? cell * 0.5;
    const h = art.height[0]?.[0] ?? cell * 0.5;
    const feet = art.feet[0]?.[0] ?? 0;
    const L = Math.min(cell, Math.max(w * 1.02, h * 0.8));
    const top = Math.max(0, cell - feet - h - L * 0.04);
    const x0 = Math.min(cell - L, Math.max(0, cell / 2 - L / 2));
    const y0 = Math.min(cell - L, top);
    const k = size / L;
    return (
      <div
        class="portrait"
        style={{
          width: size,
          height: size,
          backgroundImage: `url(${petUrl(art.small)})`,
          backgroundSize: `${cell * atlas.cols * k}px ${cell * atlas.rows * k}px`,
          backgroundPosition: `${-x0 * k}px ${-y0 * k}px`,
        }}
      />
    );
  }
  return (
    <div
      class="portrait"
      style={{
        width: size,
        height: size,
        backgroundImage: `url(${petUrl(art.small)})`,
        backgroundSize: `${size * atlas.cols}px ${size * atlas.rows}px`,
        backgroundPosition: '0 0',
      }}
    />
  );
}

/** Linh thú hoạt họa (CSS steps) cho màn trận đấu. `row`: idle/move/attack/cast/down. */
export function PetAnimated({ species, size, row = 'idle' }: { species: string; size: number; row?: string }) {
  const atlas = petAtlas();
  const art = petArt(species);
  if (!atlas || !art) return <div class="sprite" />;
  const r = Math.max(0, atlas.rowNames.indexOf(row));
  return (
    <div
      class="sprite"
      style={{
        width: size,
        height: size,
        backgroundImage: `url(${petUrl(art.file)})`,
        backgroundSize: `${size * atlas.cols}px ${size * atlas.rows}px`,
        backgroundPositionY: `${-r * size}px`,
        ['--s' as string]: `${size}px`,
        animation: `petframes 0.8s steps(${atlas.cols}) infinite`,
      }}
    />
  );
}
