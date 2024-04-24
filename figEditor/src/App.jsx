import React, { Fragment } from "react";
import "./App.css";
import ThingsToDo from "./ThingsToDo";
import TextEditor from "./TextEditor";
import Title from "./Title";

export default function App() {
  return (
    <Fragment>
      <Title />
      <TextEditor />
      <ThingsToDo />
    </Fragment>
  );
}
