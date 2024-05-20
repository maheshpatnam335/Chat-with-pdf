import React, { useState } from 'react';

const SearchPDF = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

    const handleSearch = async () => {
        const response = await fetch(`http://localhost:5000/search?query=${query}`);
        const data = await response.json();
        setResults(data);
    };

    return (
        <div>
            <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} />
            <button onClick={handleSearch}>Search</button>
            <ul>
                {results.map(result => (
                    <li key={result.id}>{result.distance}</li>
                ))}
            </ul>
        </div>
    );
};

export default SearchPDF;
