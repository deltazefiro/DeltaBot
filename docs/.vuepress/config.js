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

    // 假定是 GitHub. 同时也可以是一个完整的 GitLab URL
    repo: '233a344a455/DeltaBot',

    // 假如文档不是放在仓库的根目录下：
    docsDir: 'docs',
    docsBranch: 'dev',
    editLinks: true,
  }
}
  