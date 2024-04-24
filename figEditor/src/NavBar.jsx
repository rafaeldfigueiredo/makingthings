import React from "react";

export default function NavBar() {
  const navElements = ["Home"];
  return (
    <nav>
      <ul id="navList">
        {navElements.map((navEl, index) => {
          return (
            <li className="navElement" key={index}>
              {navEl}
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
