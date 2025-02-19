// If your Node.js version doesn't support fetch, install node-fetch and uncomment the following line:
// const fetch = require('node-fetch');

const fs = require('fs');
const path = require('path');

// Chartmetric API Access Token
const ACCESS_TOKEN = 'ACCESS_TOKEN_HERE';

// List of Chartmetric Artist IDs
const artistIds = [
  781320, 10281098, 3651398, 834, 384142, 1011054, 717312, 3923533,
  207335, 217633, 3167, 9990449, 3972463, 3544186, 4373808, 8812446,
  12653520, 208137, 751087, 1653887, 1525222, 1404155, 260988,
  3730441, 493676, 1348885, 691085, 4550, 4934, 538222, 3883672,
  1939, 10440582, 7946705, 4539948
];

/*
  AUTOMATIC CONFIGURATION GENERATION:
  Instead of manually changing the configuration each month, the following code automatically
  generates the configurations for the last four months.

  - It uses today's date and loops back 1 to 4 months.
  - The day is set to 13 as a consistent reference date.
  - The date is formatted as YYYY-MM-DD.
  - A label is created using a short month abbreviation (e.g., "dec") plus the last two digits of the year.
  - A folder name is generated based on the label.
*/

const configs = [];
const today = new Date();
const monthNames = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"];

for (let i = 1; i <= 4; i++) {
  // Create a date for the i-th previous month, using the 13th day as a reference.
  let d = new Date(today.getFullYear(), today.getMonth() - i, 13);
  
  // Get year, month, and day components.
  let year = d.getFullYear();
  let month = d.getMonth() + 1; // JavaScript months are 0-indexed.
  let day = d.getDate();

  // Format month and day with two digits.
  let monthStr = month.toString().padStart(2, '0');
  let dayStr = day.toString().padStart(2, '0');
  let dateStr = `${year}-${monthStr}-${dayStr}`;

  // Create a label like "dec24" using the month abbreviation and the last two digits of the year.
  let label = monthNames[d.getMonth()] + year.toString().slice(-2);

  // Define the folder name using the label.
  let folderName = `ch_artist_tt_audience_data_${label}`;

  // Add the configuration object to the array.
  configs.push({
    label: label,
    date: dateStr,
    folderName: folderName
  });
}

/*
  FUNCTION: fetchAndSaveArtistData
  This function fetches the TikTok audience data for one artist using a specific configuration.
  - It constructs the API URL using the artist's ID and the date from the config.
  - It ensures the target folder exists (creating it if needed).
  - It writes the fetched JSON data into a file named with the artist ID and label.
*/
async function fetchAndSaveArtistData(artistId, config) {
  const { date, label, folderName } = config;
  const dataFolder = path.join(process.cwd(), folderName);

  // Ensure the directory exists; if not, create it.
  if (!fs.existsSync(dataFolder)) {
    fs.mkdirSync(dataFolder);
  }

  // Build the API URL with the current artistId and date.
  const url = `https://api.chartmetric.com/api/artist/${artistId}/tiktok-audience-stats?date=${date}`;
  const headers = { Authorization: `Bearer ${ACCESS_TOKEN}` };

  try {
    console.log(`Fetching data for artist ID ${artistId} for ${label}...`);
    const response = await fetch(url, { headers });
    console.log('Response Status:', response.status);

    // Check if the response is successful.
    if (!response.ok) {
      const errorBody = await response.text();
      console.error(`Error for artist ID ${artistId}:`, errorBody);
      throw new Error(`Failed to fetch data for artist ID ${artistId}: ${response.statusText}`);
    }

    const data = await response.json();
    // Define the file name for saving the data.
    const fileName = `artist_${artistId}_tt_audience_data_${label}.json`;
    const filePath = path.join(dataFolder, fileName);

    // Save the JSON data to the file.
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
    console.log(`Data for artist ID ${artistId} saved to ${filePath}`);
  } catch (error) {
    console.error(`Error fetching data for artist ID ${artistId}:`, error.message);
  }
}

/*
  FUNCTION: main
  This function iterates through each configuration and, for each one, fetches the data
  for every artist in the list.
*/
async function main() {
  for (const config of configs) {
    console.log(`\nStarting task for ${config.label} data...`);
    for (const artistId of artistIds) {
      await fetchAndSaveArtistData(artistId, config);
    }
  }
}

// Run the main function.
main();
