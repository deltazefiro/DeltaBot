module.exports = {
  base: '/DeltaBot/',
  themeConfig: {
    nav: [
      { text: '主页', link: '/' },
      { text: '功能', link: '/features' },
      { text: '使用方法', link: '/usage' },
      { text: '部署', link: '/setup' }
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

    themeConfig: {
        lastUpdated: 'Last Updated'
    }
  }
}
  