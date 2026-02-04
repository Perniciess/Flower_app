import antfu from "@antfu/eslint-config";
import nextPlugin from "@next/eslint-plugin-next";
import boundaries from "eslint-plugin-boundaries";

const FSD_LAYERS = ["app", "pages", "widgets", "features", "entities", "shared"];

export default antfu(
    {
        // Formatting
        stylistic: {
            indent: 4,
            quotes: "double",
            semi: true,
        },

        // TypeScript (strict)
        typescript: {
            tsconfigPath: "./tsconfig.json",
        },

        react: true,

        ignores: [".next/**", "out/**", "build/**", "next-env.d.ts"],
    },

    // Next.js rules
    {
        plugins: {
            "@next/next": nextPlugin,
        },
        rules: {
            ...nextPlugin.configs.recommended.rules,
            ...nextPlugin.configs["core-web-vitals"].rules,
        },
    },

    // Project overrides
    {
        rules: {
            "import/no-default-export": "off",
        },
    },

    // TS-only stricter rules
    {
        files: ["**/*.ts", "**/*.tsx"],
        rules: {
            "ts/consistent-type-imports": [
                "error",
                {
                    prefer: "type-imports",
                    fixStyle: "inline-type-imports",
                },
            ],
            "ts/no-import-type-side-effects": "error",
            "ts/no-unsafe-assignment": "error",
            "ts/no-unsafe-call": "error",
            "ts/no-unsafe-member-access": "error",
            "ts/no-unsafe-return": "error",
            "ts/no-unused-vars": [
                "error",
                {
                    argsIgnorePattern: "^_",
                    varsIgnorePattern: "^_",
                },
            ],
        },
    },

    // FSD boundaries
    {
        files: ["src/**/*.ts", "src/**/*.tsx"],
        plugins: { boundaries },
        settings: {
            "boundaries/elements": FSD_LAYERS.map(layer => ({
                type: layer,
                pattern: `src/${layer}`,
                mode: "folder",
                capture: ["slice"],
            })),
            "boundaries/ignore": ["src/**/*.test.*", "src/**/*.spec.*"],
        },
        rules: {
            "boundaries/element-types": [
                "error",
                {
                    default: "disallow",
                    // eslint-disable-next-line no-template-curly-in-string -- boundaries plugin placeholder syntax
                    message: "${from.type} is not allowed to import ${to.type}",
                    rules: [
                        { from: "app", allow: FSD_LAYERS },
                        { from: "pages", allow: ["widgets", "features", "entities", "shared"] },
                        { from: "widgets", allow: ["features", "entities", "shared"] },
                        { from: "features", allow: ["entities", "shared"] },
                        { from: "entities", allow: ["entities", "shared"] },
                        { from: "shared", allow: ["shared"] },
                    ],
                },
            ],
            "boundaries/entry-point": [
                "error",
                {
                    default: "disallow",
                    rules: [
                        { target: ["shared"], allow: "**" },
                        { target: ["app", "pages", "widgets", "features", "entities"], allow: "index.ts" },
                    ],
                },
            ],
        },
    },
);
