import Vue from "vue";
import Router from "vue-router";
import Load from "src/components/Load/Load";
import Resources from "src/components/Resources/Resources";

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: "/",
      name: "Загрузить фото",
      component: Load
    },
    {
      path: "/resources",
      name: "Ресурсы",
      component: Resources
    }
  ]
});
