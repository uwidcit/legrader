const { grade } = require('./lib.js');

const submission = process.argv[2];

if(!submission){
    console.log('No assignment passed')
}else{
    grade(submission, './participants.csv');
}
