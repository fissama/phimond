import { session } from '../state/app.ts';
import { Login } from './Login.tsx';
import { World } from './World.tsx';

export function App() {
  const ch = session.character.value;
  return ch ? <World /> : <Login />;
}
