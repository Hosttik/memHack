<template> </template>

<script>
import { mapMutations } from "vuex";
import changeThemeColors from "src/helpers/changeThemeColors";
export default {
  name: "Home",
  data() {
    return {};
  },
  methods: {
    ...mapMutations(["changeTheme"]),
    setTheme(name) {
      const color = this.themeBySeason[name];
      this.changeTheme(color);
      changeThemeColors(this.$vuetify.theme, color);
    }
  }
};
</script>

<style scoped></style>
