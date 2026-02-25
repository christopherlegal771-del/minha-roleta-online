from flask import Flask, render_template_string

app = Flask(__name__)

# Este é o design do site (HTML + CSS + JS da Roleta)
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Roleta Cromática</title>
    <style>
        body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; background: #222; color: white; }
        canvas { border-radius: 50%; box-shadow: 0 0 20px rgba(0,0,0,0.5); margin: 20px; }
        .controls { margin-top: 20px; text-align: center; }
        textarea { width: 300px; height: 100px; border-radius: 8px; padding: 10px; }
        #spin { 
            background: #ff4500; color: white; border: none; padding: 15px 40px; 
            font-size: 20px; border-radius: 50px; cursor: pointer; font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>Roleta de Nomes</h1>
    <canvas id="wheel" width="400" height="400"></canvas>
    <div class="controls">
        <p>Digite os nomes (um por linha):</p>
        <textarea id="names">Item 1\nItem 2\nItem 3\nItem 4\nItem 5</textarea><br><br>
        <button id="spin">GIRAR (SPIN)</button>
    </div>

    <script>
        const canvas = document.getElementById("wheel");
        const ctx = canvas.getContext("2d");
        const spinBtn = document.getElementById("spin");
        const namesInput = document.getElementById("names");

        let currentRotation = 0;

        function drawWheel() {
            const names = namesInput.value.split('\\n').filter(n => n.trim() !== "");
            if (names.length === 0) return;

            const arc = (2 * Math.PI) / names.length;
            ctx.clearRect(0, 0, 400, 400);

            names.forEach((name, i) => {
                const angle = currentRotation + i * arc;
                // Cores do círculo cromático
                ctx.fillStyle = `hsl(${(i * 360) / names.length}, 70%, 50%)`;
                ctx.beginPath();
                ctx.moveTo(200, 200);
                ctx.arc(200, 200, 200, angle, angle + arc);
                ctx.fill();
                ctx.stroke();

                // Texto
                ctx.save();
                ctx.translate(200, 200);
                ctx.rotate(angle + arc / 2);
                ctx.fillStyle = "white";
                ctx.font = "bold 16px Arial";
                ctx.fillText(name.substring(0, 15), 70, 5);
                ctx.restore();
            });
        }

        spinBtn.onclick = () => {
            const extraRotation = Math.random() * 3600 + 1000;
            let start = null;
            const duration = 4000;

            function animate(timestamp) {
                if (!start) start = timestamp;
                const progress = timestamp - start;
                const easeOut = 1 - Math.pow(1 - progress / duration, 3);
                currentRotation += (extraRotation / 100) * (1 - easeOut);
                drawWheel();
                if (progress < duration) requestAnimationFrame(animate);
            }
            requestAnimationFrame(animate);
        };

        namesInput.oninput = drawWheel;
        drawWheel();
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    app.run(debug=True)