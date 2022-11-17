// Umsetzung der Funktionen für die Generierung eines Musters über die Web
window.onload = function () {
    let surface = null;
    document.getElementById("generate").addEventListener("click", function () {

        function updateProgress(progress) {
            document.getElementsByClassName('display')[0].style = `--height: ${progress * 100}%`;
            if (progress == 101) {
                document.getElementsByClassName('display')[0].style = `--height: 0%`;
            }
        }

        surface = new Generator(document.getElementsByClassName('canvas')[0], {
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
            update: updateProgress
        });
        surface.generate();
    });
};