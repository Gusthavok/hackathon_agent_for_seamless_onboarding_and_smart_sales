/** @type {import('next').NextConfig} */

const nextConfig = {
  images: {
    domains: ['localhost', 'm.media-amazon.com'], // Autoriser localhost
  },
  experimental: {
    appDir: true,  // Active l'App Directory (nécessaire pour les routes dans le dossier `app/`)
  },
};

export default nextConfig;