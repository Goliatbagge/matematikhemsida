// Graf-funktioner för Matematik 3c hemsidan

// Vänta tills DOM är laddad
document.addEventListener('DOMContentLoaded', function() {
    // Rita alla grafer när sidan laddas
    setupSekantIntroInteractive();
    setupGranplantaInteractive();
    setupAndringskvotInteractive();
    setupTangentIntroInteractive();
    setupAbsolutbeloppGraph();
});

// Gemensam layout-konfiguration för alla grafer
const commonLayout = {
    font: {
        family: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
        size: 12
    },
    paper_bgcolor: 'white',
    plot_bgcolor: '#f8f9fa',
    margin: { t: 60, r: 40, b: 60, l: 60 },
    hovermode: 'closest'
};

const commonConfig = {
    responsive: true,
    displayModeBar: true,
    displaylogo: false,
    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d', 'toImage']
};

// Graf 1: Introduktion till sekanter - INTERAKTIV med HTML sliders
function setupSekantIntroInteractive() {
    const element = document.getElementById('graph-sekant-intro');
    const slider1 = document.getElementById('sekant-x1');
    const slider2 = document.getElementById('sekant-x2');
    const value1 = document.getElementById('sekant-x1-value');
    const value2 = document.getElementById('sekant-x2-value');

    if (!element || !slider1 || !slider2) return;

    // Funktion för att uppdatera grafen
    function updateGraph() {
        const x1Val = parseFloat(slider1.value);
        const x2Val = parseFloat(slider2.value);

        // Uppdatera värdevisning
        value1.textContent = x1Val.toFixed(1);
        value2.textContent = x2Val.toFixed(1);

        // Skapa x-värden för kurvan
        const x = [];
        for (let i = -6; i <= 6; i += 0.1) {
            x.push(i);
        }

        // Skapa en parabel y = 0.2x^2 - 3
        const y = x.map(val => 0.2 * Math.pow(val, 2) - 3);

        // Kurvan
        const curve = {
            x: x,
            y: y,
            type: 'scatter',
            mode: 'lines',
            name: 'f(x) = 0.2x² - 3',
            line: {
                color: '#2196F3',
                width: 3
            }
        };

        // Punkter för sekanten
        const x1 = x1Val;
        const y1 = 0.2 * Math.pow(x1, 2) - 3;
        const x2 = x2Val;
        const y2 = 0.2 * Math.pow(x2, 2) - 3;

        // Sekanten (förlängd för att synas bättre)
        const k = (y2 - y1) / (x2 - x1);
        const m = y1 - k * x1;
        const sekantX = [-6, 6];
        const sekantY = sekantX.map(x => k * x + m);

        const secant = {
            x: sekantX,
            y: sekantY,
            type: 'scatter',
            mode: 'lines',
            name: `Sekant (k = ${k.toFixed(2)})`,
            line: {
                color: '#f44336',
                width: 2,
                dash: 'dash'
            }
        };

        // Punkter på kurvan
        const points = {
            x: [x1, x2],
            y: [y1, y2],
            type: 'scatter',
            mode: 'markers+text',
            name: 'Punkter',
            marker: {
                color: '#4CAF50',
                size: 12
            },
            text: [`(${x1.toFixed(1)}, ${y1.toFixed(1)})`, `(${x2.toFixed(1)}, ${y2.toFixed(1)})`],
            textposition: 'top center',
            textfont: {
                size: 11,
                color: '#2E7D32'
            }
        };

        const data = [curve, secant, points];

        const layout = {
            ...commonLayout,
            title: `Sekant mellan två punkter på en kurva<br><sub style="font-size: 12px;">Sekantens lutning k = ${k.toFixed(2)}</sub>`,
            xaxis: {
                title: 'x',
                zeroline: true,
                gridcolor: '#e0e0e0',
                range: [-6, 6]
            },
            yaxis: {
                title: 'y',
                zeroline: true,
                gridcolor: '#e0e0e0',
                range: [-4, 5]
            },
            showlegend: true,
            legend: {
                x: 0.02,
                y: 0.98
            }
        };

        Plotly.react(element, data, layout, commonConfig);
    }

    // Lyssna på slider-ändringar
    slider1.addEventListener('input', updateGraph);
    slider2.addEventListener('input', updateGraph);

    // Initial ritning
    updateGraph();
}

