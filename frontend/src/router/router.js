import Vue from 'vue';
import Router from 'vue-router';
import Account from 'src/components/Account/Account';
import Filters from 'src/components/Filters/Filters';
import Load from 'src/components/Load/Load';
import Finish from 'src/components/Finish/Finish';


Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [{
    path: '/',
    name: 'Загрузить фото',
    component: Load
  }, {
    path: '/account',
    name: 'Личный кабинет',
    component: Account
  }, {
    path: '/filters',
    name: 'Фильтры',
    component: Filters
  }, {
    path: '/finish',
    name: 'Результат',
    component: Finish
  }]

});
