/* eslint-disable react/prop-types */
import React from "react";

export default function BoldButton({ textarea }) {
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