// Graf 2: Granplanta exempel - INTERAKTIV med HTML slider
function setupGranplantaInteractive() {
    const element = document.getElementById('graph-granplanta');
    const slider = document.getElementById('gran-x2');
    const valueDisplay = document.getElementById('gran-x2-value');

    if (!element || !slider) return;

    function updateGraph() {
        const x2Val = parseFloat(slider.value);

        // Uppdatera värdevisning
        valueDisplay.textContent = x2Val.toFixed(2);

        // Skapa en tillväxtkurva för granen (logaritmisk tillväxt)
        const x = [];
        const y = [];
        for (let i = 0; i <= 3.5; i += 0.05) {
            x.push(i);
            // Använd en funktion som ger y(0)≈0.5 och y(2)≈1.4
            y.push(0.5 + 0.7 * Math.log(i + 1));
        }

        // Granens tillväxtkurva
        const curve = {
            x: x,
            y: y,
            type: 'scatter',
            mode: 'lines',
            name: 'Granhöjd',
            line: {
                color: '#4CAF50',
                width: 3
            }
        };

        // Sekanten mellan x=0 och x=x2Val
        const x1 = 0, y1 = 0.5 + 0.7 * Math.log(x1 + 1);
        const x2 = x2Val, y2 = 0.5 + 0.7 * Math.log(x2 + 1);

        // Beräkna lutning och tillväxthastighet
        const k = (y2 - y1) / (x2 - x1);

        const secant = {
            x: [x1, x2],
            y: [y1, y2],
            type: 'scatter',
            mode: 'lines',
            name: `Sekant (${k.toFixed(2)} dm/år)`,
            line: {
                color: '#f44336',
                width: 2,
                dash: 'dash'
            }
        };

        // Punkter
        const points = {
            x: [x1, x2],
            y: [y1, y2],
            type: 'scatter',
            mode: 'markers+text',
            name: 'Mätpunkter',
            marker: {
                color: '#FF9800',
                size: 12
            },
            text: [`(${x1}, ${y1.toFixed(1)})`, `(${x2.toFixed(2)}, ${y2.toFixed(1)})`],
            textposition: 'top center',
            textfont: {
                size: 11,
                color: '#E65100'
            }
        };

        const data = [curve, secant, points];

        const layout = {
            ...commonLayout,
            title: `Granplantans tillväxt<br><sub style="font-size: 12px;">Genomsnittlig tillväxthastighet: ${k.toFixed(2)} dm/år</sub>`,
            xaxis: {
                title: 'Tid (år)',
                zeroline: true,
                gridcolor: '#e0e0e0',
                range: [-0.2, 3.5]
            },
            yaxis: {
                title: 'Höjd (dm)',
                zeroline: true,
                gridcolor: '#e0e0e0',
                range: [-0.2, 2.5]
            },
            showlegend: true,
            legend: {
                x: 0.02,
                y: 0.98
            }
        };

        Plotly.react(element, data, layout, commonConfig);
    }

    // Lyssna på slider-ändringar
    slider.addEventListener('input', updateGraph);

    // Initial ritning
    updateGraph();
}

// Graf 3: Ändringskvot för f(x) = x^2 - INTERAKTIV med HTML sliders
function setupAndringskvotInteractive() {
    const element = document.getElementById('graph-andringsk');
    const slider1 = document.getElementById('andring-x1');
    const slider2 = document.getElementById('andring-x2');
    const value1 = document.getElementById('andring-x1-value');
    const value2 = document.getElementById('andring-x2-value');

    if (!element || !slider1 || !slider2) return;

    function updateGraph() {
        const x1Val = parseFloat(slider1.value);
        const x2Val = parseFloat(slider2.value);

        // Uppdatera värdevisning
        value1.textContent = x1Val.toFixed(1);
        value2.textContent = x2Val.toFixed(1);

        // Skapa x-värden för kurvan
        const x = [];
        for (let i = 0; i <= 7; i += 0.1) {
            x.push(i);
        }

        // f(x) = x^2
        const y = x.map(val => Math.pow(val, 2));

        // Kurvan
        const curve = {
            x: x,
            y: y,
            type: 'scatter',
            mode: 'lines',
            name: 'f(x) = x²',
            line: {
                color: '#673AB7',
                width: 3
            }
        };

        // Punkter för sekanten
        const x1 = x1Val, y1 = Math.pow(x1, 2);
        const x2 = x2Val, y2 = Math.pow(x2, 2);

        // Sekanten
        const k = (y2 - y1) / (x2 - x1);
        const m = y1 - k * x1;
        const sekantX = [Math.max(0, x1 - 1), Math.min(7, x2 + 1)];
        const sekantY = sekantX.map(x => k * x + m);

        const secant = {
            x: sekantX,
            y: sekantY,
            type: 'scatter',
            mode: 'lines',
            name: `Sekant (k = ${k.toFixed(2)})`,
            line: {
                color: '#f44336',
                width: 2,
                dash: 'dash'
            }
        };

        // Punkter på kurvan
        const points = {
            x: [x1, x2],
            y: [y1, y2],
            type: 'scatter',
            mode: 'markers+text',
            name: 'Punkter',
            marker: {
                color: '#FF9800',
                size: 12
            },
            text: [`(${x1.toFixed(1)}, ${y1.toFixed(1)})`, `(${x2.toFixed(1)}, ${y2.toFixed(1)})`],
            textposition: 'top center',
            textfont: {
                size: 11,
                color: '#E65100'
            }
        };

        const data = [curve, secant, points];

        const layout = {
            ...commonLayout,
            title: `Ändringskvot för f(x) = x²<br><sub style="font-size: 12px;">k = Δy/Δx = (${y2.toFixed(1)} - ${y1.toFixed(1)}) / (${x2.toFixed(1)} - ${x1.toFixed(1)}) = ${k.toFixed(2)}</sub>`,
            xaxis: {
                title: 'x',
                zeroline: true,
                gridcolor: '#e0e0e0',
                range: [0, 7]
            },
            yaxis: {
                title: 'f(x)',
                zeroline: true,
                gridcolor: '#e0e0e0',
                range: [0, 50]
            },
            showlegend: true,
            legend: {
                x: 0.02,
                y: 0.98
            }
        };

        Plotly.react(element, data, layout, commonConfig);
    }

    // Lyssna på slider-ändringar
    slider1.addEventListener('input', updateGraph);
    slider2.addEventListener('input', updateGraph);

    // Initial ritning
    updateGraph();
}

