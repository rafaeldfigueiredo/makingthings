import React, { Fragment, useState } from "react";

export default function ThingsToDo() {
  let [isOn, setOn] = useState(false);
  return (
    <Fragment>
      <button style={{ height: "auto" }} onClick={() => setOn(!isOn)}>
        Things to Do
      </button>
      {!isOn ? 
      <h4 style={{ marginLeft: "15px" }}>Stories is off</h4> :
      <aside id="todo" style={{ display: "flex" }}>
      <h2>Core Functionality:</h2>
      <ul>
        <li>
          <del>Editing Area: A large, central section for typing and formatting text.</del>
        </li>
        <li>
          Formatting Toolbar: Buttons or icons for applying styles (
            <del>bold</del>,
            <del>italics</del>,
            <del>underline</del>,
            headings,
            bullets).
        </li>
      </ul>
      <h2>Additional Features (Consider):</h2>
      <ul>
        <li>
          Text Formatting Options:
          <ul>
            <li>Font selection</li> <li>Text color options</li>
            <li>Text alignment (left, center, right)</li>
          </ul>
        </li>
        <li>
          Paragraph Formatting:
          <ul>
            <li>Line spacing options</li> <li>Indentation controls</li>
          </ul>
        </li>
        <li>
          Content Management:
          <ul>
            <li>Inserting images and videos</li>
            <li>Link creation and editing</li>
          </ul>
        </li>
        <li>Undo/Redo Functionality</li>
        <li>Live Preview: Reflect changes as users format text</li>
      </ul>
      <h3>Layout:</h3>
      <ul>
        <li>
          Top Bar:
          <ul>
            <li>Save, export, or create new documents</li>
            <li>(Optional) User account information</li>
          </ul>
        </li>
        <li>
          Bottom Bar:
          <ul>
            <li>Character count or word count display</li>
            <li>(Optional) Fullscreen mode or table creation</li>
          </ul>
        </li>
      </ul>
      <h3>Bonus points:</h3>
      <ul>
        <li>Markdown Support</li>
        <li>Collaboration Features: Real-time editing with other users</li>
        <li>Version Control: Track changes made to the document</li>
      </ul>
    </aside>}
    </Fragment>

  );
}
