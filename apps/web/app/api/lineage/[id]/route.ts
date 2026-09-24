import { upstream } from "@/lib/server";
export async function GET(
  _req: Request,
  { params }: { params: Promise<{ id: string }> },
) {
  const { id } = await params;
  return upstream(`/api/lineage/${encodeURIComponent(id)}`, {}, true);
}
