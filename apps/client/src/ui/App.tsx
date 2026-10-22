import { useEffect, useState } from 'preact/hooks';
import { loadDictionary } from '../game/content.ts';
import { loadManifests } from '../render/assets.ts';
import { session } from '../state/app.ts';
import { Game } from './Game.tsx';
import { Login } from './Login.tsx';

export function App() {
  const [ready, setReady] = useState(false);
  useEffect(() => {
    void Promise.all([loadDictionary(), loadManifests()]).finally(() => setReady(true));
  }, []);
  if (!ready) return <div class="loading">Phimond</div>;
  return session.character.value ? <Game /> : <Login />;
}
