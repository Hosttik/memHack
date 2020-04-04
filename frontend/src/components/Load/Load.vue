<template>
    <div v-cloak @drop.prevent="addFile" @dragover.prevent class="dropArea">
        <h2>Перетащите файл</h2>
        <div>
            Поддерживаемый формат файла: jpg, jpeg, png.
            Максимальный размер изображения 5 Mb.
        </div>
        <ul>
            <li v-for="file in files">
                {{ file.name }} ({{ file.size | kb }} kb) <button @click="removeFile(file)" title="Remove">X</button>
            </li>
        </ul>

        <v-btn :disabled="uploadDisabled" @click="upload">Загрузить файл</v-btn>
    </div>
</template>

<script>

export default {
    name: "Load",
    data() {
        return {
            files: [],
        };
    },
    computed: {
        uploadDisabled() {
            return this.files.length === 0;
        }
    },
    methods:{
        addFile(e) {
            let droppedFiles = e.dataTransfer.files;
            if(!droppedFiles) return;
            // this tip, convert FileList to array, credit: https://www.smashingmagazine.com/2018/01/drag-drop-file-uploader-vanilla-js/
            ([...droppedFiles]).forEach(f => {
                this.files.push(f);
            });
        },
        removeFile(file){
            this.files = this.files.filter(f => {
                return f != file;
            });
        },
        upload() {

            let formData = new FormData();
            this.files.forEach((f,x) => {
                formData.append('file'+(x+1), f);
            });

            fetch('https://httpbin.org/post', {
                method:'POST',
                body: formData
            })
                .then(res => res.json())
                .then(res => {
                    console.log('done uploading', res);
                })
                .catch(e => {
                    console.error(JSON.stringify(e.message));
                });
        }
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
