import React, { useState } from 'react';
import FontResultCard from './Card';

const LivePreview = ({ fonts }) => {
  const [text, setText] = useState('');

  return (
    <div className="px-4 py-6">
      <h2 className="text-2xl font-semibold mb-4">Live Preview</h2>
      <input
        type="text"
        placeholder="Type here to preview..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="w-full max-w-lg px-4 py-2 mb-6 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {fonts.map((font) => (
          <FontResultCard
            key={font.name}
            fontName={font.name}
            fontCategory={font.category}
            sampleText={text}
          />
        ))}
      </div>
    </div>
  );
};

export default LivePreview;
