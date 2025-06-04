const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');

const client = new Client({
    authStrategy: new LocalAuth(), // Guarda la sesión en tu disco
    puppeteer: {
        headless: false // Cambia a true si no quieres que se abra el navegador
    }
});

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true }); // Muestra el QR en la terminal
});

client.on('ready', () => {
    console.log('✅ Cliente conectado y listo!');
});

client.on('message', async (message) => {
    const texto = message.body.toLowerCase();
    if (texto.includes("lts") || texto.includes("saldo")) {
        const fecha = new Date(message.timestamp * 1000).toLocaleString();
        console.log(`[${fecha}] ${message.from}: ${message.body}`);
        fs.appendFileSync('litros.log', `[${fecha}] ${message.body}\n`);
    }
});

client.initialize();
