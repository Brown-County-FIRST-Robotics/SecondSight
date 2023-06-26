import React from "react";

import {
    Nav,
    NavLogo,
    NavLink,
    Bars,
    NavMenu,
    NavBtn,
    NavBtnLink,
} from "./NavbarElements";


const Navbar = () => {
    return (
        <>
           <Nav>
            <NavLogo to="/">
                Logo
            </NavLogo>
            <Bars />

            <NavMenu>
                <NavLink 
                  to="/"
                  activeStyle={{ color:'black' }}
                >
                    Home
                </NavLink>
                <NavLink 
                  to="/info"
                  activeStyle={{ color: 'black' }}
                >
                    Info
                </NavLink>
                <NavLink 
                  to="/color" 
                  activeStyle={{ color: 'black' }}
                >
                    Color
                </NavLink>
                <NavBtn>
                    <NavBtnLink to="/config">Config</NavBtnLink>
                </NavBtn>
            </NavMenu>
           </Nav> 
        </>
    );
};
export default Navbar;

