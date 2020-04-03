<template>
  <div id="app">
    <v-app>
      <v-toolbar dark tabs flat color="primary">
        <v-toolbar-side-icon @click="toggleeMenu"></v-toolbar-side-icon>
        <v-toolbar-title>{{ $router.currentRoute.name }} </v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-content>
        <v-navigation-drawer
          temporary
          v-model="showMenu"
          height="100%"
          absolute
        >
          <v-list class="pt-0" dense>
            <v-divider></v-divider>

            <v-list-tile
              v-for="item in getMenuItems()"
              :key="item.title"
              @click=""
              :to="item.href"
            >
              <v-list-tile-action>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-tile-action>

              <v-list-tile-content>
                <v-list-tile-title>{{ item.title }}</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>
        </v-navigation-drawer>
        <v-container grid-list-md text-xs-center @click="hideMenu">
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
            &copy;2019 — <strong>BUGuvix</strong>
          </v-card-text>
        </v-card>
      </v-footer>
    </v-app>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      showMenu: false
    };
  },
  methods: {
    toggleeMenu() {
      this.showMenu = !this.showMenu;
    },
    hideMenu() {
      this.showMenu = false;
    },
    getMenuItems() {
      return [
        {
          title: "Главная",
          icon: "home",
          href: "/"
        },
        {
          title: "Ресурсы",
          icon: "view_list",
          href: "/resources"
        }
      ];
    }
  }
};
</script>

<style scoped></style>
