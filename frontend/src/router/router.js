import Vue from 'vue';
import Router from 'vue-router';
import Home from 'src/components/Home/Home';
import Account from 'src/components/Account/Account';
import Filters from 'src/components/Filters/Filters';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [{
    path: '/',
    name: 'Главная',
    component: Home
  }, {
    path: '/account',
    name: 'Личный кабинет',
    component: Account
  }, {
    path: '/filters',
    name: 'Фильтры',
    component: Filters
  }]
});
