import antfu from "@antfu/eslint-config";
import nextPlugin from "@next/eslint-plugin-next";
import boundaries from "eslint-plugin-boundaries";

const FSD_LAYERS = [
    "app",
    "pages",
    "widgets",
    "features",
    "entities",
    "shared",
];

export default antfu(
    {
        // Форматирование
        stylistic: {
            indent: 4,
            quotes: "double",
            semi: true,
        },

        // TypeScript
        typescript: {
            tsconfigPath: "./tsconfig.json",
        },

        // React
        react: true,

        // Next.js — игнорируем сгенерированное
        ignores: [".next/**", "out/**", "build/**", "next-env.d.ts"],
    },

    // Next.js правила (@next/next/*)
    {
        plugins: {
            "@next/next": nextPlugin,
        },
        rules: {
            ...nextPlugin.configs.recommended.rules,
            ...nextPlugin.configs["core-web-vitals"].rules,
        },
    },

    // Общие переопределения
    {
        rules: {
            // Next.js использует default export для страниц/layout
            "import/no-default-export": "off",
        },
    },

    // TypeScript-специфичные правила (только для .ts/.tsx)
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
            "ts/no-unsafe-assignment": "off",
            "ts/no-unsafe-call": "off",
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
            "boundaries/elements": FSD_LAYERS.map((layer) => ({
                type: layer,
                pattern: `src/${layer}/*`,
                capture: ["slice"],
            })),
            "boundaries/ignore": ["src/**/*.test.*", "src/**/*.spec.*"],
        },
        rules: {
            "boundaries/element-types": [
                "error",
                {
                    default: "disallow",
                    rules: [
                        { from: "app", allow: FSD_LAYERS },
                        {
                            from: "pages",
                            allow: [
                                "widgets",
                                "features",
                                "entities",
                                "shared",
                            ],
                        },
                        {
                            from: "widgets",
                            allow: ["features", "entities", "shared"],
                        },
                        { from: "features", allow: ["entities", "shared"] },
                        { from: "entities", allow: ["entities", "shared"] },
                        { from: "shared", allow: ["shared"] },
                    ],
                },
            ],
        },
    },
);
