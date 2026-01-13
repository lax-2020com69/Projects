import React, { useState } from "react";
import Button from "../../atoms/button/Button";
import "./SearchById.css";

interface SearchByIdProps {
  onSearch: (id: string) => void;
  onReset: () => void;
}

const SearchById: React.FC<SearchByIdProps> = ({ onSearch, onReset }) => {
  const [searchId, setSearchId] = useState("");

  const handleSearchClick = () => {
    if (!searchId.trim()) {
      onReset(); // show all data again if input is empty
      return;
    }
    onSearch(searchId.trim());
  };

  return (
    <div className="search-container">
      <input
        type="number"
        placeholder="Enter trainee ID..."
        value={searchId}
        onChange={(e) => setSearchId(e.target.value)}
        className="search-input"
      />
      <Button onClick={handleSearchClick}>🔍 Search by ID</Button>
    </div>
  );
};

export default SearchById;
