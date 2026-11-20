import path from 'node:path';
import { fileURLToPath } from 'node:url';
/** @type {import('next').NextConfig} */

const nextConfig = {
  outputFileTracingRoot: path.dirname(fileURLToPath(import.meta.url)),
  images: {
    remotePatterns: [{ protocol: 'https', hostname: 'a.storyblok.com' }],
  },
};
export default nextConfig;
