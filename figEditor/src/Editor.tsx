import React from "react";

interface EditorProps {
  text: string;
  onTextChange: (newText: string) => void;
  onClear: () => void;
  onFocusChange?: (isFocused: boolean) => void;
  placeholder?: string;
  rows: number;
}

const Editor: React.FC<EditorProps> = ({ text, onTextChange, onClear, rows, placeholder, onFocusChange }) => {

  function handleTextAreaChange(event: React.ChangeEvent<HTMLTextAreaElement>) {
    onTextChange(event.target.value)
  }

  function handleFocus(event: React.FocusEvent<HTMLTextAreaElement>) {
    console.log(event.type);
    onFocusChange?.(true);
  }

  function applyFormat(format: 'bold' | 'italic' | 'underline') {
    const selectionStart = (event?.target as HTMLTextAreaElement)?.selectionStart
    const selectionEnd = (event?.target as HTMLTextAreaElement)?.selectionEnd

    if (selectionStart != null && selectionEnd !== null) {
      const selectedText = text.substring(selectionStart, selectionEnd)
      let newText = ''
      let tag = ''

      switch (format) {
        case 'bold':
          tag = 'b'
          break
        case 'italic':
          tag = 'i'
          break
        case 'underline':
          tag = 'u'
          break
        default:
          return
      }
      const formattedText = `<${tag}>${selectedText}</${tag}>`
      newText = text.substring(0, selectionStart) + formattedText + text.substring(selectionEnd)
      onTextChange(newText)
    }
  }


  return (
    <div className="editor-container">
      <div className="editor-toolbar">
        <button onClick={() => { applyFormat('bold') }}><b>B</b></button>
        <button onClick={() => { applyFormat('italic') }}><i>I</i></button>
        <button onClick={() => { applyFormat('underline') }}><u>U</u></button>
      </div>
      <textarea
        onFocus={handleFocus}
        placeholder={placeholder}
        onChange={handleTextAreaChange}
        value={text}
        rows={rows}
        className="editor-input" />
      <button onClick={onClear}>Clear</button>
    </div>
  )

}

export default Editor;