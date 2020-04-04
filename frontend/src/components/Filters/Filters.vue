<template>
    <v-layout row>
        <v-flex class="full-height" xs3>
            <v-card class="full-height filters"><h1>Фильтры</h1>
                <v-list two-line>
                    <template v-for="filter in filters">
                        <v-list-item
                                :key="filter.id"
                                ripple
                                @click=""
                        >
                            
                        </v-list-item>
                    </template>
                </v-list>
            </v-card>
        </v-flex>
        <v-flex xs9>
            <v-card class="full-height">
                <div class="photo-wrap">
                    <div class="origin-photo">
                        <div class="img-text">Оригинал</div>
                        <img :src="originImgPath" class="img-photo"/></div>
                    <div class="future-photo">
                        <div class="img-text">Результат</div>
                        <img :src="originImgPath" class="img-photo"/></div>
                </div>
                <v-btn outline
                       class="ma-2"
                       color="indigo"
                >Далее
                </v-btn>
            </v-card>
        </v-flex>
    </v-layout>
</template>

<script>
  import { apiHost } from 'src/api/api.utils';
  import showNotify from 'src/helpers/showNotify';
  import showErrors from 'src/helpers/showErrors';

  export default {
    name: 'Filters',
    beforeCreate: async function () {
      const params = {'user_id': localStorage.getItem('memHackUserId')};
      try {
        const res = await apiHost.get('/get-original-file', params);
        const isSuccess = res.data.is_success;
        if (!isSuccess) {
          return showErrors(res && res.data && res.data.errors);
        }
        const img = res.data.content;
        this.originImgPath = img;
        this.resultImgPath = img;
      } catch (e) {
        showNotify({
          text: 'Произошла ошибка',
          type: 'error'
        })
      }
      try {
        const res = await apiHost.post('/get-preview-filters', params);
        const isSuccess = res.data.is_success;
        if (!isSuccess) {
          return showErrors(res && res.data && res.data.errors);
        }
        this.filters = res.data.content;
      } catch (e) {
        showNotify({
          text: 'Произошла ошибка',
          type: 'error'
        })
      }
    },
    data() {
      return {
        originImgPath: '',
        resultImgPath: '',
        filters: [{
          id: 'filter1',
          name: 'Фильтр первый йопта',
          path: 'https://lh3.googleusercontent.com/proxy/jqgFmlrKj1jNJOWYraERsfjoMitJ7lHQ8fUQi1VD5od9ThNF2iujR_waJIJaOdWVcfXojaGlMSPhPU9AuFdK44eqAWZIyg'
        }, {
          id: 'filter2',
          name: 'Фильтр второй йопта',
          path: 'https://lh3.googleusercontent.com/proxy/jqgFmlrKj1jNJOWYraERsfjoMitJ7lHQ8fUQi1VD5od9ThNF2iujR_waJIJaOdWVcfXojaGlMSPhPU9AuFdK44eqAWZIyg'
        }, {
          id: 'filter3',
          name: 'Фильтр третий йопта',
          path: 'https://lh3.googleusercontent.com/proxy/jqgFmlrKj1jNJOWYraERsfjoMitJ7lHQ8fUQi1VD5od9ThNF2iujR_waJIJaOdWVcfXojaGlMSPhPU9AuFdK44eqAWZIyg'
        }, {
          id: 'filter4',
          name: 'Фильтр четвертый йопта',
          path: 'https://lh3.googleusercontent.com/proxy/jqgFmlrKj1jNJOWYraERsfjoMitJ7lHQ8fUQi1VD5od9ThNF2iujR_waJIJaOdWVcfXojaGlMSPhPU9AuFdK44eqAWZIyg'
        }, {
          id: 'filter5',
          name: 'Фильтр пятый йопта',
          path: 'https://lh3.googleusercontent.com/proxy/jqgFmlrKj1jNJOWYraERsfjoMitJ7lHQ8fUQi1VD5od9ThNF2iujR_waJIJaOdWVcfXojaGlMSPhPU9AuFdK44eqAWZIyg'
        }, {
          id: 'filter6',
          name: 'Фильтр шестой йопта',
          path: 'https://lh3.googleusercontent.com/proxy/jqgFmlrKj1jNJOWYraERsfjoMitJ7lHQ8fUQi1VD5od9ThNF2iujR_waJIJaOdWVcfXojaGlMSPhPU9AuFdK44eqAWZIyg'
        }, {
          id: 'filter7',
          name: 'Фильтр седьмой йопта',
          path: 'https://lh3.googleusercontent.com/proxy/jqgFmlrKj1jNJOWYraERsfjoMitJ7lHQ8fUQi1VD5od9ThNF2iujR_waJIJaOdWVcfXojaGlMSPhPU9AuFdK44eqAWZIyg'
        }, {
          id: 'filter8',
          name: 'Фильтр восьмой йопта',
          path: 'https://lh3.googleusercontent.com/proxy/jqgFmlrKj1jNJOWYraERsfjoMitJ7lHQ8fUQi1VD5od9ThNF2iujR_waJIJaOdWVcfXojaGlMSPhPU9AuFdK44eqAWZIyg'
        },]
      };
    },
  }
</script>

<style scoped>
    .full-height {
        height: 720px;
    }

    .photo-wrap {
        padding-top: 50px;
        width: 100%;
        display: block;
        height: 90%;
        vertical-align: middle;
    }


    .origin-photo {
        width: 50%;
        height: 100%;
        float: left;
        position: relative;
    }

    .future-photo {
        width: 50%;
        height: 100%;
        float: right;
        position: relative;
    }

    .img-photo {
        background: grey;
        width: 70%;
        height: 100%;
    }

    .img-text {
        position: absolute;
        top: -20px;
        left: 0;
        right: 0;
    }

    .filters {
        overflow: scroll;
    }

</style>
