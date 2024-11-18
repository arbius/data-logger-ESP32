const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');  // Import the path module
const readline = require('readline');



const app = express();
const port = 3000;

app.use(express.static(path.join(__dirname, 'public')));


// Middleware to parse incoming JSON requests
app.use(bodyParser.json());

// Route to handle POST requests to /time with JSON data
app.post('/time', (req, res) => {
    const jsonData = req.body;
    // console.log('jsonData', jsonData)
    
    // Convert the incoming JSON data to a string and add a newline for separation
    const dataToAppend = JSON.stringify(jsonData) + '\n';
    // console.log('dataToAppend', dataToAppend)
    // Append the data to the file
    fs.appendFile('time.json', dataToAppend, (err) => {
        if (err) {
            console.error('Error appending to file:', err);
            return res.status(500).send('Error appending to file');
        }

        console.log(`Data received and appended to file successfully ${jsonData.iso_timestamp} ${jsonData.temperature}F ${jsonData.humidity}%`);
        // console.log(`Last entry ISO Timestamp: ${jsonData.iso_timestamp}`);

        // res.send('Data appended successfully!');
        res.send(`Data appended successfully!, Timestamp: ${jsonData.iso_timestamp}`)
      });
      
    });

// Endpoint to get the last entry in a JSON file
app.get('/last-entry', (req, res) => {
    const filePath = path.join(__dirname, 'time.json');  // Path to your JSON file
    
    // Check if the file exists before proceeding
    if (!fs.existsSync(filePath)) {
      return res.status(404).json({ message: 'No data exists yet. Please try again later.' });
    }

    // Create a readline interface to read the file line by line
    const readInterface = readline.createInterface({
      input: fs.createReadStream(filePath),
      console: false
    });
  
    let lastEntry = null;  // To hold the last valid JSON object
  
    // Process each line of the file
    readInterface.on('line', (line) => {
      try {
        // Parse the line as JSON
        const jsonData = JSON.parse(line.trim());
  
        // Update the lastEntry with the most recent valid JSON
        lastEntry = jsonData;
      } catch (err) {
        console.error('Error parsing line as JSON:', err);
      }
    });
  
    // When reading is complete, send the last entry as a response
    readInterface.on('close', () => {
        if (lastEntry) {
            // Send only the iso_timestamp, temperature, and humidity
            res.json({
              timeStamp: lastEntry.iso_timestamp,  // Use the iso_timestamp from the JSON
              temperature: lastEntry.temperature,
              humidity: lastEntry.humidity
            });
          } else {        res.status(404).json({ message: 'No valid data found in the file' });
      }
    });
  });

  // Endpoint to get paginated entries from the JSON file
app.get('/entries', (req, res) => {
  const filePath = path.join(__dirname, 'time.json');  // Path to your JSON file
  
  // Check if the file exists before proceeding
  if (!fs.existsSync(filePath)) {
      return res.status(404).json({ message: 'No data exists yet. Please try again later.' });
  }

  const page = parseInt(req.query.page) || 1;  // Current page, default to 1
  const pageSize = parseInt(req.query.pageSize) || 10;  // Entries per page, default to 10

  const startLine = (page - 1) * pageSize;
  const endLine = startLine + pageSize;

  const readInterface = readline.createInterface({
      input: fs.createReadStream(filePath),
      console: false
  });

  let currentLine = 0;
  const entries = [];

  readInterface.on('line', (line) => {
      if (currentLine >= startLine && currentLine < endLine) {
          try {
              const jsonData = JSON.parse(line.trim());
              // Extract only timestamp, temperature, and humidity
              const entry = {
                  timestamp: jsonData.iso_timestamp,
                  temperature: jsonData.temperature,
                  humidity: jsonData.humidity
              };
                
              entries.push(entry);
          } catch (err) {
              console.error('Error parsing line as JSON:', err);
          }
      }
      currentLine++;
  });

  readInterface.on('close', () => {
      if (entries.length > 0) {
          res.json({
              page,
              pageSize,
              entries
          });
      } else {
          res.status(404).json({ message: 'No data found for the requested page.' });
      }
  });
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
