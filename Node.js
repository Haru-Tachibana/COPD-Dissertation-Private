const fetch = require('node-fetch'); // Import node-fetch for making HTTP requests
const fs = require('fs');            // Import file system module for writing files

// API endpoint
const apiUrl = 'https://aqs.epa.gov/data/api/list/countiesByState?email=test@aqs.api&key=test&state=46';

// Function to convert JSON to CSV
function jsonToCsv(jsonData) {
    const array = typeof jsonData !== 'object' ? JSON.parse(jsonData) : jsonData;
    let csvStr = '';

    // Get the headers
    const headers = Object.keys(array[0]);
    csvStr += headers.join(',') + '\n';

    // Loop through each object in the JSON data
    array.forEach(item => {
        let line = '';
        headers.forEach((header, index) => {
            if (index > 0) line += ',';
            line += item[header];
        });
        csvStr += line + '\n';
    });

    return csvStr;
}

// Function to save CSV file at specified path
function saveCsvFile(csvStr, filepath) {
    fs.writeFileSync(filepath, csvStr, 'utf8');
    console.log(`File saved at ${filepath}`);
}

// Fetch data from API, convert to CSV, and save to file
fetch(apiUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();  // Parse the JSON data
    })
    .then(data => {
        if (Array.isArray(data) && data.length > 0) {
            const csvStr = jsonToCsv(data);
            const filepath = './counties_data.csv'; // Set the path to save CSV file
            saveCsvFile(csvStr, filepath);
        } else {
            console.error('Invalid or empty JSON response.');
        }
    })
    .catch(error => console.error('Error fetching data:', error));