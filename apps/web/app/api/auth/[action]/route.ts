import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { SESSION, sameOrigin, upstream } from "@/lib/server";
export async function POST(
  req: NextRequest,
  { params }: { params: Promise<{ action: string }> },
) {
  if (!sameOrigin(req))
    return NextResponse.json(
      { error: "Request origin rejected." },
      { status: 403 },
    );
  const { action } = await params;
  if (!["register", "login", "logout"].includes(action))
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  if (action === "logout") {
    const result = await upstream("/api/logout", { method: "POST" }, true);
    (await cookies()).delete(SESSION);
    return result;
  }
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Invalid request." }, { status: 400 });
  }
  if (
    !body ||
    typeof body !== "object" ||
    !("username" in body) ||
    !("password" in body) ||
    typeof body.username !== "string" ||
    typeof body.password !== "string" ||
    !/^[A-Za-z0-9_]{3,24}$/.test(body.username) ||
    new TextEncoder().encode(body.password).length < 10 ||
    new TextEncoder().encode(body.password).length > 72
  )
    return NextResponse.json(
      {
        error:
          "Use 3–24 letters, digits, or underscores for your keeper name and a 10–72 byte password.",
      },
      { status: 400 },
    );
  const result = await upstream(`/api/${action}`, {
    method: "POST",
    body: JSON.stringify({ username: body.username, password: body.password }),
  });
  const data = await result.json();
  if (!result.ok) return NextResponse.json(data, { status: result.status });
  if (typeof data.token !== "string")
    return NextResponse.json(
      { error: "The station returned an invalid session." },
      { status: 502 },
    );
  (await cookies()).set(SESSION, data.token, {
    httpOnly: true,
    sameSite: "strict",
    secure: process.env.NODE_ENV === "production",
    path: "/",
    maxAge: 60 * 60 * 24 * 7,
  });
  return NextResponse.json(
    { character_id: data.character_id },
    { headers: { "Cache-Control": "no-store" } },
  );
}
