const express = require('express');
const app = express();
const fetch = require('node-fetch');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');

app.use(bodyParser.json());

const EntrySchema = new mongoose.Schema({
    API: {
        type: String,
        required: true
    },
    Description: {
        type: String,
        required: true
    },
    Auth: {
        type: String,
        required: true
    },
    HTTPS: {
        type: Boolean,
        required: true
    },
    Cors: {
        type: String,
        required: true
    },
    Link: {
        type: String,
        required: true
    },
    Category: {
        type: String,
        required: true
    }
});

const Entry = mongoose.model('Entry', EntrySchema);

app.post('/entries', (req, res) => {
    const entry = req.body;
    fetch(`https://api.publicapis.org/entries?title=${entry.API}`)
        .then(response => response.json())
        .then(data => {
            const newEntry = new Entry({
                API: data.entries[0].API,
                Description: data.entries[0].Description,
                Auth: data.entries[0].Auth,
                HTTPS: data.entries[0].HTTPS,
                Cors: data.entries[0].Cors,
                Link: data.entries[0].Link,
                Category: data.entries[0].Category
            });
            newEntry.save()
                .then(() => res.status(201).json({ message: 'API entry saved successfully' }))
                .catch(error => {
                    console.log(error);
                    res.status(500).json({ error });
                });
        })
        .catch(error => {
            console.log(error);
            res.status(500).json({ error });
        });
});

mongoose.connect('mongodb://localhost:27017/entries', { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => {
        app.listen(3000, () => {
            console.log('Server running on port 3000');
        });
    })
    .catch(error => {
        console.log(error);
    });
