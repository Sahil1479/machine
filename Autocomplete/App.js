import React, { useState, useEffect, useRef, useCallback } from "react";

// Utility: Simulated async fetch (like calling an API)
const mockSuggestions = [
  "apple", "apricot", "banana", "blackberry", "blueberry", "cherry", 
  "grape", "grapefruit", "kiwi", "lemon", "lime", "mango", "melon", 
  "orange", "peach", "pear", "pineapple", "plum", "raspberry", "strawberry", "watermelon"
];

const fetchSuggestions = (query) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const filtered = mockSuggestions.filter(item =>
        item.toLowerCase().includes(query.toLowerCase())
      );
      resolve(filtered);
    }, 300); // simulate network delay
  });
};

// Utility: Debounce hook
const useDebounce = (value, delay) => {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const handler = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);
  return debounced;
};

export default function Autocomplete() {
  const [input, setInput] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [highlightIndex, setHighlightIndex] = useState(-1);
  const [showDropdown, setShowDropdown] = useState(false);
  const listRef = useRef(null);

  const debouncedInput = useDebounce(input, 300);

  const handleChange = (e) => {
    setInput(e.target.value);
    setShowDropdown(true);
  };

  // Fetch suggestions on debounced input
  useEffect(() => {
    if (!debouncedInput.trim()) {
      setSuggestions([]);
      return;
    }

    let isActive = true;
    fetchSuggestions(debouncedInput).then((results) => {
      if (isActive) {
        setSuggestions(results);
        setHighlightIndex(-1);
      }
    });

    return () => {
      isActive = false; // cancel if component unmounts or input changes quickly
    };
  }, [debouncedInput]);

  // Keyboard Navigation
  const handleKeyDown = (e) => {
    if (!suggestions.length) return;

    switch (e.key) {
      case "ArrowDown":
        setHighlightIndex((prev) => (prev + 1) % suggestions.length);
        break;
      case "ArrowUp":
        setHighlightIndex((prev) =>
          prev <= 0 ? suggestions.length - 1 : prev - 1
        );
        break;
      case "Enter":
        if (highlightIndex >= 0) {
          selectSuggestion(suggestions[highlightIndex]);
        }
        break;
      case "Escape":
        setShowDropdown(false);
        break;
      default:
        break;
    }
  };

  const selectSuggestion = (value) => {
    setInput(value);
    setShowDropdown(false);
    setSuggestions([]);
  };

  const renderHighlightedText = (text) => {
    const index = text.toLowerCase().indexOf(input.toLowerCase());
    if (index === -1) return text;
    return (
      <>
        {text.slice(0, index)}
        <strong className="text-blue-600">{text.slice(index, index + input.length)}</strong>
        {text.slice(index + input.length)}
      </>
    );
  };

  return (
    <div className="relative w-96 mx-auto mt-10">
      <input
        type="text"
        className="w-full border border-gray-300 rounded px-4 py-2"
        placeholder="Search fruits..."
        value={input}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        onFocus={() => setShowDropdown(true)}
      />
      {showDropdown && suggestions.length > 0 && (
        <ul
          ref={listRef}
          className="absolute z-10 w-full border border-gray-300 bg-white rounded shadow mt-1 max-h-60 overflow-y-auto"
        >
          {suggestions.map((item, index) => (
            <li
              key={item}
              className={`px-4 py-2 cursor-pointer ${
                highlightIndex === index ? "bg-blue-100" : ""
              }`}
              onMouseEnter={() => setHighlightIndex(index)}
              onMouseDown={() => selectSuggestion(item)} // onMouseDown to avoid losing focus
            >
              {renderHighlightedText(item)}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
