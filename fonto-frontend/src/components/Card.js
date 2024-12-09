import React from 'react';

const FontResultCard = ({ fontName, fontCategory, sampleText }) => {
  return (
    <div
      className="border rounded-lg p-4 m-4 text-center transition-transform transform hover:scale-105 hover:shadow-lg"
      style={{ fontFamily: fontName }}
    >
      <h3 className="text-lg font-bold">{fontName}</h3>
      <p className="text-base my-2">{sampleText || "Sample Text"}</p>
      <span className="text-sm text-gray-500">{fontCategory}</span>
    </div>
  );
};

export default FontResultCard;
