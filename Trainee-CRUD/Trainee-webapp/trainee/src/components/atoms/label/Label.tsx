import React from 'react'
import "./Label.css";
type LabelProps = {
  htmlFor?:string;
    children:React.ReactNode;
    className?:string;
};
const Label:React.FC<LabelProps> = ({htmlFor, children, className}) => {
  return (
    <div className={`trainee-label ${className || ""}`}>
        <label htmlFor={htmlFor}>{children}</label>
    </div>
  )
}

export default Label;