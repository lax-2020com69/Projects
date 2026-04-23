// components/Emoji.js
import React from 'react';
import PropTypes from 'prop-types';

const Emoji = ({ symbol, label, size, className }) => {
  if (!symbol || !label) {
    console.error('Emoji requires both a symbol and a label for accessibility.');
  }

  return (
    <span
      role="img"
      aria-label={label}
      className={`inline-block ${className}`}
      style={{ fontSize: size }}
    >
      {symbol}
    </span>
  );
};

Emoji.propTypes = {
  symbol: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  size: PropTypes.string, // Allow the size to be passed as a string (e.g., '24px', '1.5em')
  className: PropTypes.string, // Allow custom class names for styling
};

Emoji.defaultProps = {
  size: '1em', // Default size
  className: '', // Default empty class
};

export default Emoji;
