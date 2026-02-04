import type { NextConfig } from "next";

const nextConfig: NextConfig = {
    images: {
        qualities: [75, 100],
    },
    allowedDevOrigins: ["127.0.0.1", "localhost"],
};

export default nextConfig;
