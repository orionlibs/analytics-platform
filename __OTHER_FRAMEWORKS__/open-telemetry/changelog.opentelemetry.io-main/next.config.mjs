/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    // Don't run ESLint during builds
    ignoreDuringBuilds: true
  }
};

export default nextConfig;
