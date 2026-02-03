import type { NextConfig } from "next";

const nextConfig: NextConfig = {
    images: {
        qualities: [75, 100],
    },
    allowedDevOrigins: ["http://127.0.0.1:3000"],
};

export default nextConfig;
