/* eslint-disable react/prop-types */
import React from "react";

export default function UnderlineButton({ textarea }) {
  const undercutIt = () => {
    if (textarea) {
      // @ts-ignore
      textarea.style.textDecoration !== "underline"
        ? // @ts-ignore
          (textarea.style.textDecoration = "underline")
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
