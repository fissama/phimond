import { render } from 'preact';
import './ui/styles.css';
import { Game } from './game/controller.ts';
import { Session } from './net/session.ts';
import { API_BASE } from './net/config.ts';
import { BrowserTransport, type WireTransport } from './net/transport.ts';
import { LocalTransport, loadEngine } from './net/localTransport.ts';
import { App } from './ui/App.tsx';
import { LoadingScreen } from './ui/Loading.tsx';

async function boot(): Promise<void> {
  const root = document.getElementById('app')!;
  root.textContent = '';
  const local = import.meta.env.VITE_GAME_LOCAL === '1' || new URLSearchParams(location.search).has('local');
  let wire: WireTransport;
  if (local) {
    render(<LoadingScreen label="Đang khởi động máy chủ…" />, root);
    wire = new LocalTransport(await loadEngine());
  } else wire = new BrowserTransport(API_BASE);
  render(<App game={new Game(new Session(wire))} local={local} />, root);
}
void boot();
