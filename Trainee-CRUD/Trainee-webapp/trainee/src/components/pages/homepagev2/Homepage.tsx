import { useEffect, useState } from "react";
import Button from "../../atoms/button/Button";
import PopupForm from "../../organisms/popupformv2/PopupForm";
import SearchById from "../../molecules/searchbyid/SearchById";
import ViewTraineePopup from "../../organisms/ViewTraineePopup/ViewTraineePopup";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEdit, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
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
  const [viewTrainee, setViewTrainee] = useState<HomepageProps | null>(null);

  const getFetchData = async () => {
    const response = await fetch("http://localhost:8080/Trainee/trainees", {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });
    const responseData = await response.json();
    setData(responseData);
  };

  useEffect(() => {
    getFetchData();
  }, [isOpen]);

  const handlePopupOpen = () => {
    setSelectedTrainee(null);
    setIsOpen(true);
  };

  const handlePopupClose = () => {
    setIsOpen(false);
    getFetchData();
  };

  const handleEdit = (trainee: HomepageProps) => {
    setSelectedTrainee(trainee);
    setIsOpen(true);
  };

  const deleteTrainee = async (id: number) => {
    try {
      await fetch(`http://localhost:8080/Trainee/trainees/${id}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
      });
    } catch (error) {
      console.error(error);
    }
  };

  const handleDelete = (id: number) => {
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

  // 🔍 View trainee by ID (popup)
  const handleSearch = async (id: string) => {
    try {
      const response = await fetch(`http://localhost:8080/Trainee/trainees/${id}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });

      if (!response.ok) {
        alert("Trainee not found");
        return;
      }

      const trainee = await response.json();
      setViewTrainee(trainee);
    } catch (error) {
      console.error("Error searching trainee:", error);
    }
  };

  const handleReset = () => {
    setViewTrainee(null);
    getFetchData();
  };

  return (
    <div className="main-container">
      <h2>Trainee Management</h2>

      <div className="top-bar">
        <div className="add-btn">
          <Button onClick={handlePopupOpen}>+ Add</Button>
        </div>
        <SearchById onSearch={handleSearch} onReset={handleReset} />
      </div>

      {isOpen && <PopupForm onClose={handlePopupClose} trainee={selectedTrainee} />}
      {viewTrainee && <ViewTraineePopup trainee={viewTrainee} onClose={handleReset} />}

      <div className="table-container">
        <table>
          <thead>
            <tr style={{ backgroundColor: "#00c3ff" }}>
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
              <tr
                key={item.id}
                style={{ backgroundColor: index % 2 === 0 ? "#f0f0f0" : "#ffffff" }}
              >
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

      {deleteConfirmId !== null && (
        <div className="overlay">
          <div className="confirm-box">
            <p>Are you sure you want to delete this trainee?</p>
            <div className="confirm-actions">
              <button className="yes-btn" onClick={confirmDelete}>Yes</button>
              <button className="no-btn" onClick={cancelDelete}>No</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Homepage;
