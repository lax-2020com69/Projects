import React from 'react'
import './Button.css';

type ButtonProps = {
    children: React.ReactNode;
    onClick: () => void;
    className?:string;
};

const Button: React.FC<ButtonProps> = ({children,
   onClick,className}) => {
  return (
  <button 
  className={`trainee-button ${className || ""}`}
   onClick={onClick}>
    {children}
  </button>);
};
export default Button;
