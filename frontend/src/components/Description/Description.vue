<template>
    <div>
        <h2 class="mb-2">Заполните данные о человеке на фото</h2>
        <v-app id="inspire">
            <v-flex xs12>
                <v-card class="full-height">
                    <div class="photo-wrap d-inline-block">
                        <div class="origin-photo">
                            <img :src="originImgPath" class="img-photo"/>
                        </div>
                    </div>
                    <div class="d-inline-block form_data">
                        <v-form>
                            <v-container>
                                <v-flex>
                                    <v-text-field
                                        v-model="description.last_name"
                                        label="Фамилия"
                                    ></v-text-field>
                                </v-flex>
                                <v-flex>
                                    <v-text-field
                                        v-model="description.first_name"
                                        label="Имя"
                                    ></v-text-field>
                                </v-flex>
                                <v-flex>
                                    <v-text-field
                                        v-model="description.middle_name"
                                        label="Отчество"
                                    ></v-text-field>
                                </v-flex>
                                <v-flex>
                                    <v-text-field
                                        v-model="description.rank"
                                        label="Воинское звание"
                                    ></v-text-field>
                                </v-flex>
                                <v-flex>
                                    <v-textarea
                                        v-model="description.info"
                                        label="Доп. информация"
                                    ></v-textarea>
                                </v-flex>

                                <v-btn @click="upload">Далее</v-btn>
                            </v-container>
                        </v-form>
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

    export default {
        name: "Description",
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
            } catch (e) {
                showNotify({
                    text: 'Произошла ошибка',
                    type: 'error'
                })
            }
        },
        data: () => ({
            originImgPath: '',
            description: {
                first_name: '',
                last_name: '',
                middle_name: '',
                rank: '',
                info: '',
            },
        }),
        methods: {
            upload: async function () {
                try {
                    const res = await apiHost.get('/save-description', {...this.description, 'user_id': localStorage.getItem('memHackUserId')});
                    if (res.data.is_success) {
                        showNotify({
                            text: 'Данные успешно загружены',
                            type: 'success'
                        });
                        this.$router.push({path: 'filters'})
                    } else {
                        showErrors(res && res.data && res.data.errors);
                    }
                } catch (e) {
                    showNotify({
                        text: 'Ошибка загрузки данных',
                        type: 'error'
                    })
                }
            },
        }
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