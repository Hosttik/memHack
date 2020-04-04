<template>
    <div>
        <h2 class="mb-2">Информация о наградах</h2>
        <v-app id="inspire">
            <v-flex xs12>
                <v-card class="full-height">
                    <div class="photo-wrap d-inline-block">
                        <div class="origin-photo">
                            <img :src="medalsImgPath" class="img-photo"/>
                        </div>
                    </div>
                    <div class="d-inline-block form_data">
                        <div v-if="medalsDescription">
                            {{medalsDescription}}
                        </div>
                        <div v-else>
                            Здесь будет описание найденных наград
                        </div>
                    </div>
                </v-card>
            </v-flex>
        </v-app>
    </div>
</template>

<script>
    import { apiHost } from 'src/api/api.utils';
    import showNotify from 'src/helpers/showNotify';
    import showErrors from 'src/helpers/showErrors';
    import getUrl from 'src/helpers/getUrl';

    export default {
        name: "Medals",
        beforeCreate: async function () {
            const params = {'user_id': localStorage.getItem('memHackUserId')};
            try {
                const res = await apiHost.get('/get-medals-file', params);
                const isSuccess = res.is_success;
                if (!isSuccess) {
                    return showErrors(res && res.errors);
                }
                this.medalsImgPath = getUrl(res.content.file_path);
                this.medalsDescription = getUrl(res.content.medals_description);
            } catch (e) {
                showNotify({
                    text: 'Произошла ошибка',
                    type: 'error'
                })
            }
        },
        data: () => ({
            medalsImgPath: '',
            medalsDescription: '',
        }),
    }
</script>

<style scoped>
    .full-height {
        height: 550px;
    }

    .photo-wrap {
        padding: 20px 0;
        width: 50%;
        height: 100%;
        float: left;
        vertical-align: top;
    }

    .origin-photo {
        width: 100%;
        height: 100%;
        float: left;
        position: relative;
    }

    .form_data {
        float: left;
        width: 40%;
    }

    .img-photo {
        background: grey;
        width: 70%;
        height: 100%;
    }
</style>