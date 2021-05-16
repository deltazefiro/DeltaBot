const path = require("path");

module.exports = context => ({
    title: 'DeltaBot Document',
    description: 'DeltaBot文档中心',
    head: [
        ['link', {rel: 'icon', href: '/icon.png'}]
    ],
    base: '/DeltaBot/',
    theme: 'titanium',
    themeConfig: {
        nav: [
            {text: '主页', link: '/'},
            {text: '功能列表', link: '/features'},
            {text: '使用方法', link: '/usage'},
            {text: '部署指南', link: '/setup'}
        ],

        sidebar: [
            '/',
            '/features',
            '/usage',
            '/setup'
        ],

        repo: '233a344a455/DeltaBot',

        docsBranch: 'dev',
        docsDir: 'docs',
        editLinks: true,

        lastUpdated: true,

        nextVersionTitle: 'dev',
        docsDirVersioned: 'archive',
        docsDirPages: 'pages',
    },

    plugins: [
        ["versioning",
            {
                versionedSourceDir: path.resolve(context.sourceDir, "..", "archive"),
                pagesSourceDir: path.resolve(context.sourceDir, "..", "pages"),
                onNewVersion(version, versionDestPath) {
                    console.log(`Created version ${version} in ${versionDestPath}`);
                }
            }
        ],
    ]
});