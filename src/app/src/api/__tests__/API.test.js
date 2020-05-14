import upload_files, { createFormData } from '../API';


const fetchMock = jest.spyOn(global, 'fetch').mockImplementation(() => Promise.resolve({ json: () => [] }))

test('should create correct FormData on single file', () => { 
    const file = new File(["test"], "test.txt", { type: "text/plain", size: 4 });
    const expectedFormData = new FormData();
    expectedFormData.append("name", "test");
    expectedFormData.append("size", 4);
    expectedFormData.append("file_type", "text/plain");
    expectedFormData.append("file", file);

    const formData = createFormData([file]);
    for (var key in expectedFormData) {
        expect(expectedFormData[key]).toEqual(formData[key]);
    }
});

test('should create correct FormData on multiple file', () => { 
    const file = new File(["test"], "test.txt", { type: "text/plain", size: 4 });
    const secondaryFile = new File(["fooo"], "fooo.txt", { type: "text/plain", size: 4 });

    const expectedFormData = new FormData();
    expectedFormData.append("name", "test");
    expectedFormData.append("size", 4);
    expectedFormData.append("file_type", "text/plain");
    expectedFormData.append("file", file);
    expectedFormData.append("name", "fooo");
    expectedFormData.append("size", 4);
    expectedFormData.append("file_type", "text/plain");
    expectedFormData.append("file", secondaryFile);

    const formData = createFormData([file, secondaryFile]);
    for (var key in expectedFormData) {
        expect(expectedFormData[key]).toEqual(formData[key]);
    }
});

test('should upload succesfully', async () => { 
    const formData = new FormData();
    const data = await upload_files([]);
    expect(Array.isArray(data)).toEqual(true);
    expect(data.length).toEqual(0);
    expect(fetchMock).toHaveBeenCalledWith("http://127.0.0.1:8000/api/upload/", {method: "post", body: formData});
});


