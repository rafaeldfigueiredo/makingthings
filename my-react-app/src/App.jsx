import { useEffect, useState } from "react";

export default function App() {
  const [title, setTitle] = useState('');

  useEffect(() => {
    getData();
  }, []);

  const getData = async () => {
    const response = await fetch('https://jsonplaceholder.typicode.com/todos/1');
    const task = await response.json();
    console.log(task)
    setTitle(task.title);
  };

  return <h1>{title}</h1>;
}