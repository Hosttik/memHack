<template>
    <v-layout row>
        <v-flex class="full-height" xs3>
            <v-card class="full-height filters"><h1>Фильтры</h1>
                <v-list>
                    <template v-for="filter in filters">
                        <div :key="filter.id">
                            <v-list-tile>
                                <v-switch @change="filterChange" v-model="filter.activate" inset
                                          :label="filter.name"></v-switch>
                            </v-list-tile>
                            <img :src="filter.path"/>
                        </div>
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
                       :to="'/finish'"
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
  import getUrl from 'src/helpers/getUrl';
  import { mapMutations } from "vuex";

  export default {
    name: 'Filters',
    beforeCreate: async function () {
      const params = {'user_id': localStorage.getItem('memHackUserId')};
      try {
        const res = await apiHost.get('/get-original-file', params);
        const isSuccess = res.is_success;
        if (!isSuccess) {
          return showErrors(res && res.errors);
        }
        const img = getUrl(res.content.file_path);
        this.originImgPath = img;
        this.resultImgPath = img;
      } catch (e) {
        showNotify({
          text: 'Произошла ошибка',
          type: 'error'
        })
      }
      try {
        const res = await apiHost.get('/get-preview-filters', params);
        const isSuccess = res.is_success;
        if (!isSuccess) {
          return showErrors(res && res.errors);
        }
        this.filters = res.content.map(filter => {
          filter.activate = false;
          return filter
        });
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
        timerId: null,
        filters: [{
          id: 'filter1',
          activate: false,
          name: 'Фильтр первый йопта',
          path: 'https://lh3.googleusercontent.com/proxy/jqgFmlrKj1jNJOWYraERsfjoMitJ7lHQ8fUQi1VD5od9ThNF2iujR_waJIJaOdWVcfXojaGlMSPhPU9AuFdK44eqAWZIyg'
        }, {
          id: 'filter2',
          activate: false,
          name: 'Фильтр второй йопта',
          path: 'https://lh3.googleusercontent.com/proxy/jqgFmlrKj1jNJOWYraERsfjoMitJ7lHQ8fUQi1VD5od9ThNF2iujR_waJIJaOdWVcfXojaGlMSPhPU9AuFdK44eqAWZIyg'
        }, {
          id: 'filter3',
          activate: false,
          name: 'Фильтр третий йопта',
          path: 'https://lh3.googleusercontent.com/proxy/jqgFmlrKj1jNJOWYraERsfjoMitJ7lHQ8fUQi1VD5od9ThNF2iujR_waJIJaOdWVcfXojaGlMSPhPU9AuFdK44eqAWZIyg'
        }, {
          id: 'filter4',
          activate: false,
          name: 'Фильтр четвертый йопта',
          path: 'https://lh3.googleusercontent.com/proxy/jqgFmlrKj1jNJOWYraERsfjoMitJ7lHQ8fUQi1VD5od9ThNF2iujR_waJIJaOdWVcfXojaGlMSPhPU9AuFdK44eqAWZIyg'
        }, {
          id: 'filter5',
          activate: false,
          name: 'Фильтр пятый йопта',
          path: 'https://lh3.googleusercontent.com/proxy/jqgFmlrKj1jNJOWYraERsfjoMitJ7lHQ8fUQi1VD5od9ThNF2iujR_waJIJaOdWVcfXojaGlMSPhPU9AuFdK44eqAWZIyg'
        }, {
          id: 'filter6',
          activate: false,
          name: 'Фильтр шестой йопта',
          path: 'https://lh3.googleusercontent.com/proxy/jqgFmlrKj1jNJOWYraERsfjoMitJ7lHQ8fUQi1VD5od9ThNF2iujR_waJIJaOdWVcfXojaGlMSPhPU9AuFdK44eqAWZIyg'
        }, {
          id: 'filter7',
          activate: false,
          name: 'Фильтр седьмой йопта',
          path: 'https://lh3.googleusercontent.com/proxy/jqgFmlrKj1jNJOWYraERsfjoMitJ7lHQ8fUQi1VD5od9ThNF2iujR_waJIJaOdWVcfXojaGlMSPhPU9AuFdK44eqAWZIyg'
        }, {
          id: 'filter8',
          activate: false,
          name: 'Фильтр восьмой йопта',
          path: 'https://lh3.googleusercontent.com/proxy/jqgFmlrKj1jNJOWYraERsfjoMitJ7lHQ8fUQi1VD5od9ThNF2iujR_waJIJaOdWVcfXojaGlMSPhPU9AuFdK44eqAWZIyg'
        },]
      };
    },
    methods: {
      ...mapMutations(["changeLoaderStatus"]),
      filterChange: async function () {
        if (this.$store.state.loader) {
          return;
        }
        if (this.timerId) {
          clearTimeout(this.timerId);
        }
        this.timerId = setTimeout(async () => {
          this.changeLoaderStatus(true);
          const filters = this.filters.filter(filter => filter.activate).map(filter => filter.id).join('&');
          try {
            const res = await apiHost.get(`/use-filters?${filters}`);
            const isSuccess = res.data.is_success;
            if (!isSuccess) {
              this.changeLoaderStatus(false);
              return showErrors(res && res.data && res.data.errors);
            }

            this.resultImgPath = res.data.content;
          } catch (e) {
            this.changeLoaderStatus(false);
            showNotify({
              text: 'Произошла ошибка',
              type: 'error'
            })
          }
        }, 1000);
      }
    }
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
        padding: 15px;
        float: left;
        position: relative;
    }

    .future-photo {
        width: 50%;
        padding: 15px;
        float: right;
        position: relative;
    }

    .img-photo {
        background: grey;
        width: 100%;
        height: 100%;
        object-fit: cover;
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
