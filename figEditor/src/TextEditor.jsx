import React, { Fragment } from "react";
import FormatBar from "./FormatBar";

function NavBar() {
  const navElements = ["Home", "Text Editor", "About"];
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

export default function TextEditor() {
  return (
    <Fragment>
      <header>
        <NavBar />
      </header>
      <main>
        <FormatBar />
        <textarea style={{ resize: "none" }} defaultValue={'LOREM IPSUM'} id="textEditor"/>
      </main>
    </Fragment>
  );
}
