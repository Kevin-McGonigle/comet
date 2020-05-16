const puppeteer = require('puppeteer');

const HOMEPAGE = 'http://localhost:3000';
const METRICS = 'http://localhost:3000/metrics';

let browser;
let page;

describe('E2E', () => {
    beforeEach(async () => {
        jest.setTimeout(10000000);
        browser = await puppeteer.launch({
            headless: false
        });
        page = await browser.newPage();

        page.emulate({
            viewport: {
                width: 1000,
                height: 1000
            },
            userAgent: ''
        });

        await page.goto(HOMEPAGE);
    });

    it('Create modal uploads & redirect to /metrics successfully', async () => {
        await page.click('#createButton');
        await page.type('#textAreaId', 'def pass(): pass', {delay: 20});
        await page.click('.css-nwvixr');
        await page.waitForNavigation();
        expect(page.url()).toBe(METRICS);
        browser.close();
    });

    it('Create modal should allow creation of new file', async () => {
        await page.click('#createButton');
        await page.type('#textAreaId', 'def pass(): pass', {delay: 20});

        await page.click('#plus');
        await page.type('input.css-5ljhhe', 'test', {delay: 20})
        await page.click('.📦z-idx_21 > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2)')

        await page.waitForSelector('#test')
        await page.click('#test');
        await page.type('#textAreaId', 'def pass(): pass', {delay: 20});

        await page.click('.css-nwvixr');
        await page.waitForNavigation();
        expect(page.url()).toBe(METRICS);
        browser.close();
    });

    it('Create modal should allow deletion of created tabs', async () => {
        await page.click('#createButton');

        await page.click('#plus');
        await page.type('input.css-5ljhhe', 't', {delay: 100})
        await page.click('.📦z-idx_21 > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2)')

        await page.waitFor(1000);
        await page.waitForSelector('#t')
        await page.click('#t');
        await page.click('#trash'); // delete tab test

        expect(document.querySelector('#t')).toBe(null);
        browser.close();
    });

    // it('Upload modal should allow uploading of files & redirection to metrics page', async () => {

    //     await page.click('#uploadButton');
    //     const uploadHandler = await page.$('.css-5ljhhe');
    //     await uploadHandler.uploadFile('test.txt');

    //     await page.waitForSelector('.css-nwvixr');
    //     await page.click('.css-nwvixr');

    //     browser.close();
    // });

    it('Metrics page should display all relevant information', async () => {
        await page.click('#createButton');
        await page.type('#textAreaId', 'def pass(): pass', {delay: 20});
        await page.click('.css-nwvixr');
        await page.waitForNavigation();
        expect(page.url()).toBe(METRICS);

        await page.waitForSelector('#ClassDiagram')
        await page.click('#ClassDiagram');
        await page.waitFor(500);

        await page.waitForSelector('#InheritanceTree')
        await page.click('#InheritanceTree');
        await page.waitFor(500);

        await page.waitForSelector('#AbstractSyntaxTree');
        await page.click('#AbstractSyntaxTree');
        await page.waitFor(500);

        await page.waitForSelector('#ControlFlowDiagram');
        await page.click('#ControlFlowDiagram');
        await page.waitFor(500);

        await page.waitForSelector('#DependencyGraph');
        await page.click('#DependencyGraph');
        await page.waitFor(500);

        await page.waitForSelector('#TreeMap');
        await page.click('#TreeMap');
        await page.waitFor(500);

        browser.close();
    });

});