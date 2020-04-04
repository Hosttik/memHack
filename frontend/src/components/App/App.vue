<template>
    <div id="app">
        <v-app>
            <v-toolbar dark tabs flat color="primary">
                <v-spacer></v-spacer>

                <v-btn v-for="item in getMenuItems()"
                       outline
                       class="ma-2"
                       :key="item.title"
                       :to="item.href"
                       style=""
                       outlined>
                    <v-icon left>{{ item.icon }}</v-icon>
                    {{ item.title }}
                </v-btn>

                <v-spacer></v-spacer>
            </v-toolbar>
            <v-content>
                <v-container fluid grid-list-md text-xs-center>
                    <router-view></router-view>
                </v-container>
            </v-content>
            <v-footer dark height="auto">
                <v-card
                        flat
                        tile
                        width="100%"
                        class="primary white--text text-xs-center"
                >
                    <v-card-text class="white--text">
                        &copy;2020 — <strong>BUGuvix</strong>
                    </v-card-text>
                </v-card>
            </v-footer>
        </v-app>
    </div>
</template>

<script>
  import { apiHost } from 'src/api/api.utils';

  export default {
    name: 'App',
    created: async function () {
      try {
        const res = await apiHost.post('http://google.com', {});
        console.log(res);
      } catch (e) {
        console.log(e);
      }
    },
    data() {
      return {};
    },
    methods: {
      getMenuItems() {
        return [{
          title: 'Главная',
          icon: 'fa-upload',
          href: '/'
        }, {
          title: 'Личный кабинет',
          icon: 'fa-user',
          href: '/account'
        }];
      }
    }
  };
</script>

<style scoped>
</style>
