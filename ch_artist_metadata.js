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

// Directory to save JSON files
const dataFolder = path.join(process.cwd(), 'ch_artist_metadata');

// Ensure the directory exists
if (!fs.existsSync(dataFolder)) {
  fs.mkdirSync(dataFolder);
}

// Fetch and save artist metadata
async function fetchAndSaveArtistData(artistId) {
  const url = `https://api.chartmetric.com/api/artist/${artistId}`;
  const headers = { Authorization: `Bearer ${ACCESS_TOKEN}` };

  try {
    const response = await fetch(url, { headers });
    if (!response.ok) {
      throw new Error(`Failed to fetch data for artist ID ${artistId}: ${response.statusText}`);
    }
    const data = await response.json();

    // Generate a filename based on the artist name or ID
    const fileName = `artist_${artistId}_metadata.json`;
    const filePath = path.join(dataFolder, fileName);

    // Save JSON data to file
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
    console.log(`Data for artist ID ${artistId} saved to ${filePath}`);
  } catch (error) {
    console.error(`Error fetching data for artist ID ${artistId}:`, error.message);
  }
}

// Main function to process all artist IDs
async function main() {
  for (const artistId of artistIds) {
    await fetchAndSaveArtistData(artistId);
  }
}

main();