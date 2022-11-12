// Umsetzung der Funktionen für die Generierung eines Musters über die Web
window.onload = function () {
    let surface = null;
    document.getElementById("generate").addEventListener("click", function () {

        function updateProgress(progress) {
            document.getElementsByClassName('display')[0].style = `--height: ${progress}%`;
            if (progress == 101) {
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
                angle: {
                    min: parseInt(document.getElementById("growth_angle_min").value) || 0,
                    max: parseInt(document.getElementById("growth_angle_max").value) || 360
                },
                rate: {
                    min: parseInt(document.getElementById("growth_rate_min").value) || 1,
                    max: parseInt(document.getElementById("growth_rate_max").value) || 10
                },
                opposite: {
                    min: parseInt(document.getElementById("growth_opposite_min").value) / 100 || 0.01,
                    max: parseInt(document.getElementById("growth_opposite_max").value) / 100 || 0.5
                },
                time: {
                    min: parseInt(document.getElementById("growth_time_min").value) || 1,
                    max: parseInt(document.getElementById("growth_time_max").value) || 1
                }
            },
            updateProgress
        });
        surface.generate();
    });
};

// Repräsentiert die Oberfläche auf der das Muster generiert wird
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

    // Startkristalle bzw. Keime erstellen
    create(amount, settings) {
        for (let i = 0; i < amount; i++) {
            let x = Utils.randomInt((this.width - settings.spawn.width) / 2, (this.width + settings.spawn.width) / 2 - 1);
            let y = Utils.randomInt((this.height - settings.spawn.height) / 2, (this.height + settings.spawn.height) / 2 - 1);
            let growthData = {
                angle: Utils.random(settings.growth.angle.min, settings.growth.angle.max),
                growthRate: Utils.random(settings.growth.rate.min, settings.growth.rate.max),
                oppositeGrowth: Utils.random(settings.growth.opposite.min, settings.growth.opposite.max),
            }

            let growth = {
                x: Utils.notZero(Math.cos(growthData.angle) * growthData.growthRate),
                y: Utils.notZero(Math.sin(growthData.angle) * growthData.growthRate)
            }

            let computedGrowth = {
                up: Math.ceil(Math.abs(growth.y > 0 ? growth.y : growth.y * growthData.oppositeGrowth)),
                down: Math.ceil(Math.abs(growth.y < 0 ? growth.y : growth.y * growthData.oppositeGrowth)),
                left: Math.ceil(Math.abs(growth.x < 0 ? growth.x : growth.x * growthData.oppositeGrowth)),
                right: Math.ceil(Math.abs(growth.x > 0 ? growth.x : growth.x * growthData.oppositeGrowth))
            }
            let color = Utils.getGray(growthData.angle);

            let time = Utils.randomInt(settings.growth.time.min, settings.growth.time.max);
            if (this.crystals[y][x] == null) {
                this.crystals[y][x] = new Crystal(x, y, computedGrowth, time, color);
                this.filled++;
                continue;
            }
            i--;
        }
    }

    // Kristalle generieren
    async generate() {
        while (!await this.isFilled()) {
            await this.grow();
            await Utils.sleep(100)
        }
        await this.draw();
        this.updateProgress(101);
    }

    // Kristall erstellen, wenn an der Stelle noch keiner ist
    add(crystal) {
        if (crystal.y > this.crystals.length - 1 || crystal.x > this.crystals[0].length - 1 || crystal.x < 0 || crystal.y < 0) return false;
        if (this.crystals[crystal.y][crystal.x] == null || this.crystals[crystal.y][crystal.x].time > 1) {
            (this.crystals[crystal.y][crystal.x] == null) && this.filled++;
            this.crystals[crystal.y][crystal.x] = crystal;
            crystal.draw(this);
            return true;
        }
        return false;
    }

    // Aktuelle Kristalle zeichnen
    draw() {
        this.canvasDrawer.clear();
        const crystalCopy = Utils.flatten2dArray(this.crystals);
        crystalCopy.forEach(crystal => {
            crystal && crystal.draw(this);
        });
    }

    // Kristalle wachsen lassen
    async grow() {
        const crystalCopy = await Utils.getContentsOf2dArray(this.crystals);
        crystalCopy.forEach(crystal => !crystal.grew && crystal.grow(this));
    }

    // Überprüfen, ob das Feld voll ist
    isFilled() {
        if (this.getLevel() >= 100) return true;
        return false;
    }

    // Füllgrad des Feldes berechnen
    getLevel() {
        let level = this.filled / (this.width * this.height) * 100;
        this.updateProgress(level); // Füllgrad in Web-App anzeigen
        return level;
    }

    // Kristall zeichenen (Übergabe an CanvasDrawer)
    drawPoint(x, y, color) {
        this.canvasDrawer.drawPoint(x, y, color);
    }
}


