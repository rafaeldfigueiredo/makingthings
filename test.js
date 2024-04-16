async function fetchPoke(pokemon=1) {
  const response = await fetch(`https://pokeapi.co/api/v2/pokemon/${pokemon}`);
  const data = await response.json()
  return data
}

async function renderPoke(data){
  clearList()
  let pokeName = document.createTextNode(data.name);
  const image = document.createElement('img');
  let pokesubtitle = document.createElement('figcaption')
  pokesubtitle.setAttribute('id','name');

  image.src = data.sprites.front_default;
  pokesubtitle.appendChild(pokeName);
  list.appendChild(image);
  list.appendChild(pokesubtitle);
} 

async function getPoke(){ // main safe func
  clearList()
  let value = document.querySelector("#input").value //gets input value
  let data = await fetchPoke(value); // Being numeric, fetchPoke get from db
  renderPoke(data)
}
 
async function keepDis() {
  clearList()
  for (let value = 1; value <= 100; value++) {
    const data = await fetchPoke(value);
    renderPoke(data);
    await new Promise((resolve) => setTimeout(resolve, 1000)); // Wait 1 second
  }
  console.log("All Pokemons displayed!");
}

async function getPokeRand(){ // Get random one
  clearList()
  renderPoke(await fetchPoke(Math.floor(Math.random() * 1000)))
}

function clearList(){
  let x = document.querySelectorAll('img')
  let y = document.querySelectorAll('figcaption')
  for (let i = 0; i < x.length; i++) {
    x[i].remove()
    y[i].remove()
  }
}