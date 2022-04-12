class Materializer {
    constructor(targetName) {
        this.target = targetName;
        this.activated = false;
    }
    
    activate() {
        this.activated = true;
    }
    
    materialize() {
        return this.activated ? this.target : undefined;
    }
}