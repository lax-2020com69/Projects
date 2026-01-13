import { faXmark } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useEffect, useState } from "react";
import Label from "../../atoms/label/Label";
import Input from "../../atoms/input/Input";
import Button from "../../atoms/button/Button";
import "./PopupForm.css";

type Trainee = {
  id: number;
  name: string;
  email: string;
  department: string;
  stipend: number;
};

type PopupFormProps = {
  onClose: () => void;
  trainee?: Trainee | null;
};

const PopupForm: React.FC<PopupFormProps> = ({ onClose, trainee }) => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [department, setDepartment] = useState("");
  const [stipend, setStipend] = useState("");

  useEffect(() => {
    if (trainee) {
      setName(trainee.name);
      setEmail(trainee.email);
      setDepartment(trainee.department);
      setStipend(trainee.stipend.toString());
    } else {
      // Reset when adding a new trainee
      setName("");
      setEmail("");
      setDepartment("");
      setStipend("");
    }
  }, [trainee]);

  const handleSubmit = async () => {
    // Basic validation
    if (!name || !email || !department || !stipend) {
      alert("Please fill in all fields.");
      return;
    }

    const payload = {
      id: trainee ? trainee.id : undefined,
      name,
      email,
      department,
      stipend: Number(stipend),
    };

    try {
      const response = await fetch(
        trainee
          ? `http://localhost:8080/Trainee/trainees/${trainee.id}`
          : "http://localhost:8080/Trainee/trainees",
        {
          method: trainee ? "PUT" : "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to save trainee");
      }

      await response.json();
      alert(trainee ? "Trainee updated successfully!" : "Trainee added successfully!");
      onClose();
    } catch (error) {
      console.error("Error saving trainee:", error);
      alert("Something went wrong while saving. Please try again.");
    }
  };

  return (
    <div className="form-container">
      <div className="add-form">
        <FontAwesomeIcon icon={faXmark} className="close-btn" onClick={onClose} />

        <h2>{trainee ? "Edit Trainee" : "Add Trainee"}</h2>

        <Label htmlFor="name">Name</Label>
        <Input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <br />

        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <br />

        <Label htmlFor="department">Department</Label>
        <Input
          id="department"
          type="text"
          value={department}
          onChange={(e) => setDepartment(e.target.value)}
          required
        />
        <br />

        <Label htmlFor="stipend">Stipend</Label>
        <Input
          id="stipend"
          type="number"
          value={stipend}
          onChange={(e) => setStipend(e.target.value)}
          required
        />
        <br />

        <Button onClick={handleSubmit}>{trainee ? "Update" : "Submit"}</Button>
      </div>
    </div>
  );
};

export default PopupForm;
