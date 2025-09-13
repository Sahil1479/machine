import React, { useState, useEffect } from 'react';
const Search = () => {
    const [query, setQuery] = useState('');
    const [debouncedQuery, setDebouncedQuery] = useState('');

    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedQuery(query);
        }, 1000);

        return () => clearTimeout(timer);
    }, [query]);


    useEffect(() => {
        if(debouncedQuery) {
            console.log(`Searching for: ${debouncedQuery}`);
            // Here you would typically make an API call to fetch search results
        }
    }, [debouncedQuery]);

    return (
        <div>
        <input type="text" onChange={(e) => setQuery(e.target.value)} value={query} placeholder="Search..." />
        <p>Debounced Query: {debouncedQuery}</p>
        </div>
    );
};

export default Search;