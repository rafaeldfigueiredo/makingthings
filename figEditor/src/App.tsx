import { useState, useEffect } from 'react';
import Editor from './Editor';
import './App.css';
import Header from './Header';
import useDebounce from './hooks/Debounce';

const LOCAL_STORAGE_KEY: string = 'react-editor-text';
const SAVE_DELAY: number = 1000;

function App() {
  const [text, setText] = useState<string>(() => {
    const savedText = localStorage.getItem(LOCAL_STORAGE_KEY);
    return savedText !== null ? savedText : '';
  });

  const debouncedText = useDebounce<string>(text, SAVE_DELAY)

  useEffect(() => {
    try {
      localStorage.setItem(LOCAL_STORAGE_KEY, debouncedText);
      console.log(`Saved! Current text:${debouncedText}`);
    } catch (error) {
      console.error("Failed to save to localStorage:", error);
    }
  }, [debouncedText]);

  const handleTextChange = (newText: string) => {
    setText(newText);
  };


  const handleClearChange = () => {
    localStorage.removeItem(LOCAL_STORAGE_KEY);
    setText('');
    console.log('Text Cleared.');
  };

  const handleFocusChange = (isFocused: boolean) => {
    console.log(`Editor Focus Changed: ${isFocused}`);

  }

  return (
    <div className="App">
      <Header />
      <Editor
        text={text}
        onFocusChange={handleFocusChange}
        onTextChange={handleTextChange}
        onClear={handleClearChange}
        placeholder="Enter your text here:"
        rows={10}
      />

      <div className="char-counter">
        Character Count: {text.length}
      </div>

      <div className='char-counter'>
        <h2>Current State (in App):</h2>
        <div dangerouslySetInnerHTML={{ __html: text }} />
      </div>
    </div>
  );
}

export default App;