class Ducktypium {
    constructor(color) {
        assertColor(color);
        this.color = color;
        this.calibrationSequence = [];
    }
    
    refract(color) {
        assertColor(color);
        
        if (this.color === color) return color;
        else {
            const colorTable = {
                'red': {
                    'yellow': 'orange',
                    'blue': 'purple'
                }, 
                'blue': {
                    'red': 'purple',
                    'yellow': 'green'
                },
                'yellow': {
                    'red': 'orange',
                    'blue': 'green'
                }
            };
            return colorTable[color][this.color];
        }
    }
    
    calibrate(sequence) {
        this.calibrationSequence = sequence.map(i => i * 3).sort();
    }
}

function assertColor(color) {
    if (!['red', 'blue', 'yellow'].includes(color)) throw new ValueError;
}