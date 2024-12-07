import React from 'react';
import InputField from './InputField';

function Homepage() {
  return (
    <div className="homepage">
      <div className="text-center mt-20 px-4">
        <h1 className="text-5xl font-extrabold text-gray-900 leading-tight">
          Shaping a world with reimagination.
        </h1>
        <p className="text-sm text-gray-600 mt-4 mb-8">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Odio incidunt nam itaque sed eius modi error totam sit illum. Voluptas doloribus asperiores quaerat aperiam. Quidem harum omnis beatae ipsum soluta!
        </p>
        <InputField />
      </div>
    </div>
  );
}

export default Homepage;
