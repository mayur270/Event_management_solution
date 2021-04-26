<template>
  <nav>
    <v-navigation-drawer
      v-model="drawer"
      app
    >
      <v-container style="background: #e5e5e5">
        <v-img
        max-height="139"
        max-width="250"
        src="../assets/logo.png"
        ></v-img>
      </v-container>

      <v-divider></v-divider>

      <v-container class="mt-1">
        <v-layout justify-center>
          <v-card-actions>
            <v-btn 
            router to="/create-event"
            color="#14213d" 
            class="my-4 px-4"
            depressed
            dark
            >
              <span>Create Event</span>
            </v-btn>
          </v-card-actions>
        </v-layout>
        
        <v-list nav class="mt-0">
          <v-list-item router to="/events" >
            <v-list-item-action>
              <v-icon small>fas fa-tachometer-alt</v-icon>
            </v-list-item-action>
          <v-list-item-content >
            <v-list-item-title >Events</v-list-item-title>
          </v-list-item-content>
          </v-list-item>

          <v-list-item  router to="/tickets" >
            <v-list-item-action>
              <v-icon small>fas fa-users</v-icon>
            </v-list-item-action>
            <v-list-item-content >
              <v-list-item-title >Tickets</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

        </v-list>
      </v-container>

    <!--  -->
    </v-navigation-drawer>

    <v-app-bar app flat style="background: #fca311" class="white--text">
      <v-app-bar-nav-icon class="ml-0" @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-toolbar-title>Event Management Dashboard</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn icon class="mr-0">
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>

    </v-app-bar>

  </nav>
</template>

<script>

export default {
  name: 'Navbar',
  data: () => ({ drawer: true }),
};
</script>