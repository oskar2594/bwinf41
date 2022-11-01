window.onload = function () {
    let surface = null;
    document.getElementById("generate").addEventListener("click", function () {

        function updateProgress(progress) {
            document.getElementsByClassName('display')[0].style = `--height: ${progress}%`;
            if(progress == 101) {
                document.getElementsByClassName('display')[0].style = `--height: 0%`;
            }
        }

        surface = new Surface(document.getElementsByClassName('canvas')[0], {
            width: parseInt(document.getElementById("width").value) || 500,
            height: parseInt(document.getElementById("height").value) || 500,
            spawn: {
                width: parseInt(document.getElementById("spawn_width").value) || 500,
                height: parseInt(document.getElementById("spawn_height").value) || 500,
                amount: parseInt(document.getElementById("spawn_amount").value) || 100
            },
            growth: {
                up: {
                    min: parseInt(document.getElementById("growth_up_min").value) || 1,
                    max: parseInt(document.getElementById("growth_up_max").value) || 1
                },
                down: {
                    min: parseInt(document.getElementById("growth_down_min").value) || 1,
                    max: parseInt(document.getElementById("growth_down_max").value) || 1
                },
                left: {
                    min: parseInt(document.getElementById("growth_left_min").value) || 1,
                    max: parseInt(document.getElementById("growth_left_max").value) || 1
                },
                right: {
                    min: parseInt(document.getElementById("growth_right_min").value) || 1,
                    max: parseInt(document.getElementById("growth_right_max").value) || 1
                }
            },
            updateProgress
        });
        surface.generate();
    });
};


class Surface {
    filled = 0;
    constructor(ref, settings) {
        this.canvasDrawer = new CanvasDrawer(ref, settings.width, settings.height);
        this.width = settings.width;
        this.height = settings.height;
        this.crystals = new Array(settings.height).fill(0).map(x => new Array(settings.width).fill(null));
        this.create(settings.spawn.amount, { spawn: settings.spawn, growth: settings.growth });
        this.canvasDrawer.clear();
        this.updateProgress = settings.updateProgress;
    }

    create(amount, settings) {
        for (let i = 0; i < amount; i++) {
            let x = Utils.randomInt((this.width - settings.spawn.width) / 2, (this.width + settings.spawn.width) / 2 - 1);
            let y = Utils.randomInt((this.height - settings.spawn.height) / 2, (this.height + settings.spawn.height) / 2 - 1);
            let growth = {
                up: Utils.randomInt(settings.growth.up.min, settings.growth.up.max),
                down: Utils.randomInt(settings.growth.down.min, settings.growth.down.max),
                left: Utils.randomInt(settings.growth.left.min, settings.growth.left.max),
                right: Utils.randomInt(settings.growth.right.min, settings.growth.right.max)
            }
            if (this.crystals[y][x] == null) {
                this.crystals[y][x] = new Crystal(x, y, growth);
                this.filled++;
                continue;
            }
            i--;
        }
    }

    async generate() {
        while (!await this.isFilled()) {
            await this.grow();
            await Utils.sleep(100)
        }
        await this.draw();
        this.updateProgress(101);
    }

    add(crystal) {
        if (crystal.y > this.crystals.length - 1 || crystal.x > this.crystals[0].length - 1 || crystal.x < 0 || crystal.y < 0) return "out";
        if (this.crystals[crystal.y][crystal.x] == null) {
            this.crystals[crystal.y][crystal.x] = crystal;
            this.filled++;
            return true;
        }
        return false;
    }

    draw() {
        this.canvasDrawer.clear();
        const crystalCopy = Utils.flatten2dArray(this.crystals);
        crystalCopy.forEach(crystal => {
            crystal && crystal.draw(this);
        });
    }

    async grow() {
        const crystalCopy = await Utils.getContentsOf2dArray(this.crystals);
        crystalCopy.forEach(crystal => !crystal.grew && crystal.grow(this));
    }

    isFilled() {
        this.updateProgress(this.filled / (this.width * this.height) * 100);
        if (this.filled >= this.width * this.height) {
            return true;
        }
        return false;
    }

    drawPoint(x, y, color) {
        this.canvasDrawer.drawPoint(x, y, color);
    }
}

class Crystal {
    growth = { up: 1, down: 1, left: 1, right: 1 };
    grew = false;
    constructor(x, y, growth, color) {
        growth && (this.growth = growth);
        this.x = x;
        this.y = y;
        this.color = color || Utils.randomGray();
    }

    async grow(surface) {
        if (this.grew) return;
        for (let i = 1; i < this.growth.up + 1; i++) {
            if (!await surface.add(this.createCopy(this.x, this.y - i))) break;
        }
        for (let i = 1; i < this.growth.down + 1; i++) {
            if (!await surface.add(this.createCopy(this.x, this.y + i))) break;
        }
        for (let i = 1; i < this.growth.left + 1; i++) {
            if (!await surface.add(this.createCopy(this.x - i, this.y))) break;
        }
        for (let i = 1; i < this.growth.right + 1; i++) {
            if (!await surface.add(this.createCopy(this.x + i, this.y))) break;
        }
        this.grew = true;
    }

    createCopy(x, y) {
        return new Crystal(x, y, this.growth, this.color);
    }

    draw(surface) {
        surface.drawPoint(this.x, this.y, this.color);
    }

}


class CanvasDrawer {
    constructor(canvas, width = 500, height = 500) {
        this.canvas = canvas;
        this.context = this.canvas?.getContext("2d");
        this.canvas.width = width;
        this.canvas.height = height;
    }

    drawPoint(x, y, color = "red") {
        this.context.fillStyle = color;
        this.context.fillRect(x, y, 1, 1);
    }

    clear() {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }

}

class Utils {
    static randomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1) + min);
    }

    static randomGray() {
        let color = Utils.randomInt(0, 180);
        return `rgb(${color}, ${color}, ${color})`;
    }

    static randomColor() {
        return `rgb(${Utils.randomInt(0, 205)}, ${Utils.randomInt(0, 205)}, ${Utils.randomInt(0, 205)})`;
    }

    static copyArray(array) {
        return array.map(x => x);
    }

    static copy2dArray(array) {
        return array.map(x => Utils.copyArray(x));
    }

    static flatten2dArray(array) {
        return array.reduce((a, b) => a.concat(b));
    }

    static getContentsOf2dArray(array) {
        let contents = [];
        let yLength = array[0].length;
        for (let x = 0; x < array.length; x++) {
            for (let y = 0; y < yLength; y++) {
                if (array[x][y] != null) contents.push(array[x][y]);
            }
        }
        return contents;
    }

    static sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

}