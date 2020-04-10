const UPLOAD_URL = "http://127.0.0.1:8000/api/upload/";

const upload_files = (data) => {
    let formData = new FormData();

    data.forEach(file => {
        formData.append("name", file.name);
        formData.append("size", file.nsize);
        formData.append("fileType", file.type);
        formData.append("file", file);
    });

    fetch(UPLOAD_URL, {
        method: 'post',
        body: formData
    }).then(r => console.log(r) || r.json())
        .then(server_data => console.log(server_data))
        .catch(e => console.log(e));
}

export default upload_files;
