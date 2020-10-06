module.exports = async function (context, req, inputDocument) {
    context.log('showresult!!');
    const rawDbData = inputDocument
    const dbData = rawDbData[rawDbData.length - 1].result
    const responseMessage = JSON.stringify(dbData)
    context.log(responseMessage)
    context.res = {
        body: responseMessage
    };
}
