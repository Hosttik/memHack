import Vue from "vue";
import Router from "vue-router";
import Home from "src/components/Home/Home";
import Resources from "src/components/Resources/Resources";

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: "/",
      name: "Главная",
      component: Home
    },
    {
      path: "/resources",
      name: "Ресурсы",
      component: Resources
    }
  ]
});
