import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit, faTrashCan } from '@fortawesome/free-solid-svg-icons';
import React, { useEffect, useState } from 'react'
import Popup from '../popup/Popup';
interface TraineeDetailsProps {
    id:number;
    name:string;
    email:string;
    department:string;
    stipend:number;
};
const TraineeDetails= () => {
    const [open,isopen] = useState<boolean>(false);
    const [data,setData] = useState<TraineeDetailsProps[]>([]);
    const [selectedTrainee, setSelectedTrainee] = useState<TraineeDetailsProps | null>(null);

    const handlePopupOpen = () => {
        setSelectedTrainee(null);
        isopen(true);
    };
    const handlePopupClose = () => {
        isopen(false);
    };
    const getfatchData = async () => {
        const response = await fetch("http://localhost:8080/Trainee/trainees", {
            method: "GET",
            headers: {"Content-Type": "application/json"},
    });
    
    const responseData = await response.json();
    setData(responseData);
};
    console.log( data );

    const handleEdit = (trainee: TraineeDetailsProps) => {
        setSelectedTrainee(trainee);
        isopen(true);
    };
    useEffect(() => {
        getfatchData();
    },[open]);
    
  return (
    <div>
        <table>
            <thead>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Department</th>
                <th>Stipend</th>
                <th>Action</th>
            </thead>
            <tbody>
                {data.map((item) => (
                    <tr key={item.id}>
                        <td>{item.id}</td>
                        <td>{item.name}</td>
                        <td>{item.email}</td>
                        <td>{item.department}</td>
                        <td>{item.stipend}</td>
                    <td>
                        <FontAwesomeIcon style={{ color: "blue"}} icon={faEdit} onClick={handleEdit(item)} />
                        <FontAwesomeIcon style={{ color: "red"}} icon={faTrashCan} onClick={handleDelete(item)} />
                    </td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
  )
}

export default TraineeDetails;