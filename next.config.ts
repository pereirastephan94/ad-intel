import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  // Allow longer serverless function timeout for Claude analysis
  experimental: {
    serverActions: { bodySizeLimit: '2mb' }
  }
}

export default nextConfig
