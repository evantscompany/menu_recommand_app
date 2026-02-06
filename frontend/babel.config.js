// frontend/babel.config.js
module.exports = function(api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: [
      'react-native-reanimated/plugin', // <-- 이 한 줄이 애니메이션의 열쇠입니다!
    ],
  };
};