import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = {
  title: "Phimond — The Field Journal",
  description:
    "A living field journal of creatures, kinship, and the world of Phimond.",
};
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
