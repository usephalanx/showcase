/**
 * Babel configuration for the Expo TodoApp project.
 *
 * Uses the babel-preset-expo preset which includes all necessary
 * transformations for React Native and Expo.
 *
 * @param {object} api - Babel API object.
 * @returns {object} Babel configuration.
 */
module.exports = function (api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
  };
};
