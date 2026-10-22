import { petArt, petAtlas, petUrl } from '../render/assets.ts';

/** Ô vuông chân dung linh thú cắt từ atlas nhỏ (khung idle đầu tiên). */
export function PetPortrait({ species, size = 44 }: { species: string; size?: number }) {
  const atlas = petAtlas();
  const art = petArt(species);
  if (!atlas || !art) return <div class="portrait" style={{ width: size, height: size }} />;
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
