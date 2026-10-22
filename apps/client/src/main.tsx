import { render } from 'preact';
// style.css trước: lớp da UI (skin.ts) được chèn sau để đè lên kiểu mặc định.
import './ui/style.css';
import { App } from './ui/App.tsx';

render(<App />, document.getElementById('app')!);
