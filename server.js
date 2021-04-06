// require all dependencies
const express = require('express');
const { spawn } = require('child_process');
const fs = require('fs');

const scriptName = __dirname + '/blinds.py';
// const scriptName = 'test.py';
const statusFileName = __dirname + '/status.txt';
const app = express();

// set up the template engine
app.set('views', __dirname);
// app.set('view engine', 'html');
app.use(express.static(__dirname + '/public'));

// GET response for '/'
app.get('/', function (req, res) {

    // render the 'index' template, and pass in a few variables
    res.render('index', { title: 'Blinds', message: 'Blinds' });
});

app.get('/close', function(req, res) {
    // res.send('closed resp');
    // console.log('Close command');
    // return;
    // Call your python script here.
    // I prefer using spawn from the child process module instead of the Python shell
    const scriptPath = scriptName;
    const process = spawn('python3', [scriptPath, 'close'])
    process.stdout.on('data', (myData) => {
        // Do whatever you want with the returned data.
        // ...
        fs.writeFile(statusFileName, 'closed', function(err) {
            if(err) {
                return console.log(err);
            }
            console.log('The file was saved!');
        }); 
        res.send('closed');
    })
    process.stderr.on('data', (myErr) => {
        // If anything gets written to stderr, it'll be in the myErr variable
    })
})
app.get('/open', function(req, res) {
    // res.send('opened resp');
    // console.log('Open command');
    // return;
    // Call your python script here.
    // I prefer using spawn from the child process module instead of the Python shell
    const scriptPath = scriptName;
    const process = spawn('python3', [scriptPath, 'open'])
    process.stdout.on('data', (myData) => {
        // Do whatever you want with the returned data.
        // ...
        fs.writeFile(statusFileName, 'opened', function(err) {
            if(err) {
                return console.log(err);
            }
            console.log('The file was saved!');
        }); 
        res.send('opened');
    })
    process.stderr.on('data', (myErr) => {
        // If anything gets written to stderr, it'll be in the myErr variable
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
