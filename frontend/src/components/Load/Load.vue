<template>
    <div v-cloak @drop.prevent="addFile" @dragover.prevent class="dropArea">
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
</template>

<script>

  import { apiHost } from 'src/api/api.utils';

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
        formData.append('user_id', 1);
        formData.append('file', file);
        try {
          const res = await apiHost.post('/upload-file', formData);
          if (res.is_success) {
              // вывести сообщение об успехе
              this.$router.push({ path: 'filters' })
          } else {
              // вывести ошибку
          }
        } catch (e) {
            // вывести ошибку нашу на фронте "Ошибка загрузки файла"
        }
      },
    }
  };
</script>

<style scoped>
    .dropArea {
        background-color: lightblue;
        border: 2px solid darkgray;
        min-height: 400px;
    }
</style>