// Graf 4: Tangent intro - INTERAKTIV med HTML slider
function setupTangentIntroInteractive() {
    const element = document.getElementById('graph-tangent-intro');
    const slider = document.getElementById('tangent-h');
    const valueDisplay = document.getElementById('tangent-h-value');

    if (!element || !slider) return;

    function updateGraph() {
        const h = parseFloat(slider.value);

        // Uppdatera värdevisning
        valueDisplay.textContent = h.toFixed(2);

        // Skapa x-värden för kurvan
        const x = [];
        for (let i = -1; i <= 5; i += 0.1) {
            x.push(i);
        }

        // f(x) = x^2
        const y = x.map(val => Math.pow(val, 2));

        // Kurvan
        const curve = {
            x: x,
            y: y,
            type: 'scatter',
            mode: 'lines',
            name: 'f(x) = x²',
            line: {
                color: '#2196F3',
                width: 3
            }
        };

        // Fix punkt vid x=2
        const x1 = 2, y1 = 4;
        const x2 = x1 + h, y2 = Math.pow(x2, 2);

        // Sekanten/tangenten
        const k = (y2 - y1) / h;
        const m = y1 - k * x1;
        const lineX = [0, 5];
        const lineY = lineX.map(x => k * x + m);

        const line = {
            x: lineX,
            y: lineY,
            type: 'scatter',
            mode: 'lines',
            name: h < 0.5 ? `Tangent (k = ${k.toFixed(2)})` : `Sekant (k = ${k.toFixed(2)})`,
            line: {
                color: h < 0.5 ? '#4CAF50' : '#f44336',
                width: 2,
                dash: h < 0.5 ? 'solid' : 'dash'
            }
        };

        // Punkter
        const points = {
            x: [x1, x2],
            y: [y1, y2],
            type: 'scatter',
            mode: 'markers',
            name: 'Punkter',
            marker: {
                color: '#FF9800',
                size: 12
            }
        };

        const data = [curve, line, points];

        const layout = {
            ...commonLayout,
            title: `${h < 0.5 ? 'Tangent' : 'Sekant'} till f(x) = x²<br><sub style="font-size: 12px;">h = ${h.toFixed(2)}, lutning k = ${k.toFixed(2)}</sub>`,
            xaxis: {
                title: 'x',
                zeroline: true,
                gridcolor: '#e0e0e0',
                range: [-0.5, 5]
            },
            yaxis: {
                title: 'y',
                zeroline: true,
                gridcolor: '#e0e0e0',
                range: [-1, 20]
            },
            showlegend: true,
            legend: {
                x: 0.02,
                y: 0.98
            }
        };

        Plotly.react(element, data, layout, commonConfig);
    }

    // Lyssna på slider-ändringar
    slider.addEventListener('input', updateGraph);

    // Initial ritning
    updateGraph();
}

// Graf 5: Absolutbelopp - statisk graf
function setupAbsolutbeloppGraph() {
    const element = document.getElementById('graph-absolutbelopp');

    if (!element) return;

    // Skapa x-värden
    const x = [];
    for (let i = -5; i <= 5; i += 0.1) {
        x.push(i);
    }

    // f(x) = |x|
    const y = x.map(val => Math.abs(val));

    // Kurvan
    const curve = {
        x: x,
        y: y,
        type: 'scatter',
        mode: 'lines',
        name: 'f(x) = |x|',
        line: {
            color: '#E91E63',
            width: 3
        }
    };

    // Markera hörnet vid x=0
    const corner = {
        x: [0],
        y: [0],
        type: 'scatter',
        mode: 'markers',
        name: 'Hörn (ej deriverbar)',
        marker: {
            color: '#f44336',
            size: 15,
            symbol: 'x'
        }
    };

    const data = [curve, corner];

    const layout = {
        ...commonLayout,
        title: 'f(x) = |x| - Absolutbeloppsfunktionen',
        xaxis: {
            title: 'x',
            zeroline: true,
            gridcolor: '#e0e0e0',
            range: [-5, 5]
        },
        yaxis: {
            title: 'f(x)',
            zeroline: true,
            gridcolor: '#e0e0e0',
            range: [-1, 5]
        },
        showlegend: true,
        legend: {
            x: 0.02,
            y: 0.98
        }
    };

    Plotly.newPlot(element, data, layout, commonConfig);
}

console.log('Interaktiva grafer laddade!');
