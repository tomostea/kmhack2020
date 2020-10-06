module.exports = async function (context, req) {
    context.log('todb!!');
    context.log(req.query, req.body)
    const name = (req.query.name || (req.body && req.body.name));
    const date = new Date()
    let time = date.getTime() + 32400000 // timezone考慮
    if (req.query.time) {
        const rawTime = req.query.time
        const timeList = rawTime.split("a")
        const realTime = `${timeList[0]}-${timeList[1]}-${timeList[2]}T${timeList[3]}:${timeList[4]}:${timeList[5]}`
        time = Number(Date.parse(realTime))
    }
    const hr = (req.query.hr || 1)
    const volume = (req.query.volume || 1)
    const responseMessage = name ? `${name} ${time} ${hr} ${volume}` : "hello"
    context.res = {
        body: responseMessage
    };
    if (name) {
    context.bindings.outputDocument = JSON.stringify({ 
            name: name,
            time: time,
            hr: hr,
            volume: volume
        });
    }
}
