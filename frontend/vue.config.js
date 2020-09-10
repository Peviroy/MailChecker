const path = require('path');

module.exports = {
  transpileDependencies: ['vuetify'],

  outputDir: path.resolve(__dirname, '../dist'),

  pluginOptions: {
    i18n: {
      locale: 'en',
      fallbackLocale: 'en',
      localeDir: 'locales',
      enableInSFC: false
    }
  }
};
