import { upstream } from "@/lib/server";
export async function GET() {
  return upstream("/api/character", {}, true);
}
