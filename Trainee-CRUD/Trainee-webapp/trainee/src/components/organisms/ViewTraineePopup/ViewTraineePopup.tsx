import React from "react";
import "./ViewTraineePopup.css";

interface ViewTraineePopupProps {
  trainee: {
    id: number;
    name: string;
    email: string;
    department: string;
    stipend: number;
  };
  onClose: () => void;
}

const ViewTraineePopup: React.FC<ViewTraineePopupProps> = ({ trainee, onClose }) => {
  return (
    <div className="view-overlay">
      <div className="view-popup">
        <h3>Trainee Details</h3>
        <div className="view-details">
          <p><strong>ID:</strong> {trainee.id}</p>
          <p><strong>Name:</strong> {trainee.name}</p>
          <p><strong>Email:</strong> {trainee.email}</p>
          <p><strong>Department:</strong> {trainee.department}</p>
          <p><strong>Stipend:</strong> {trainee.stipend}</p>
        </div>
        <button className="close-btn" onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

export default ViewTraineePopup;
