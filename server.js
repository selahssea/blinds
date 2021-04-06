const express = require('express');
const { spawn } = require('child_process');
const fs = require('fs');

const scriptName = __dirname + '/blinds.py';
const cleanupScriptPath = __dirname + '/cleanup.py';
const statusFileName = __dirname + '/status.txt';
const app = express();

app.set('views', __dirname);
app.use(express.static(__dirname + '/public'));

app.get('/', function (req, res) {
    res.render('index');
});

app.get('/close', function(req, res) {
    const scriptPath = scriptName;
    const percentage = req.query.percentage ? req.query.percentage : '';
    const process = spawn('python3', [scriptPath, 'close', percentage]);
    process.stdout.on('data', (myData) => {
        fs.writeFile(statusFileName, 'closed', function(err) {
            if(err) {
                return console.log(err);
            }
            console.log('The file was saved!');
        }); 
        res.send('closed');
    })
    process.stderr.on('data', (err) => {
        console.error('Blinds.py error: ', String(err))
        res.status(500).send('Blinds close script error');
    })
})

app.get('/open', function(req, res) {
    const scriptPath = scriptName;
    const percentage = req.query.percentage ? req.query.percentage : '';
    const process = spawn('python3', [scriptPath, 'open', percentage])
    process.stdout.on('data', (myData) => {
        fs.writeFile(statusFileName, 'opened', function(err) {
            if(err) {
                return console.log(err);
            }
            console.log('The file was saved!');
        }); 
        res.send('opened');
    })
    process.stderr.on('data', (err) => {
        console.error('Blinds.py error: ', String(err));
        res.status(500).send('Blinds open script error');
    })
})

app.get('/stop', function(req, res) {
    const killBlindsPy = spawn('pkill', ['-9', '-f', 'blinds.py']);
    killBlindsPy.stdout.on('data', data => {
        console.log(`pkill out: ${data}`);
    })
    killBlindsPy.stdout.on('close', code => {
        console.error(`stderr: ${code}`);
        const process = spawn('python3', [cleanupScriptPath])
        process.stdout.on('data', (myData) => {
            res.send('stopped');
        })
        process.stderr.on('data', (err) => {
            console.error('Cleanup.py error: ', String(err));
            res.status(500).send('Cleanup script error');
        })
    })
})

app.get('/status', function(req, res) {
    fs.readFile(statusFileName, 'utf8', function(err, data) {
        console.log(data);
        res.send(data);
    });
})

// start up the server
app.listen(3000, function () {
    console.log('Listening on http://localhost:3000');
});
