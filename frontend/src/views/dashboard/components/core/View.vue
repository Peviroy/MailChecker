<template>
  <v-content>
    <router-view />
    
    <dashboard-core-footer />
  </v-content>
</template>

<script>
  export default {
    name: 'DashboardCoreView',

    components: {
      //DashboardCoreAppBar: () => import('./AppBar'),
      DashboardCoreFooter: () => import('./Footer'),
    },
  }
</script>
