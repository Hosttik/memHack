export default {
  changeTheme: (state, newThemeName) => {
    state.theme = newThemeName;
  },
  changeLoaderStatus: (state, status) => {
    state.loader = status;
  },
};
