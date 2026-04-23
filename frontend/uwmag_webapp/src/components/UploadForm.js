import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Emoji from './Emoji';
import "./UploadForm.css";

// Moved translations outside to prevent re-creation on every render
const translations = {
  en: {
    chooseFile: 'Choose Image',
    uploadBtn: 'Analyze Waste',
    noFile: 'Please select an image first!',
    error: 'Upload failed. Please try again.',
    previewText: 'Image Preview:'
  },
  ta: {
    chooseFile: 'படத்தைத் தேர்ந்தெடுக்கவும்',
    uploadBtn: 'கழிவுகளை ஆய்வு செய்க',
    noFile: 'தயவுசெய்து முதலில் ஒரு படத்தை தேர்ந்தெடுக்கவும்!',
    error: 'பதிவேற்றம் தோல்வியடைந்தது. மீண்டும் முயற்சிக்கவும்.',
    previewText: 'பட முன்னோட்டம்:'
  },
  si: {
    chooseFile: 'රූපයක් තෝරන්න',
    uploadBtn: 'අපද්‍රව්‍ය විශ්ලේෂණය කරන්න',
    noFile: 'කරුණාකර පළමුව රූපයක් තෝරන්න!',
    error: 'උඩුගත කිරීම අසාර්ථක විය. කරුණාකර නැවත උත්සාහ කරන්න.',
    previewText: 'රූප පෙරදසුන:'
  }
};

const UploadForm = ({ onPredict, language, setLoading }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  // Shortcut for current language translations
  const t = translations[language] || translations.en;

  // Cleanup preview URL to prevent memory leaks
  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      // Create a temporary URL for the image preview
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedFile) {
      alert(t.noFile);
      return;
    }

    // 1. Trigger loading state in App.js
    setLoading(true);

    // 2. Create FormData
    const formData = new FormData();
    formData.append('file', selectedFile); 
    formData.append('language', language); // 👈 Crucial: Tells Backend which language to use for AI ideas

    try {
      // 3. Send to Flask Backend
      const response = await axios.post('http://localhost:5000/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // 4. Pass only the data part of the response back to App.js
      onPredict(response.data); 
    } catch (error) {
      console.error("Error uploading image:", error);
      alert(t.error);
      setLoading(false); // Stop loading if it fails
    }
  };

  return (
    <div className="upload-container">
      <form onSubmit={handleSubmit} className="upload-form">
        <div className="file-input-wrapper">
          <label className="custom-file-upload">
            <Emoji symbol="📷" label="camera" /> {t.chooseFile}
            <input 
              type="file" 
              accept="image/*" 
              onChange={handleFileChange} 
            />
          </label>
        </div>

        {/* Image Preview Area */}
        {previewUrl && (
          <div className="preview-section">
            <p className="preview-label">{t.previewText}</p>
            <div className="preview-image-container">
              <img src={previewUrl} alt="Preview" className="image-preview" />
            </div>
          </div>
        )}

        <button type="submit" className="btn-action upload-button">
          <Emoji symbol="🚀" label="rocket" /> {t.uploadBtn}
        </button>
      </form>
    </div>
  );
};

export default UploadForm;
