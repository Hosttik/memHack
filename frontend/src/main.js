import Vue from "vue";
import App from "src/components/App/App";
import router from "src/router/router";
import store from "src/store/store";
import Vuetify from "vuetify";
import "vuetify/dist/vuetify.min.css";
import colors from "vuetify/es5/util/colors";

Vue.use(Vuetify,{
  theme: {
    primary: colors[store.state.theme].lighten1,
    secondary: colors[store.state.theme].darken1,
    accent: colors[store.state.theme].accent1
  }
});

new Vue({
  el: "#app",
  router,
  store,
  template: "<App/>",
  components: { App }
});
