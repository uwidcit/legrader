const fs = require("fs").promises;
const exists = require('fs').existsSync;
const { createReadStream } = require('fs');
const csv = require('csv-parser');
const {spawn} = require('child_process');
const {timeout, TimeoutError } = require('promise-timeout');
const path = require('path');

//gets name of student based on myelearning submission folder name
function getName(dirname){
    dirname = dirname.replace('sample', '').replace('stream1\\', '').replace('stream2\\', '').replace('submissions', '').replace('/', '').replace('\\', '');
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
async function getStudentPartial(participantFile){
    const students = await loadStudents(participantFile);

    return function(dirname){
        const {firstname, lastname} = getName(dirname);
        const key = `${firstname} ${lastname}`;
        res = students[key];
        return res === undefined ? { 'First name':firstname, 'Surname':lastname, 'ID number': 'unknown' } : res;
    }
}


function readCSV(path){
    return new Promise((resolve)=>{
      const results = [];
  
      createReadStream(path)
        .pipe(csv())
        .on('data', (data) => results.push(data))
        .on('end', () => {
          resolve(results);
        });
  
    });
}


function initDB(){
    const init = spawn('python', [path.join(__dirname, `/workspace/initDB.py`)]);
    return new Promise((resolve, reject) => {
        init.stdout.on('data', function (data) {
            console.log(data.toString());
            // dataToSend = data.toString();
        });

        init.stderr.on('data', data=>console.log(data.toString()));
        init.on('close', code => {
            resolve(code);
        })
    });

}

function startServer(){
    const server = spawn('python', [path.join(__dirname, `/workspace/main.py`)]);

    server.stdout.on('data', function (data) {
        console.log(data.toString());
    });

    server.stderr.on('data', data=>console.log(data.toString()));

    // return new Promise((resolve, reject)=>{
    //     setTimeout(_=>{
    //         resolve({
    //             stop : () => {
    //                 server.kill('SIGINT');
    //                 console.log('\tStopping Server'); 
    //             }
    //         });

    //     }, 2000)
    // });
   

}

async function clearWorkspace(){
    const main = path.join(__dirname, `/workspace/main.py`);
    const initDB = path.join(__dirname, `/workspace/initDB.py`);
    const question3 = path.join(__dirname, `/workspace/static/app.html`);
    const question4 = path.join(__dirname, `/workspace/templates/app.html`);
    const testdb = path.join(__dirname, `/workspace/test.db`);
    const models = path.join(__dirname, `/workspace/models.py`);

    const files = [main, initDB, question3, question4, testdb, models];

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
    await fs.copyFile(path.join(dir, '/models.py'), path.join(__dirname, `/workspace/models.py`));

    const question2 = path.join(dir, '/question2.html');
    const question3 = path.join(dir, '/question3.html')
    const dummy2 = path.join(__dirname, `/dummy/question2.html`);
    const dummy3 = path.join(__dirname, `/dummy/question3.html`);
    const static = path.join(__dirname, `/workspace/static/app.html`);
    const templates = path.join(__dirname, `/workspace/templates/app.html`);

    if(exists(question2) && exists(question3)){
        await fs.copyFile(question2, templates);
        await fs.copyFile(question3, static);
    }else if (exists(question2) ){
        await fs.copyFile(question2, templates);
        await fs.copyFile(dummy3, static);
    }else if(exists(question2)){
        await fs.copyFile(question3, static);
        await fs.copyFile(dummy2, templates);
    }

}


async function grade(directory, participantFile){

    const getStudent = await getStudentPartial(participantFile);

    const student = getStudent(directory);

    console.log(`**************** Running: ${student['First name']} ${student['Surname']} ${student['ID number']} **********************`);

    let server;

    try{

        await moveToWorkspace(directory);
        
        await timeout(initDB(), 10000);
        
        console.log('\tDatabase Initialized');

        server = await startServer();
        console.log('\tServer Started');
 
    }catch(e){
        console.log('\tError', e);
        if(e instanceof TimeoutError) console.log('\tServer Timed out')
    }finally{
        if(server)server.stop();
        return grade;
    }
    
}



module.exports = {
    grade
}