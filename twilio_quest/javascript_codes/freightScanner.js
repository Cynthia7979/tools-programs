function scan(freights) {
    var contrabandCount = 0;
    for (let freight of freights) {
        if (freight === 'contraband') {
            contrabandCount++;
        }
    }
    return contrabandCount;
}