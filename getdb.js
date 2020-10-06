const http = require('http');

const HOST = `konica2020teamc2.azurewebsites.net`;
const PATH = `/api/judge`;

module.exports = async function (context, myTimer, inputDocument) {
    context.log('getdb!!');
    const rawDbData = inputDocument
    const dbData = []
    for (let data of rawDbData) {
    dbData.push({name:data.name, time:data.time, hr:data.hr, volume:data.volume})
    }
    context.log(dbData)

    // 送信用
    const postData = dbData
    let postDataStr = JSON.stringify(postData);
    let options = {
        host: HOST,
        port: 80,
        path: PATH,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(postDataStr)
        }
    };

    let req = http.request(options, (res) => {
        console.log('STATUS: ' + res.statusCode);
        console.log('HEADERS: ' + JSON.stringify(res.headers));
        res.setEncoding('utf8');
        res.on('data', (chunk) => {
            console.log('BODY: ' + chunk);
        });
    });
    req.on('error', (e) => {
        console.log('problem with request: ' + e.message);
    });
    req.write(postDataStr);
    req.end();
};
