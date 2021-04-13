const { grade } = require('lib.js');

const submission = process.argv[2];

if(!assignment){
    console.log('No assignment passed')
}else{
    grade(submission)
}
