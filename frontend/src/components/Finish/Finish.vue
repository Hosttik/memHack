<template>
    <v-layout row>
        <v-flex xs4 offset-sm4>
            <v-card>
                <v-img :src="imgPath"/>
                <v-card-actions>
                    <v-btn color="indigo" outline>Скачать</v-btn>
                    <v-spacer></v-spacer>
                    <social-sharing :url="imgPath" inline-template>
                        <div>
                            <network network="facebook">
                                <i class="fa fa-fw fa-facebook"></i>
                            </network>
                            <network network="linkedin">
                                <i class="fa fa-fw fa-linkedin"></i>
                            </network>
                            <network network="pinterest">
                                <i class="fa fa-fw fa-pinterest"></i>
                            </network>
                            <network network="twitter">
                                <i class="fa fa-fw fa-twitter"></i>
                            </network>
                            <network network="vk">
                                <i class="fa fa-vk"></i>
                            </network>
                        </div>
                    </social-sharing>


                </v-card-actions>
            </v-card>
        </v-flex>
    </v-layout>

</template>

<script>
  import showNotify from 'src/helpers/showNotify';
  import showErrors from 'src/helpers/showErrors';
  import { apiHost } from 'src/api/api.utils';

  export default {
    name: 'Finish',
    async beforeCreate() {
      const params = {'user_id': localStorage.getItem('memHackUserId')};
      try {
        const res = await apiHost.get('/get-filtered-file ', params);
        const isSuccess = res.data.is_success;
        if (!isSuccess) {
          return showErrors(res && res.data && res.data.errors);
        }
        this.imgPath = res.data.content;
      } catch (e) {
        showNotify({
          text: 'Произошла ошибка',
          type: 'error'
        })
      }
    },
    data() {
      return {
        imgPath: 'https://i.ytimg.com/vi/bgxFHfNZID0/maxresdefault.jpg'
      }
    }
  }
</script>

<style scoped>

</style>
