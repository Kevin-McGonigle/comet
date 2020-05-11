const UPLOAD_URL = "http://127.0.0.1:8000/api/upload/";

async function upload_files(data)  {
    let formData = new FormData();
    data.forEach(file => {
        formData.append("name", file.name);
        formData.append("size", file.size);
        formData.append("file_type", file.type);
        formData.append("file", file);
    });

    return await fetch(UPLOAD_URL, {
        method: 'post',
        body: formData
    })
    .then(r => r.json())
    .then(data => data)
    .catch(e => console.log(e));
}

export default upload_files;
