// import React from 'react';
import {useEffect, useState} from "react";
import Button from '../../components/atoms/button/Button';
import Addtrainee from "../addtrainee/Addtrainee";
import Viewtrainee from "../viewtrainee/Viewtrainee";
import Viewidtrainee from "../viewidtrainee/Viewidtrainee";
import Updatetrainee from "../udatetrainee/Updatetrainee";
import Deltrainee from "../deltrainee/Deltrainee";
import "./Trainee.css";
const Trainee = () => {
    const [msg,setMsg] = useState<string>("Message  Here!...");
    // const [showAddTrainee,setShowAddTrainee] = useState<boolean>(false);
    // const [showViewTrainee,setShowViewTrainee] = useState<boolean>(false);
    // const [showViewIdTrainee,setShowViewIdTrainee] = useState<boolean>(false);
    // const [showUpdateTrainee,setShowUpdateTrainee] = useState<boolean>(false);
    // const [showDelTrainee,setShowDelTrainee] = useState<boolean>(false);
    const [showPopupMsg,setShowPopupMsg] =useState<boolean>(false);
    const [activeForm, setActiveForm] = useState<string| null>(null);
    // const [showTraineeContainer,setShowTraineeContainer] = useState<boolean>(false);
    useEffect(() => {
        // setShowAddTrainee(false);
        // setShowViewTrainee(false);
        // setShowViewIdTrainee(false);
        // setShowUpdateTrainee(false);
        // setShowDelTrainee(false);
        setActiveForm(null);
        setShowPopupMsg(false);
    }, []);
    const setMsgAndShow = (message : string) => {
        setMsg(message);
        setShowPopupMsg(true);
    }; 
    // const handleaddtrainee = () => {
    //     setMsg("Added Trainee.");
    //     setShowPopupMsg(true);
    // };
    // const handlecanceltrainee = () => {
    //    setMsg("Cancled Trainee.");
    //    setShowPopupMsg(true); 
    // };
    const handleCloseMsg = () => {
        setMsg("");
        setShowPopupMsg(false);
    };
    const handleCloseTrainee = () => {
        setActiveForm(null);
    };
  return (
    <div className='trainee-container'>
        {showPopupMsg && (
            <div className='trainee-msg'>
                <p>{msg}</p>
                <div><Button onClick={handleCloseMsg}>X</Button></div>
            </div>
        )}
        {/* <div className='trainee-navbar'>
            <div><Button onClick={() => setShowAddTrainee(true)}>Add Trainee</Button></div>
            <div><Button onClick={() => setShowViewTrainee(true)}>View All Trainee</Button></div>
            <div><Button onClick={() => setShowViewIdTrainee(true)}>View Trainee by ID</Button></div>
            <div><Button onClick={() => setShowUpdateTrainee(true)}>Update Trainee</Button></div>
            <div><Button onClick={() => setShowDelTrainee(true)}>Delete Trainee</Button></div>
        </div> */}
        {/* { showAddTrainee && (<div><Addtrainee onClickhandleaddtrainee={handleaddtrainee} onClickhandlecanceltrainee={handlecanceltrainee}/></div>)} */}
        {/* {showTraineeContainer && (
            <div>
                <Button onClick={handleCloseTrainee}>X</Button>
                { showAddTrainee && (<div><Addtrainee onSuccess={() => setMsgAndShow("Added Trainee.")} onCancel={()=> setMsgAndShow("Cancelled Trainee.")}/></div>)}
                { showViewTrainee && ( <Viewtrainee/> )}
                { showViewIdTrainee && ( <Viewidtrainee/> )}
                { showUpdateTrainee && ( <Updatetrainee/> )}
                { showDelTrainee && ( <Deltrainee/> )}
            </div>
        )} */}
        <div className='trainee-navbar'>
                <div><Button onClick={() => setActiveForm("add")}>Add Trainee</Button></div>
                <div><Button onClick={() => setActiveForm("view")}>View All Trainee</Button></div>
                <div><Button onClick={() => setActiveForm("viewid")}>View Trainee by ID</Button></div>
                <div><Button onClick={() => setActiveForm("update")}>Update Trainee</Button></div>
                <div><Button onClick={() => setActiveForm("delete")}>Delete Trainee</Button></div>
            </div>

        <div>
            {activeForm && (
                <div className="trainee-form-container">
                    <Button onClick={handleCloseTrainee}>Close</Button>

                    {activeForm === "add" && (
                        <Addtrainee
                            onSuccess={() => setMsgAndShow("Added Trainee.")}
                            onCancel={() => setMsgAndShow("Cancelled Trainee.")}
                        />
                    )}
                    {activeForm === "view" && <Viewtrainee />}
                    {activeForm === "viewid" && <Viewidtrainee />}
                    {activeForm === "update" && <Updatetrainee />}
                    {activeForm === "delete" && <Deltrainee />}
                </div>
            )}
        </div>
    </div>
  )
}

export default Trainee;