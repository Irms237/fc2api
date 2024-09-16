const express = require('express');
const path = require('path');
const app = express();
const port = 3000; // Anda bisa mengganti dengan port yang Anda inginkan

// Tentukan direktori statis tempat file update.sh disimpan
app.use(express.static(path.join(__dirname, 'public')));

// Atur route untuk file update.sh
app.get('/update.sh', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'update.sh'));
});

// Jalankan server
app.listen(port, () => {
  console.log(`Server berjalan di http://localhost:${port}`);
});

