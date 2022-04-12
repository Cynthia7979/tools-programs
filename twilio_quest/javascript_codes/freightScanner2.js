function scan(freights) {
    var contrabandIndexes = [];
    freights.forEach((f, i) => {
        if (f === 'contraband') {
            contrabandIndexes.push(i);
        }
    });
    return contrabandIndexes;
}