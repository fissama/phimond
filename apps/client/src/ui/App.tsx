import { useEffect, useState } from 'preact/hooks';
import { loadDictionary } from '../game/content.ts';
import { loadManifests } from '../render/assets.ts';
import { session } from '../state/app.ts';
import { CreateCharacter, SlotSelect } from './CharacterSelect.tsx';
import { Game } from './Game.tsx';
import { Login } from './Login.tsx';
import { installSkin, loadUiManifest, uiUrl } from './skin.ts';

installSkin();

export function App() {
  const [ready, setReady] = useState(false);
  useEffect(() => {
    void Promise.all([loadDictionary(), loadManifests(), loadUiManifest()]).finally(() => setReady(true));
  }, []);
  if (!ready)
    return (
      <div class="loading">
        <img src={uiUrl('logo-badge')} alt="Phimond" style={{ width: 120, imageRendering: 'pixelated' }} />
      </div>
    );
  const ch = session.character.value;
  if (!ch) return session.slots.value ? <SlotSelect /> : <Login />;
  // Ô mới chưa đặt tên/giới tính: tạo nhân vật trước khi vào thế giới.
  return ch.draft ? <CreateCharacter /> : <Game key={ch.id} />;
}
