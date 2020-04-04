<template>
    <v-layout class="full-height" row>
        <v-flex class="full-height" xs3>
            <v-card class="full-height">sdfdfgdfg</v-card>
        </v-flex>
        <v-flex xs9>
            <v-card class="full-height">
                <div class="photo-wrap">
                    <div>sdfsdf</div>
                    <div>dsfsdgsd</div>
                </div>
                <div class="next-button-wrap">
                    <v-btn outline
                           class="ma-2"
                           color="indigo"
                    >Далее
                    </v-btn>
                </div>
            </v-card>
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
        height: 100%;
    }
    .photo-wrap {
        width: 80%;
        display: inline-flex;
    }
    .next-button-wrap {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        height: 100%;
    }

</style>
