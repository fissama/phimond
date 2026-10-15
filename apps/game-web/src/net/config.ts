// Địa chỉ server. Dev: server Go ở 127.0.0.1:8090 (cần GAME_CORS_ORIGINS + GAME_ALLOWED_ORIGINS có origin của Vite).
export const API_BASE: string = (import.meta.env.VITE_GAME_API_URL as string | undefined)?.replace(/\/$/, '') ?? 'http://127.0.0.1:8090';
export const WS_URL: string = API_BASE.replace(/^https:/, 'wss:').replace(/^http:/, 'ws:') + '/ws';
