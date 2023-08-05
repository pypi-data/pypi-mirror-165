// built with insights from https://www.digitalocean.com/community/tutorials/gatsbyjs-state-management-in-gatsby
import React, { useState } from 'react';
import { eraseCookie } from '../components/utils';

export interface AppContextType {
  user: any; 
  setUser: any;
  logout: any; 
  cookie_name: string;
}

const cookie_name = "app_cookie_";
 
export const appContext = React.createContext<AppContextType>({} as AppContextType);
const Provider = ({ children }:any) => {
  const [user, setUser] = useState(null); 
  const logout = () => {
    setUser(null);
    eraseCookie(cookie_name);
  };
  
  return (
    <appContext.Provider value={{ user, setUser, logout, cookie_name }}>
      {children}
    </appContext.Provider>
  );
};


export default ({ element }:any) => (
  <Provider>
    {element}
  </Provider>
);