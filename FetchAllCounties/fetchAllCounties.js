import fs from 'fs';
import path from 'path';
import fetch from 'node-fetch';
import csv from 'csv-parser';

// Constants
const USER_ID = 'paloma030415@gmail.com'; // Your email
const API_KEY = 'greymallard57'; // Your API key
const PARAMS = '88101,88502'; // PM2.5 parameter codes (FRM/FEM and non-FRM)
const INPUT_CSV_PATH = '/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Fetched Data/counties_data.csv'; // Path to your CSV file
const OUTPUT_CSV_PATH = '/Users/yangyangxiayule/Documents/GitHub/COPD-Project/Fetched Data/pm25_data_by_county_2018.csv'; // Output file path

let consolidatedData = [];

// Function to fetch quarterly data for a specific county
async function fetchQuarterlyDataByCounty(countyCode, countyName) {
    let countyData = { County: countyName }; // Start with the county name

    // Construct the URL for the specific year
    const url = `https://aqs.epa.gov/data/api/quarterlyData/byCounty?email=${USER_ID}&key=${API_KEY}&param=${PARAMS}&bdate=20180101&edate=20181231&state=46&county=${countyCode}`;

    try {
        const response = await fetch(url);
        const data = await response.json();

        // Check if no data was found
        if (data.Header[0].status === 'No data matched your selection') {
            console.log(`No data for ${countyName}`);
            // Populate with nulls for missing data
            for (let i = 1; i <= 4; i++) {
                countyData[`Q${i}_Data`] = null;
            }
        } else {
            // Extract quarterly PM2.5 data for the year
            data?.Data?.forEach((item, index) => {
                countyData[`Q${index + 1}_Data`] = item.arithmetic_mean; // Assuming 'arithmetic_mean' holds PM2.5 values
            });
        }

    } catch (error) {
        console.error(`Error fetching quarterly data for ${countyName}: ${error}`);
        // If an error occurs, store nulls for all quarters
        for (let i = 1; i <= 4; i++) {
            countyData[`Q${i}_Data`] = null;
        }
    }

    consolidatedData.push(countyData); // Add the county data to consolidated data
}

// Function to read county data from CSV
function readCountyData() {
    return new Promise((resolve, reject) => {
        const counties = [];

        fs.createReadStream(INPUT_CSV_PATH)
            .pipe(csv())
            .on('data', (row) => {
                counties.push({ county: row.County, code: row.Code }); // Assuming columns 'County', 'Code'
            })
            .on('end', () => {
                resolve(counties);
            })
            .on('error', reject);
    });
}

// Function to write consolidated data to CSV
function writeDataToCSV() {
    const header = ['County', 'Q1_Data', 'Q2_Data', 'Q3_Data', 'Q4_Data'];
    const csvData = [header, ...consolidatedData.map(row => header.map(col => row[col] || ''))];

    const csvString = csvData.map(row => row.join(',')).join('\n');
    fs.writeFileSync(OUTPUT_CSV_PATH, csvString);
    console.log(`Data saved to ${OUTPUT_CSV_PATH}`);
}

// Main function to execute fetching
async function main() {
    try {
        const counties = await readCountyData(); // Read county data from CSV

        // Fetch data for each county
        for (const county of counties) {
            await fetchQuarterlyDataByCounty(county.code, county.county);
        }

        writeDataToCSV(); // Write the fetched data to a CSV file
    } catch (error) {
        console.error(`Error: ${error}`);
    }
}

main();