// Represaentiert einen einzelnen Kristall (Pixel auf dem Canvas)
class Crystal {
    growth = { up: 1, down: 1, left: 1, right: 1 };
    grew = false;

    constructor(x, y, growth, time, color) {
        growth && (this.growth = growth);
        this.x = x;
        this.y = y;
        this.time = time || 1;
        this.color = color || Utils.randomGray();
    }

    // Kristall wachsen lassen
    async grow(surface) {
        this.time--;
        if (this.time > 0) return;
        if (this.grew) return;
        this.grew = true;

        // Wachstum nach oben
        for (let i = 1; i < this.growth.up + 1; i++) {
            if (!await surface.add(this.createCopy(this.x, this.y - i))) break;
        }

        // Wachstum nach unten
        for (let i = 1; i < this.growth.down + 1; i++) {
            if (!await surface.add(this.createCopy(this.x, this.y + i))) break;
        }

        // Wachstum nach links
        for (let i = 1; i < this.growth.left + 1; i++) {
            if (!await surface.add(this.createCopy(this.x - i, this.y))) break;
        }

        // Wachstum nach rechts
        for (let i = 1; i < this.growth.right + 1; i++) {
            if (!await surface.add(this.createCopy(this.x + i, this.y))) break;
        }
    }

    // Erstellt eine Kopie des Kristalls
    createCopy(x, y) {
        return new Crystal(x, y, this.growth, 1, this.color);
    }

    // Zeichnet den Kristall
    draw(surface) {
        surface.drawPoint(this.x, this.y, this.color);
    }

}


// Hilfsfunktionen zum Zeichnen auf einem Canvas
class CanvasDrawer {
    constructor(canvas, width = 500, height = 500) {
        this.canvas = canvas;
        this.context = this.canvas?.getContext("2d");
        this.canvas.width = width;
        this.canvas.height = height;
    }

    // Zeichnet einen Punkt
    drawPoint(x, y, color = "red") {
        this.context.fillStyle = color;
        this.context.fillRect(x, y, 1, 1);
    }

    // Löscht den Canvas
    clear() {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }

}

// Hilfsfunktionen
class Utils {


    // Zufallszahl zwischen min und max
    static random(min, max) {
        return Math.random() * (max - min) + min;
    }

    // Ganzzahlige Zufallszahl zwischen min und max
    static randomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1) + min);
    }

    // Grautonfarbe in Abhängigkeit des Winkels
    static getGray(angle) {
        let color = Math.floor(55 + (angle / 360) * 170);
        return `rgb(${color}, ${color}, ${color})`;
    }

    // 2d-Array in 1d-Array umwandeln
    static flatten2dArray(array) {
        return array.reduce((a, b) => a.concat(b));
    }

    // Alle Inhalte eines 2d-Arrays
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

    // Warten für async Funktionen
    static sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // Zahl nicht gleich 0
    static notZero(value) {
        return value > 0 ? Math.max(value, 0.01) : Math.min(value, 0.01);
    }

}