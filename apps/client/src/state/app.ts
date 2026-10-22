import { Session } from '../net/session.ts';
import { BrowserWire, apiBaseFromEnv } from '../net/transport.ts';

/** Một phiên cho toàn ứng dụng. */
export const session = new Session(new BrowserWire(apiBaseFromEnv()));
