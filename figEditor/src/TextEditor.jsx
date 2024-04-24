import React from "react";
import FormatBar from "./FormattingBar/FormatBar";
import NavBar  from "./NavBar";
import TextArea  from "./TextArea";

export default function TextEditor() {
  return (
    <>
      <header>
        <NavBar />
      </header>
      <main>
        <FormatBar />
        <TextArea/>
      </main>
    </>
  );
}
