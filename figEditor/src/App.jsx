import React, { Fragment } from "react";
import "./App.css";
import ThingsToDo from "./ThingsToDo";
import TextEditor from "./TextEditor";

function App() {
  return (
    <Fragment>
      <TextEditor />
      <ThingsToDo />
    </Fragment>
  );
}

export default App;
