import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import "../css/Profile.min.css";


const Profile = () => {
  const { user, logout} = useAuth0();

  return (
      <div className="container">
        <h2 className="title">Personal Information</h2>
        <h2 className="name">{user.given_name} {user.family_name}</h2>
        <h2 className="name">{user.email}</h2>
        <div>
          <button className="logout_button" onClick={() => logout({ returnTo: window.location.origin })}><div>Log out</div></button>
        </div>
      </div>

  );
}

export default Profile;