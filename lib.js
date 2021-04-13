const fs = require("fs").promises;
const exists = require('fs').existsSync;
const extra = require('fs-extra');
const {spawn} = require('child_process');
const {timeout, TimeoutError } = require('promise-timeout');

const DEBUG = true;

const GRADER = '/mnt/c/Users/snick/Desktop/DCIT/INFO 2602/A2Marker/';


//gets name of student based on myelearning submission folder name
function getName(dirname){
    const [firstname, ...lastname] = dirname.split('_')[0].split(' ');
    return {firstname, lastname: lastname.join(' ')};
}

//Creates a map which returns a student object from their full name in myelearning
//participant file download
async function loadStudents(participantFile='participants.csv'){
    const submissions = await readCSV(participantFile);
    return submissions.reduce((acc, cur)=>{
        acc[`${cur['First name']} ${cur['Surname']}`] = cur;
        return acc;
    }, {});
}

// partial function which returns a getStudent() function,
// get student function returns a student object from a submission directory name
async function getStudentPartial(){
    const students = await loadStudents();

    return function(dirname){
        const {firstname, lastname} = getName(dirname);
        const key = `${firstname} ${lastname}`;
        res = students[key];
        return res === undefined ? { 'First name':firstname, 'Surname':lastname, 'ID number': 'unknown' } : res;
    }
}

const getStudent = getStudentPartial();

function initDB(){
    const init = spawn('python3', [path.join(__dirname, `/workspace/initDB.py`)]);
    return new Promise((resolve, reject) => {
        init.stdout.on('data', function (data) {
            console.log(data.toString());
            // dataToSend = data.toString();
        });

        // init.stderr.on('data', (data) => {
        //     console.error(`stderr: ${data}`);
        // });
        init.on('close', code => {
            resolve(code);
        })
    });

}

function startServer(){
    const server = spawn('python3', [path.join(__dirname, `/workspace/main.py`)]);

    server.stdout.on('data', function (data) {
        console.log(data.toString());
    });

    return new Promise((resolve, reject)=>{
        setTimeout(_=>{
            resolve({
                stop : () => {
                    server.kill('SIGINT');
                    console.log('\tStopping Server'); 
                }
            });

        }, 2000)
    });
   

}

async function clearWorkspace(){
    const main = path.join(__dirname, `/workspace/main.py`);
    const initDB = path.join(__dirname, `/workspace/initDB.py`);
    const question3 = path.join(__dirname, `/workspace/static/app.html`);
    const question4 = path.join(__dirname, `/workspace/templates/app.html`);
    const testdb = path.join(__dirname, `/workspace/test.db`);

    const files = [main, initDB, question3, question4, testdb];

    const promises = files.map( file=>{
        if(exists(file))
            return fs.unlink(file);
        else
            return new Promise( r => r('Done') );
    });

    return Promise.allSettled(promises);
    
}

async function moveToWorkspace(dir){
 
    await fs.copyFile(path.join(dir, '/main.py'), path.join(__dirname, `/workspace/main.py`));
    await fs.copyFile(path.join(dir, '/initDB.py'), path.join(__dirname, `/workspace/initDB.py`));


    const question3 = path.join(dir, '/question3.html');
    const question4 = path.join(dir, '/question4.html')
    const dummy3 = path.join(__dirname, `/dummy/question3.html`);
    const dummy4 = path.join(__dirname, `/dummy/question4.html`);
    const static = path.join(__dirname, `/workspace/static/app.html`);
    const templates = path.join(__dirname, `/workspace/templates/app.html`);

    if(exists(question3) && exists(question4)){
        await fs.rename(question3, templates);
        await fs.rename(question4, static);
    }else if (exists(question3) ){
        await fs.rename(question3, templates);
        await fs.copyFile(dummy4, static);
    }else if(exists(question4)){
        await fs.rename(question4, static);
        await fs.copyFile(dummy3, templates);
    }

}


async function grade(directory){

    const { ID } = getStudent(directory);

    console.log('**************** Running: '+ID+' **********************');

    let server;

    try{

        await moveToWorkspace(directory);
        
        await timeout(initDB(), 10000);
        
        console.log('\tDatabase Initialized');

        server = await startServer();
        console.log('\tServer Started');
 
    }catch(e){
        console.log('\tError', e);
        if(e instanceof TimeoutError)
            console.log('\tServer Timed out')
    }finally{
        if(server)server.stop();
        return grade;
    }
    
}



module.exports = {
    grade
}