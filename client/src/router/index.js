import Vue from 'vue';
import Router from 'vue-router';
import Pokemons from '../components/Pokemons.vue';
import Ping from '../components/Ping.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Pokemons',
      component: Pokemons,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
});
