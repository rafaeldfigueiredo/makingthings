/* eslint-disable react/prop-types */
import React from "react";

export default function ItalicButton({ textarea }) {
  const mammaMiaIt = () => {
    if (textarea) {
      // @ts-ignore
      textarea.style.fontStyle !== "italic"
        ? // @ts-ignore
        (textarea.style.fontStyle = "italic")
        : // @ts-ignore
        (textarea.style.fontStyle = "normal");
    }
  };

  return (
    <button className="formatButton" onClick={mammaMiaIt}>
      <i>I</i>
    </button>
  );
}
