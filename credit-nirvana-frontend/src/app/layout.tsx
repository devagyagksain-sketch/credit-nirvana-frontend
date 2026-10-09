import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "CreditNirvana - Debt Collections",
  description: "AI-native debt collections and recovery platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="font-sans antialiased bg-gray-50 text-slate-900">
        {children}
      </body>
    </html>
  );
}
