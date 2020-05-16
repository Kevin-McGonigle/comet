const UPLOAD_URL = "http://127.0.0.1:8000/api/upload/";

export const createFormData = data => {
    let formData = new FormData();
    data.forEach(file => {
        formData.append("name", file.name);
        formData.append("size", file.size);
        formData.append("file_type", "text/plain");
        formData.append("file", file);
    });
    return formData;
}

export async function upload_files(data) {
    const formData = createFormData(data);
    return await fetch(UPLOAD_URL, {
        method: 'post',
        body: formData
    })
        .then(r => console.log(data) || r.json())
        .then(data => data)
        .catch(e => console.log(e));
}

export default upload_files;
