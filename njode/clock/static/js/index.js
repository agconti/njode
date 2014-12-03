;(function(){
  var http = require('http')
    , port = Number(process.argv[2]) || 3000

  http.createServer(function (req, res) {

    res.writeHead(200, { 'Content-Type': 'application/json' })

    var date = new Date()
      , jsonResponse = {
            "hour": date.getHours()
          , "minute": date.getMinutes()
          , "second": date.getSeconds()
        }

    res.end(JSON.stringify(jsonResponse))
        
  }).listen(port, function(){
    console.log('Listening on http://localhost:%d/', port)
  })

})()