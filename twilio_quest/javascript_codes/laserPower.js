function calculatePower(powers) {
    return powers.map(p => p*2).reduce((total, current) => total + current, 0);
}