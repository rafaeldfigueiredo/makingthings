/* eslint-disable react/prop-types */
// @ts-ignore
import React from "react";

function BoldButton({ textarea }) {
  const boldIt = () => {
    if (textarea) {
      // @ts-ignore
      textarea.style.fontWeight !== "900"
        ? // @ts-ignore
          (textarea.style.fontWeight = "900")
        : // @ts-ignore
          (textarea.style.fontWeight = "300");
    }
  };

  return (
    <button className="formatButton" onClick={boldIt}>
      <b>B</b>
    </button>
  );
}

function ItalicButton({ textarea }) {
  const mammaMiaIt = () => {
    if (textarea) {
      // @ts-ignore
      textarea.style.fontStyle !== "italic"
        ? // @ts-ignore
          (textarea.style.fontStyle="italic")
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

function UnderlineButton({ textarea }) {

  const undercutIt = () => {
    if (textarea) {
      // @ts-ignore
      textarea.style.textDecoration !== "underline"
        ? // @ts-ignore
          (textarea.style.textDecoration ="underline")
        : // @ts-ignore
          (textarea.style.textDecoration = "none");
    }
  };

  return (
    <button className="formatButton" onClick={undercutIt}>
      <u>U</u>
    </button>
  );
}

function AddHeader(){
  return(<button>&#x1F539;&#x1F539;&#x1F539;</button>)
}

export default function FormatBar() {
  const textarea = document.querySelector("#textEditor");

  return (
    <div id="formatting-bar">
      <BoldButton textarea={textarea} />
      <ItalicButton textarea={textarea} />
      <UnderlineButton textarea={textarea} />
      <AddHeader/>
    </div>
  );
}
