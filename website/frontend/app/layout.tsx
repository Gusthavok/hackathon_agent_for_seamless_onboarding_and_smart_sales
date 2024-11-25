"use client";

import './globals.css';
import { Inter } from 'next/font/google';
import { usePathname } from 'next/navigation';
import ChatbotInterface from '@/components/ChatbotInterface';
import { CartProvider } from '@/contexts/CartContext';

const inter = Inter({ subsets: ['latin'] });

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  if (pathname === '/login') {
    return <html lang='fr'>
              <body>
                {children}
              </body>
            </html>;
  }

  return (
    <html lang="fr">
      <body
        className={`${inter.className} min-h-screen bg-background font-sans antialiased`}
      >
        <CartProvider>
          <div className="flex h-screen overflow-hidden">
            <div className="flex-grow overflow-auto">{children}</div>
            <div className="w-2/3 min-w-[300px] border-l border-gray-200 hidden md:block">
              <ChatbotInterface />
            </div>
          </div>
        </CartProvider>
      </body>
    </html>
  );
}
