import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";
export const SESSION = "phimond_session";
export function sameOrigin(req: NextRequest) {
  const origin = req.headers.get("origin");
  return origin === req.nextUrl.origin;
}
export async function upstream(
  path: string,
  init: RequestInit = {},
  authenticated = false,
) {
  const token = authenticated
    ? (await cookies()).get(SESSION)?.value
    : undefined;
  if (authenticated && !token)
    return NextResponse.json(
      { error: "Sign in to open your field journal." },
      { status: 401 },
    );
  try {
    const headers = new Headers(init.headers);
    headers.set("Content-Type", "application/json");
    if (token) headers.set("Authorization", `Bearer ${token}`);
    const response = await fetch(
      `${process.env.GAME_API_URL || "http://127.0.0.1:8090"}${path}`,
      {
        ...init,
        headers,
        cache: "no-store",
        signal: AbortSignal.timeout(8000),
      },
    );
    const data = await response.json();
    return NextResponse.json(data, {
      status: response.status,
      headers: { "Cache-Control": "no-store" },
    });
  } catch {
    return NextResponse.json(
      {
        error:
          "The field station is offline. Start the game server and try again.",
      },
      { status: 503 },
    );
  }
}
