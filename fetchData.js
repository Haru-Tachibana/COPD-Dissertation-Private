import fetch from 'node-fetch';
import fs from 'fs';
import path from 'path';

const email = 'paloma030415@gmail.com'; // your email
const key = 'greymallard57'; // your new API key
const state = '46'; // example for South Dakota

const url = `https://aqs.epa.gov/data/api/list/countiesByState?email=${email}&key=${key}&state=${state}`;

async function fetchData() {
    try {
        console.log("Fetching data from:", url);
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("API request status:", data.Header[0].status);
        
        if (data.Header[0].status === "Success") {
            // Save to CSV
            const csvPath = path.join('/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Fetched Data', 'counties_data.csv');
            const csvContent = data.Data.map(item => `${item.code},${item.value_represented}`).join('\n');

            fs.writeFileSync(csvPath, csvContent);
            console.log("Data saved to:", csvPath);
        } else {
            console.error("Error in response:", data.Header[0].error);
        }
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

fetchData();