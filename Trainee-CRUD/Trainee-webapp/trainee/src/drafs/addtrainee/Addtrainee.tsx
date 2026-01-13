import Label from "../../components/atoms/label/Label";
import Input from "../../components/atoms/input/Input";
import Button from "../../components/atoms/button/Button";
import { useState } from "react";
import  "./Addtrainee.css";
type AddtraineeProps = {
    onSuccess :() => void;
    onCancel: () => void;
};
const Addtrainee:React.FC<AddtraineeProps> = ({onSuccess,onCancel}) => {
    const [id,setId] = useState<string>("");
    const [name,setName] = useState<string>("");
    const [email,setEmail] = useState<string>("");
    const [department,setDepartment] = useState<string>("");
    const [stipend,setStipend] = useState<string>("");

    const handleid = (e:React.ChangeEvent<HTMLInputElement>) => {
        setId(e.target.value);
    };
    const handlename = (e:React.ChangeEvent<HTMLInputElement>) => {
        setName(e.target.value);
    };
    const handleemail = (e:React.ChangeEvent<HTMLInputElement>) => {
        setEmail(e.target.value);
    };
    const handledepartment = (e:React.ChangeEvent<HTMLInputElement>) => {
        setDepartment(e.target.value);
    };
    const handlestipend = (e:React.ChangeEvent<HTMLInputElement>) => {
        setStipend(e.target.value);
    };
    const resetForm = () => {
        setId("");
        setName("");
        setEmail("");
        setDepartment("");
        setStipend("");
    };
    const handleSubmit = () => {
        onSuccess();
        resetForm();
    };
    const handleCancel = () => {
        onCancel();
        resetForm();
    };
  return (
    <div className="form-container">
        <div className='trainee-id'>
            <Label>Id:</Label>
            <Input id={'id'} name={'id'} type={'text'} value={id} onChange={handleid} />
        </div>
        <div className='trainee-name'>
            <Label>Name:</Label>
            <Input id={'name'} name={'name'} type={'text'} value={name} onChange={handlename} />
        </div>
        <div className='trainee-email'>
            <Label>Email:</Label>
            <Input id={'email'} name={'email'} type={'email'} value={email} onChange={handleemail} />
        </div>
        <div className='trainee-department'>
            <Label>Department:</Label>
            <Input id={'department'} name={'department'} type={'text'} value={department} onChange={handledepartment} />
        </div>
        <div className='trainee-stipend'>
            <Label>Stipend:</Label>
            <Input id={'stipend'} name={'stipend'} type={'text'} value={stipend} onChange={handlestipend} />
        </div>
        <div className="form-btn">
            <div><Button onClick={handleSubmit}>Submit</Button></div>
            <div><Button onClick={handleCancel}>Cancel</Button></div>
        </div>
    </div>
  )
}

export default Addtrainee;