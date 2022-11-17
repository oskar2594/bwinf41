class Generator {
    filled = 0;
    constructor(canvas, settings) {
        this.settings = settings;
        this.canvas = canvas?.getContext("2d"); (canvas.width = settings.width), (canvas.height = settings.height);
        this.canvas.clearRect(0, 0, this.settings.width, this.settings.height);
        this.crystals = new Array(settings.height).fill(0).map((x) => new Array(settings.width).fill(null));
    }
    async setCrystal(crystalData, position) {
        if (!(position.y > this.crystals.length - 1 || position.x > this.crystals[0].length - 1 ||
            position.x < 0 || position.y < 0) && (this.crystals[position.y][position.x] == null ||
                this.crystals[position.y][position.x].time > 1)) {
            this.crystals[position.y][position.x] = crystalData;
             this.filled++;
            this.canvas.fillStyle = crystalData.color;
            this.canvas.fillRect(position.y, position.x, 1, 1);
            return true;
        }
        return false;
    }
    async generate() {
        for (let i = 0; i < this.settings.spawn.amount; i++) {
            const position = {
                x: Generator.randomInt((this.settings.width - this.settings.spawn.width) / 2,
                    (this.settings.width + this.settings.spawn.width) / 2 - 1),
                y: Generator.randomInt((this.settings.height - this.settings.spawn.height) / 2,
                    (this.settings.height + this.settings.spawn.height) / 2 - 1),
            };
            const growthValues = {
                angle: Generator.random(this.settings.growth.angle.min, this.settings.growth.angle.max),
                growthRate: Generator.random(this.settings.growth.rate.min, this.settings.growth.rate.max),
                oppositeGrowth: Generator.random(this.settings.growth.opposite.min, this.settings.growth.opposite.max),
            };
            const dirGrowth = {
                x: Generator.notZero(Math.cos(growthValues.angle) * growthValues.growthRate),
                y: Generator.notZero(Math.sin(growthValues.angle) * growthValues.growthRate),
            };
            const pixelGrowth = {
                up: Math.ceil(Math.abs(dirGrowth.y > 0 ? dirGrowth.y : dirGrowth.y * growthValues.oppositeGrowth)),
                down: Math.ceil(Math.abs(dirGrowth.y < 0 ? dirGrowth.y : dirGrowth.y * growthValues.oppositeGrowth)),
                left: Math.ceil(Math.abs(dirGrowth.x < 0 ? dirGrowth.x : dirGrowth.x * growthValues.oppositeGrowth)),
                right: Math.ceil(Math.abs(dirGrowth.x > 0 ? dirGrowth.x : dirGrowth.x * growthValues.oppositeGrowth)),
            };
            const color = `rgb(${Math.floor(55 + (growthValues.angle / 360) * 170)}, ${Math.floor(
                55 + (growthValues.angle / 360) * 170)}, ${Math.floor(55 + (growthValues.angle / 360) * 170)})`;
            if (!this.setCrystal({growth: pixelGrowth, color: color,
                time: Generator.randomInt(this.settings.growth.time.min, this.settings.growth.time.max),
            }, position))
                i--;
        }
        while (this.filled < this.settings.width * this.settings.height) {
            const tempCrystals = Generator.deepCopy(this.crystals);
            this.settings.update?.(this.filled / (this.settings.width * this.settings.height));
            for (let y = 0; y < this.crystals.length; y++) {
                for (let x = 0; x < this.crystals[0].length; x++) {
                    if (tempCrystals[y][x] == null) continue;
                    let crystal = this.crystals[y][x];
                    if (crystal == null || crystal.time-- > 0 || crystal.grew) continue;
                    for (let i = 1; i < crystal.growth.up + 1; i++)
                        if (!this.setCrystal(Generator.deepCopy(crystal), { x: x, y: y - i })) break;
                    for (let i = 1; i < crystal.growth.down + 1; i++)
                        if (!this.setCrystal(Generator.deepCopy(crystal), { x: x, y: y + i })) break;
                    for (let i = 1; i < crystal.growth.left + 1; i++)
                        if (!this.setCrystal(Generator.deepCopy(crystal), { x: x - i, y: y })) break;
                    for (let i = 1; i < crystal.growth.right + 1; i++)
                        if (!this.setCrystal(Generator.deepCopy(crystal), { x: x + i, y: y })) break;
                    crystal.grew = true;
                }
            }
            this.settings.update ?? (await new Promise((resolve) => setTimeout(resolve, 0)));
        }
    }
    static notZero = (value) => (Math.ceil(Math.abs(value)) * value) / Math.abs(value);
    static random = (min, max) => Math.random() * (max - min) + min;
    static randomInt = (min, max) => Math.floor(Math.random() * (max - min + 1) + min);
    static deepCopy = (element) => JSON.parse(JSON.stringify(element));
}