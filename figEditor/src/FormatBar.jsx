// @ts-ignore
import React, { useRef } from "react";

function BoldButton() {
  const boldIt = () => {
      
    }
    
    return (
      <button className="formatButton" onClick={boldIt}>
        <b>B</b>
      </button>
    );
  }

function ItalicButton() {
  return (
    <button className="formatButton">
      <i>I</i>
    </button>
  );
}

function UnderlineButton() {
  return (
    <button className="formatButton">
      <u>U</u>
    </button>
  );
}

export default function FormatBar() {
  function NewFunction() {    
    const textarea = document.querySelector('#textEditor')
    
    textarea.style.fontWeight != "900" ? 
    textarea.style.fontWeight = "900" : 
    textarea.style.fontWeight = '300'
    }
  return (
    <div id="formatting-bar">
      <button onClick={NewFunction}>aaaaaaaaaa</button>
      <BoldButton  />
      <ItalicButton  />
      <UnderlineButton  />
    </div>
  );

  
}
