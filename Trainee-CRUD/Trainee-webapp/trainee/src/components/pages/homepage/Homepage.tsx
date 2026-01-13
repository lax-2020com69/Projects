import { useEffect, useState } from 'react'
import Button from '../../atoms/button/Button';
import PopupForm from '../../organisms/popupform/PopupForm';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit, faTrashAlt } from '@fortawesome/free-solid-svg-icons';
import "./Homepage.css";
interface HomepageProps {
    id: number;
    name: string;
    email: string;
    department: string;
    stipend: number;
}

const Homepage = () => {
    const [data, setData] = useState<HomepageProps[]>([]);
    const [isOpen, setIsOpen] = useState(false);
    const [selectedTrainee, setSelectedTrainee] = useState<HomepageProps | null>(null);
    
    const [deleteConfirmId, setDeleteConfirmId] = useState<number | null>(null);

    const handlePopupOpen = () => {
        setSelectedTrainee(null);
        setIsOpen(true);
    };
    const handlePopupClose = () => {
        setIsOpen(false);
        getFetchData();
        
    };
    const getFetchData = async () => {
        const response = await fetch ("http://localhost:8080/Trainee/trainees", {
            method: "GET",
            headers: { "Content-Type": "application/json" },
        });
        const responseData = await response.json();
        setData(responseData);
    };
    console.log(data);

    useEffect(() => {
        getFetchData();
    },[isOpen]);
    
    const handleEdit = (trainee: HomepageProps) => {
        setSelectedTrainee(trainee);
        setIsOpen(true);
    };
    const deleteTrainee = async (id: number) => {
        console.log(id);
        
            if (id) {
        try {
            const response = await fetch(
                `http://localhost:8080/Trainee/trainees/${id}`, {
                    method: "DELETE",
                    headers: {"Content-Type": "application/json"},
                }
            );
           
            const data = await response.json();
            console.log("Deleted:", data);
            
        } catch (error) {
            console.log(error);
            
        }
    }
    };
    const handleDelete = async (id: number) => {
        // const confirmed = window.confirm("Are you sure you want to delete this traine?");
        // if (!confirmed) return;

        // await deleteTrainee(id);
        // getFetchData();
        setDeleteConfirmId(id);

    };
    const confirmDelete = async () => {
        if (deleteConfirmId !== null) {
            await deleteTrainee(deleteConfirmId);
            getFetchData();
            setDeleteConfirmId(null);
        }
    };

    const cancelDelete = () => {
        setDeleteConfirmId(null);
    };
    
  return (
    <div className="main-coontainer">
        <h2>Trainee Management</h2>
        <div className="add-btn">
            <Button onClick={handlePopupOpen}>+ Add</Button>
        </div>
        {isOpen && (
            <PopupForm onClose={handlePopupClose} trainee={selectedTrainee}  />
        )}

        <div className="table-container">
            <table>
                <thead>
                    <tr style={{ backgroundColor: '#00c3ffff'}} >
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Department</th>
                        <th>Stipend</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((item, index) => (
                        <tr key={item.id}
                        style={{ backgroundColor: index % 2 === 0 ? '#f0f0f0' : '#ffffff' }} >
                            <td>{item.id}</td>
                            <td>{item.name}</td>
                            <td>{item.email}</td>
                            <td>{item.department}</td>
                            <td>{item.stipend}</td>
                            <td>
                                <div className="action-icons">
                                    <FontAwesomeIcon
                                    icon={faEdit}
                                    className="edit-icon"
                                    onClick={() => handleEdit(item)}
                                    />
                                    <FontAwesomeIcon
                                    icon={faTrashAlt}
                                    className="delete-icon"
                                    onClick={() => handleDelete(item.id)}
                                    />
                                </div>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
        {/* Custom confirmation box overlay */}
            {deleteConfirmId !== null && (
                <div
                    style={{
                        position: "fixed",
                        top: 0,
                        left: 0,
                        width: "100vw",
                        height: "100vh",
                        backgroundColor: "rgba(0,0,0,0.5)",
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                        zIndex: 1000,
                    }}
                >
                    <div
                        style={{
                            backgroundColor: "#fff",
                            padding: "20px",
                            borderRadius: "8px",
                            boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
                            width: "320px",
                            textAlign: "center",
                        }}
                    >
                        <p>Are you sure you want to delete this trainee?</p>
                        <div style={{ marginTop: "20px" }}>
                            <button
                                onClick={confirmDelete}
                                style={{
                                    backgroundColor: "red",
                                    color: "white",
                                    padding: "8px 16px",
                                    border: "none",
                                    borderRadius: "4px",
                                    marginRight: "10px",
                                    cursor: "pointer",
                                }}
                            >
                                Yes
                            </button>
                            <button
                                onClick={cancelDelete}
                                style={{
                                    padding: "8px 16px",
                                    borderRadius: "4px",
                                    cursor: "pointer",
                                }}
                            >
                                No
                            </button>
                        </div>
                    </div>
                </div>
            )}
    </div>
  )
}

export default Homepage;