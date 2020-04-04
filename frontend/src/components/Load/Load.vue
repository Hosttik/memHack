<template>
    <div v-cloak @drop.prevent="addFile" @dragover.prevent class="dropArea">
        <div>
            <h2>Перетащите файл</h2>
            <div>
                <p>Поддерживаемый формат файла: jpg, jpeg, png.</p>
                <p>Максимальный размер изображения 5 Mb.</p>
            </div>
            <ul>
                <li v-for="file in files">
                    {{ file.name }} {{ file.size }}
                    <button @click="removeFile(file)" title="Remove">X</button>
                </li>
            </ul>

            <v-btn :disabled="uploadDisabled" @click="upload">Загрузить файл</v-btn>
        </div>
    </div>
</template>

<script>

  import { apiHost } from 'src/api/api.utils';
  import showNotify from 'src/helpers/showNotify';
  import showErrors from 'src/helpers/showErrors';

  export default {
    name: 'Load',
    data() {
      return {
        files: [],
      };
    },
    computed: {
      uploadDisabled() {
        return this.files.length !== 1;
      }
    },
    methods: {
      addFile(e) {
        if (this.files.length === 1) {
          return;
        }
        let droppedFiles = e.dataTransfer.files;
        if (!droppedFiles) {
          return;
        }
        ([...droppedFiles]).forEach(f => {
          this.files.push(f);
        });
      },
      removeFile(file) {
        this.files = this.files.filter(f => {
          return f != file;
        });
      },
      upload: async function () {
        let file = this.files.shift();
        const formData = new FormData();
        formData.append('user_id', localStorage.getItem('memHackUserId'));
        formData.append('file', file);
        try {
          const res = await apiHost.post('/upload-file', formData);
          if (res.is_success) {
            showNotify({
              text: 'Картинка успешно загружена',
              type: 'success'
            });
            this.$router.push({path: 'description'})
          } else {
            showErrors(res && res.errors);
          }
        } catch (e) {
          showNotify({
            text: 'Ошибка загрузки файла',
            type: 'error'
          })
        }
      },
    }
  };
</script>

<style scoped>
    .dropArea {
        background-color: #e8ebec;;
        border: 2px dashed #5c6ac0;
        min-height: 400px;
        position: relative;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        display: flex;
    }
</style>
