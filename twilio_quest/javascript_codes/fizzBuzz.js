const arg = process.argv[2];
if ((arg % 3) === 0) {
    if ((arg % 5) === 0) {
        console.log('JavaScript');
    } else {
        console.log('Java')
    }
} else {
    if ((arg % 5) === 0) {
        console.log('Script');
    } else {
        console.log(arg);
    }
}