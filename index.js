const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const path = require('path');

const LOG_DIR = path.join(__dirname, 'logs');
const LOG_FILE = path.join(LOG_DIR, 'litros.log');

// Aseguramos que exista la carpeta de logs
if (!fs.existsSync(LOG_DIR)) {
    fs.mkdirSync(LOG_DIR);
}

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: false, // true si no quieres ver la ventana
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
});

client.on('ready', async () => {
    console.log('✅ Cliente conectado y listo!');
    console.log('🔍 Revisando historial del grupo "DRIVE"...');

    try {
        const chats = await client.getChats();
        const grupo = chats.find(chat => chat.name === "DRIVE");

        if (!grupo) {
            console.warn('⚠️ Grupo "DRIVE" no encontrado.');
            return;
        }

        const messages = await grupo.fetchMessages({ limit: 50 });

        for (const msg of messages) {
            if (msg.body.toLowerCase().includes("saldo") || msg.body.toLowerCase().includes("lts")) {
                const fecha = new Date(msg.timestamp * 1000).toLocaleString();
                const texto = `[HIST] ${fecha} - ${msg.fromMe ? 'YO' : msg.author}: ${msg.body}`;
                console.log(texto);
                fs.appendFileSync(LOG_FILE, texto + '\n');
            }
        }
    } catch (err) {
        console.error('❌ Error al buscar mensajes del grupo:', err.message);
    }

    console.log('🟢 Bot escuchando nuevos mensajes...\n');
});

client.on('message', async (message) => {
    const texto = message.body.toLowerCase();
    if (texto.includes("lts") || texto.includes("saldo")) {
        const fecha = new Date(message.timestamp * 1000).toLocaleString();
        const log = `[LIVE] ${fecha} - ${message.from}: ${message.body}`;
        console.log(log);
        fs.appendFileSync(LOG_FILE, log + '\n');
    }
});

client.initialize();
