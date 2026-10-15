import type { JSX } from 'preact';
const P = (d: string) => <svg viewBox="0 0 24 24" aria-hidden="true"><path d={d} /></svg>;
export const ICONS: Record<string, JSX.Element> = {
  pets: P('M5 11c-1.4 0-2.5-1.3-2.5-3S3.6 5 5 5s2.5 1.3 2.5 3S6.4 11 5 11zm14 0c-1.4 0-2.5-1.3-2.5-3S17.6 5 19 5s2.5 1.3 2.5 3-1.1 3-2.5 3zM9.5 8C8.1 8 7 6.7 7 5s1.1-3 2.5-3S12 3.3 12 5 10.9 8 9.5 8zm5 0c-1.4 0-2.5-1.3-2.5-3s1.1-3 2.5-3S17 3.3 17 5s-1.1 3-2.5 3zM12 12c3.5 0 6 3.2 6 6 0 2-1.6 3-3.2 3-1.2 0-1.8-.7-2.8-.7s-1.6.7-2.8.7C7.6 21 6 20 6 18c0-2.8 2.5-6 6-6z'),
  quest: P('M6 3h9l4 4v14H6zM15 3v4h4M9 12h7M9 16h7'),
  menu: P('M4 6h16M4 12h16M4 18h16'),
  bag: P('M6 8h12l1 13H5zM9 8V6a3 3 0 0 1 6 0v2'),
  map: P('M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2zM9 4v14M15 6v14'),
  shop: P('M4 9l1.5-5h13L20 9M4 9v11h16V9M4 9c0 2 3 2 4 0 1 2 4 2 4 0 1 2 4 2 4 0 1 2 4 2 4 0'),
  ranch: P('M3 11l9-7 9 7M5 10v10h14V10M10 20v-6h4v6'),
  gear: P('M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM19 12l2-1.5-2-3.5-2.4.8a7 7 0 0 0-1.6-.9L14.5 4h-5L9 6.9a7 7 0 0 0-1.6.9L5 7 3 10.5 5 12l-2 1.5L5 17l2.4-.8c.5.4 1 .7 1.6.9L9.5 20h5l.5-2.9c.6-.2 1.1-.5 1.6-.9L19 17l2-3.5z'),
  world: P('M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18'),
  sword: P('M14 4l6-1-1 6-9 9-3-3zM6 15l-3 3 3 3 3-3M4 20l-1 1'),
  skill: P('M12 3l2.5 6 6.5.5-5 4.3 1.6 6.4L12 16.8 6.4 20.2 8 13.8 3 9.5l6.5-.5z'),
  potion: P('M9 3h6M10 3v5l-5 10a2 2 0 0 0 1.8 3h10.4a2 2 0 0 0 1.8-3l-5-10V3M8 15h8'),
  shield: P('M12 3l8 3v6c0 4.5-3.2 8-8 9-4.8-1-8-4.5-8-9V6z'),
  run: P('M13 4a1.5 1.5 0 1 0 0 .1M8 21l3-6-2-3 3-3 3 3h4M7 12l2-4 4-1'),
  auto: P('M20 12a8 8 0 1 1-2.3-5.7M20 4v5h-5'),
  seal: P('M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM12 8v8M8 12h8'),
};
export const Icon = ({ n }: { n: string }) => ICONS[n] ?? null;
export const Arrow = ({ rot }: { rot: number }) => (
  <svg viewBox="0 0 24 24" style={{ transform: `rotate(${rot}deg)` }} aria-hidden="true"><path d="M12 3l9 14H3z" /></svg>
);
