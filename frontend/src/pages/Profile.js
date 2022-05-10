import React from "react";
import { useAuth0 } from "@auth0/auth0-react";

const Profile = () => {
  const { user, logout} = useAuth0();

  return (
      <div>
        <h2>Personal Information</h2>
        <h2>{user.given_name} {user.family_name}</h2>
        <h2>{user.email}</h2>
        <div>
          <button onClick={() => logout({ returnTo: window.location.origin })}>Log Out</button>
        </div>
      </div>

  );
}

export default Profile;