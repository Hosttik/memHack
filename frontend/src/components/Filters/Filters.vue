<template>
    <v-layout class="full-height" row>
        <v-flex class="full-height" xs2>
            <v-card class="full-height">Фильтры</v-card>
        </v-flex>
        <v-flex xs10>
            <v-card class="full-height">
                <div class="photo-wrap">
                    <div class="origin-photo">
                        <div class="img-text">Оригинал</div>
                        <img :src="originImgPath" class="img-photo"/></div>
                    <div class="future-photo">
                        <div class="img-text">Результат</div>
                        <img :src="originImgPath" class="img-photo"/></div>
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
        filters: {}
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
        height: 100%;
    }

    .next-button-wrap {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        height: 100%;
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
        width: 80%;
        height: 90%;
        vertical-align: middle;
    }

    .img-text {
        position: absolute;
        top: -20px;
        left: 0;
        right: 0;
    }

</style>
