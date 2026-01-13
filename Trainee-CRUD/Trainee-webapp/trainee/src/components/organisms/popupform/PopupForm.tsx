import { faXmark } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import React, { useEffect, useState } from 'react'
import Label from '../../atoms/label/Label';
import Input from '../../atoms/input/Input';
import Button from '../../atoms/button/Button';
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
const PopupForm:React.FC<PopupFormProps> = ({onClose, trainee}) => {
    const [name, setName] = useState<string>("");
    const [email, setEmail] = useState<string>("");
    const [department, setDepartment] = useState<string>("");
    const [stipend, setStipend] = useState<string>("");

    useEffect(() => {
        if (trainee) {
            setName(trainee.name);
            setEmail(trainee.email);
            setDepartment(trainee.department);
            setStipend(trainee.stipend.toString());
        }
    },[trainee]);
    const fetchData = async () => {
        try {
            const payload = {
            id: trainee ? trainee.id : undefined,
            name,
            email,
            department,
            stipend: Number(stipend),
        };
        const response = await fetch(
           
             "http://localhost:8080/Trainee/trainees",
            {
                method: trainee ? "PUT" : "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload),
            }
        );
        const data = await response.json();
       console.log({ data });
       
        
        } catch (error) {
            console.log(error)
        }
        
        
    };
    const onSubmit = () => {
        fetchData();
        onClose();
    };

  return (
    <div className="form-container">
        {/* <FontAwesomeIcon
        icon={faXmark}
        className="close-btn"
        onClick={onClose}
        /> */}
        <div className="add-form">
            <FontAwesomeIcon
            icon={faXmark}
            className="close-btn"
            onClick={onClose}
            />
            <h2>Add Form</h2>
            <Label htmlFor='name'>Name</Label>
            <Input
            id="name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
             />
             <br />
             <Label htmlFor="email">Email</Label>
             <Input 
             id="email"
             type="email"
             value={email}
             onChange={(e) => setEmail(e.target.value)}
             />
             <br />
             <Label htmlFor='department'>Department</Label>
            <Input
            id="department"
            type="text"
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
             />
             <br />
             <Label htmlFor="stipend">Stipend</Label>
             <Input 
             id="stipend"
             type="text"
             value={stipend}
             onChange={(e) => setStipend(e.target.value)}
             />
             <br />
             <Button onClick={onSubmit}>Submit</Button>
        </div>
    </div>
  )
}

export default PopupForm;