import React, { useState } from 'react';

function InputField() {
  const [searchTerm, setSearchTerm] = useState("");

  const handleChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    // Handle search logic here
    console.log("Searching for:", searchTerm);
  };

  return (
    <form onSubmit={handleSearch} className="flex items-center max-w-lg mx-auto mt-12 w-full">
      <label htmlFor="search" className="sr-only">Search</label>
      <div className="relative w-full">
        <input
          type="text"
          id="search"
          value={searchTerm}
          onChange={handleChange}
          className="bg-gray-100 border border-gray-300 text-lg text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-3 pl-10 shadow-lg transition duration-300 ease-in-out transform hover:scale-105"
          placeholder="Search for fonts..."
          required
        />
        <button
          type="submit"
          className="absolute inset-y-0 right-0 flex items-center pr-4 bg-blue-600 text-white text-lg font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 transition duration-300 ease-in-out transform hover:scale-110"
        >
          Search
        </button>
      </div>
    </form>
  );
}

export default InputField;
