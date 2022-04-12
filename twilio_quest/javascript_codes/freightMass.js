function calculateMass(freights) {
    return freights.reduce((totalMass, currentItem) => totalMass + currentItem.length, 0);
}