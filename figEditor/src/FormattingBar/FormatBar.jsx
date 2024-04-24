/* eslint-disable react/prop-types */
// @ts-ignore
import React from "react";
import AddHeader from "./AddHeader";
import UnderlineButton from "./UnderlineButton";
import ItalicButton from "./ItalicButton";
import BoldButton from "./BoldButton";

export default function FormatBar() {
  const textarea = document.querySelector("#textEditor");

  return (
    <div id="formatting-bar">
      <BoldButton textarea={textarea} />
      <ItalicButton textarea={textarea} />
      <UnderlineButton textarea={textarea} />
      <AddHeader />
    </div>
  );
}
