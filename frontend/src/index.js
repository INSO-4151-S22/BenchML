import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import { Auth0Provider } from "@auth0/auth0-react";
import { getConfig } from "./utils/config";

const config = getConfig();

const providerConfig = {
  domain: config.domain,
  clientId: config.clientId,
  audience: config.audience,
  redirectUri: window.location.origin,
  useRefreshTokens:true,
  cacheLocation:"localstorage"
};

ReactDOM.render(
  <Auth0Provider {...providerConfig}>
    <App />
  </Auth0Provider>,
  document.getElementById('root')
);

