module.exports = async function (context, req) {
    context.log('showresult2!!');

    const name = req.query.name || "stranger"
    const hr = req.query.hr || 60
    const volume = req.query.volume || 500

    const hrThres = req.query.hrthres|| 75
    const volumeThres = req.query.volumethres || 600

    let behave = 0
    if (hr < 0 && volume < 0) {
        behave = 2
    } else if (hr > hrThres && volume < volumeThres ) {
        behave = 1
    }

    const responseJson = {}
    responseJson.name = name
    responseJson.behave = behave
    responseJson.info = `hr: ${hr} volume:${volume} hrThres: ${hrThres} volumeThres: ${volumeThres}`

    context.res = {
        body: JSON.stringify(responseJson)
    };
}