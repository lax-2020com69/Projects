import React, { useEffect } from "react";
import "./Popup.css";
import Input from "../../components/atoms/input/Input";
import Label from "../../components/atoms/label/Label";
import Button from "../../components/atoms/button/Button";
import Trainee from "../trainee/Trainee";
interface Trainee {
    id?: number;
    name:string;
    email:string;
    department:string;
    stipend: number | string;
}
type PopupProps = {
    onClose: () => void;
    trainee?: Trainee | null;
};
const Popup:React.FC<PopupProps> = ({onClose, trainee}) => {
const [name,setName] = React.useState<string>("");
const [email,setEmail] = React.useState<string>("");
const [department,setDepartment] = React.useState<string>("");
const [stipend,setStipend] = React.useState<string>("");

// const handlename = (e:React.ChangeEvent<HTMLInputElement>) => {
//     setName(e.target.value);
// };
useEffect(()=> {
    if (trainee) {
        setName(trainee.name);
        setEmail(trainee.email);
        setDepartment(trainee.department);
        setStipend(trainee.stipend.toString());
    } else {
        setName("");
        setEmail("");
        setDepartment("");
        setStipend("");
    }
}, [Trainee])

const handleemail = (e:React.ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
};
const handledepartment = (e:React.ChangeEvent<HTMLInputElement>) => {
    setDepartment(e.target.value);
};
const handlestipend = (e:React.ChangeEvent<HTMLInputElement>) => {
    setStipend(e.target.value);
};

const fetchdata = async () => {
    // const payload = {
    //     name,
    //     email,
    //     department,
    //     stipend
    // };
    const payload = {
        email:email,
        name:name,
        department:department,
        stipend:Number(stipend)
    };
    console.log({payload})
    const response = await fetch(
        trainee
        ? `http://localhost:8080/Trainee/trainees?id=${trainee.id}`
        : "http://localhost:8080/Trainee/trainees", {
        method: trainee ? "PUT" : "POST",
        headers: {"Content-Type": "application/json"},
        body:JSON.stringify(payload)
    });
    
    const data = await response.json();
    console.log("data: ",data);
};
const onSumit = () => {
    fetchdata();
    onClose();
};
  return (
    <div className="popup-input">
        <div className="popup-content">
            <div className="popup-close-button" onClick={onClose}>
            <span>X</span>
            </div>
            <div className="input-group">
                <Label className="input-label">Name:</Label>
                <Input id={'name'} name={'name'} type={'text'} value={name} onChange={e => setName(e.target.value)} className="input-group" />
            </div>
            <div>
                <Label className="input-label">Email:</Label>
                <Input id={'email'} name={'email'} type={'email'} value={email} onChange={handleemail} className="input-group" />
            </div>
            <div>
                <Label className="input-label">Department:</Label>
                <Input id={'department'} name={'department'} type={'text'} value={department} onChange={handledepartment} className="input-group" />
            </div>
            <div>
                <Label className="input-label">Stipend:</Label>
                <Input id={'stipend'} name={'stipend'} type={"number"} value={stipend} onChange={handlestipend} className="input-group" />
            </div>
            <div><Button onClick={onSumit}>Submit</Button></div>
        </div>
    </div>
  )
}

export default Popup;