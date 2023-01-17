const express = require('express');
const app = express();
const fetch = require('node-fetch');

app.get('/entries', (req, res) => {
    const category = req.query.category;
    fetch(`https://api.publicapis.org/entries?category=${category}`)
        .then(response => response.json())
        .then(data => {
            const entries = data.entries.map(entry => {
                return {
                    API: entry.API,
                    Description: entry.Description
                }
            });
            res.status(200).json({ entries });
        })
        .catch(error => {
            console.log(error);
            res.status(500).json({ error });
        });
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
