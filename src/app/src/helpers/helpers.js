export async function readFile(file) {
    const fileReader = new FileReader();
    const promise = new Promise((resolve, reject) => {
        fileReader.onerror = () => {
            fileReader.abort();
            reject('Problem parsing input files');
        };
        fileReader.onload = () => {
            resolve(fileReader.result);
        };
        fileReader.readAsText(file);
    });
    return await promise;
}

export const createFileInformation = (fileNames, fileContent) => {
    return fileNames.map((file, ind) => {
        return new File([fileContent[ind]], file, {type: "text/plain", lastModified: "test"})
    });
}

export const shapeFileData = (fileData) => {
    return fileData.map((file) => {
        const data = readFile(file);
        return {
            name: file.name,
            lastModified: file.lastModified,
            size: file.size,
            type: file.type,
            content: data,
        };
    });
}

