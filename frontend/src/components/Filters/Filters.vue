<template>
    <v-layout row>
        <v-flex class="full-height" xs3>
            <v-card class="full-height">sdfdfgdfg</v-card>
        </v-flex>
        <v-flex xs9>
            <v-card>sdfdfgdfg</v-card>
        </v-flex>
    </v-layout>
</template>

<script>
  export default {
    name: 'Filters',
    data() {
      return {
        filtersList: ['']
      };
    },
  }
</script>

<style scoped>
    .full-height {
        min-height: 100%;
    }

</style>
