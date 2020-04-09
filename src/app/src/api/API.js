import qs from 'qs';

const BASE_URL = "http://127.0.0.1:8000/api/";
const UPLOAD_URL = "http://127.0.0.1:8000/api/upload/";

const formatToFormData = (files) => {
    return Object.values(files).map((file) => {
        let formData = new FormData();
        formData.append("name", file.name);
        formData.append("size", file.size);
        formData.append("fileType", file.type);
        formData.append("file", file);
        return formData;
    });
}

const POST = (data) => {
    const formData = formatToFormData(data);
    console.log(formData);

    fetch(UPLOAD_URL, {
        method: 'post',
        body: formData,
    })
    .then((response) => console.log(response) || response.json())
    .then(server_data => {
        console.log(server_data)
    })
    .catch((error) => console.log(error));
}

export default POST;
