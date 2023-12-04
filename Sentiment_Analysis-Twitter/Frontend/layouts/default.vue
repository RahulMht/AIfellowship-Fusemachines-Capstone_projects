<template>
  <v-app dark>
    <v-navigation-drawer
      v-model="drawer"
      :mini-variant="miniVariant"
      :clipped="clipped"
      fixed
      app
    >
      <v-list>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title"/>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
      :clipped-left="clipped"
      fixed
      app
    >
      <v-hover v-slot="{hover}">
        <v-sheet color="transparent" fluid rounded="pill">
          <!--      Hide Drawer Button-->
          <v-app-bar-nav-icon x-small @click.stop="drawer = !drawer"/>
          <v-btn small v-if="hover"
            icon
            @click.stop="miniVariant = !miniVariant"
          >
            <v-icon small>fa-solid fa-{{ `chevron-${miniVariant ? 'right' : 'left'}` }}</v-icon>
          </v-btn>
          <v-btn small  v-if="hover"
            icon
            @click.stop="clipped = !clipped"
          >
            <v-icon small>fa-solid fa-window-maximize</v-icon>
          </v-btn>
          <v-btn small v-if="hover"
            icon
            @click.stop="fixed = !fixed"
          >
            <v-icon small>fa-solid fa-window-minimize</v-icon>
          </v-btn>
        </v-sheet>
      </v-hover>
      <v-toolbar-title class="ml-6"><h4> <v-icon left>fa-brands fa-twitter</v-icon>{{title}}</h4></v-toolbar-title>
      <v-spacer/>
      <v-btn
        icon
        @click.stop="rightDrawer = !rightDrawer"
      >
        <v-icon>fa-solid fa-ellipsis-vertical</v-icon>
      </v-btn>
    </v-app-bar>
    <v-main>
      <v-container fluid>
        <Nuxt/>
      </v-container>
    </v-main>
    <v-navigation-drawer
      v-model="rightDrawer"
      :right="right"
      temporary
      fixed
    >
      <v-list>
        <v-list-item>
          <v-list-item-action>
            <v-icon>
              {{ themeSwitch ? 'fa-solid fa-moon' : 'fa-solid fa-sun' }}
            </v-icon>
          </v-list-item-action>
          <v-list-item-title>Switch Theme</v-list-item-title>
          <v-switch
            v-model="themeSwitch"
          ></v-switch>
        </v-list-item>
        <v-list-item to="/settings">
          <v-list-item-action>
            <v-icon>
              fa-solid fa-gear
            </v-icon>
          </v-list-item-action>
          <v-list-item-title>Settings</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-footer
      :absolute="!fixed"
      app
    >
      <span>M. Tech. AI | Kathmandu University &copy; {{ new Date().getFullYear() }}</span>
      <v-spacer></v-spacer>
      <span>Developed By: Ajeeb Rimal</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'DefaultLayout',
  data() {
    return {
      themeSwitch: false,
      clipped: true,
      drawer: false,
      fixed: false,
      items: [
        {
          icon: 'fa-solid fa-gauge',
          title: 'Dashboard',
          to: '/'
        },
        {
          icon: 'fa-solid fa-microchip',
          title: 'Training',
          to: '/train-classifier'
        }
      ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: 'Twitter Sentiment Analysis'
    }
  },
  watch: {
    themeSwitch: function (old, newVal) {
      this.$vuetify.theme.dark = old;
    },

  },
}
</script>
