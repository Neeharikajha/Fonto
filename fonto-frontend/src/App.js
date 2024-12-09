import React, { useState } from 'react';
import Homepage from './components/Homepage'; // Import Homepage component

const App = () => {
  // Fonts array
  const fonts = [
    { name: 'Roboto', category: 'Sans-serif', fontFamily: "'Roboto', sans-serif" },
    { name: 'Playfair Display', category: 'Serif', fontFamily: "'Playfair Display', serif" },
    { name: 'Pacifico', category: 'Handwriting', fontFamily: "'Pacifico', cursive" },
    // Add more fonts here with appropriate fontFamily
  ];

  // State to track the text input
  const [previewText, setPreviewText] = useState('Type something to preview fonts!');

  // Handle input change
  const handleInputChange = (e) => {
    setPreviewText(e.target.value);
  };

  return (
    <div className="App">
      {/* Render the Homepage component */}
      <Homepage />

      {/* Font Preview Section */}
      <div className="min-h-screen bg-gray-50 p-6">
        <h1 className="text-4xl font-bold text-center mb-8">Font Preview App</h1>

        {/* Input box for live preview */}
        <div className="mb-6">
          <input
            type="text"
            placeholder="Type something..."
            value={previewText}
            onChange={handleInputChange}
            className="w-full p-3 border rounded shadow focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>

        {/* Font Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {fonts.map((font, index) => (
            <div
              key={index}
              className="p-4 border rounded shadow hover:shadow-lg transition"
              style={{ fontFamily: font.fontFamily }}
            >
              <h2 className="text-xl font-semibold">{font.name}</h2>
              <p className="text-gray-600 italic">{font.category}</p>
              <p className="mt-4 text-lg">{previewText}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default App;
