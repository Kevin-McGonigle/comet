import {createFileInformation, readFile, shapeFileData} from '../helpers';
import "../../setupTests";

test('readFile should read a single file and returns its contents', () => {
    const file = readFile(new File(["foojkhjkhkjhkhhj"], "foo.txt", {
        type: "text/plain",
    }));
    file.then(value => expect(value).toEqual("foojkhjkhkjhkhhj"));
});

test('readFile should read multiple files and returns their contents', () => {
    const file = readFile([new File(["foojkhjkhkjhkhhj"], "foo.txt", {
        type: "text/plain",
    }), new File(["test"], "test.txt", {
        type: "text/plain",
    })]);
    file.then(value => expect(value).toEqual(["foojkhjkhkjhkhhj", "test"]));
});

test('createFileInformation should generate files from an array of names and content', () => {
    const fileNames = ["FileName1", "FileName2"];
    const content = ["FileName1Content", "FileName2Content"];

    const files = createFileInformation(fileNames, content);
    files.forEach((file, index) => {
        expect(file instanceof File);
        expect(file.name === fileNames[index]);
        const fileContents = readFile(file);
        fileContents.then(value => expect(value).toEqual(content[index]));
    })
});

test('shapeFileData should translate a file object into a JS object', () => {
    const file = [new File(["foojkhjkhkjhkhhj"], "foo.txt", {
        type: "text/plain",
    })];
    const shapedData = shapeFileData(file);
    expect(shapedData[0].name === 'foo.txt');
    expect(shapedData[0].size === 16);
    expect(shapedData[0].type === 'text/plain');
});