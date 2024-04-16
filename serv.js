const list = document.querySelector('#list')

/**
 * Interact with PókeAPI to get pokemons data
 * @param pokemon - ID of the Pokemon. Default is 1(Bulbasaur)
 * @returns data - A JSON file containing Pokemon characteristics
 */
async function fetchPoke(pokemon=1) {
  const response = await fetch(`https://pokeapi.co/api/v2/pokemon/${pokemon}`);
  const data = await response.json()
  return data
}

/**
 * Render a Pokemon image and name based on fetchPoke return of data.
 * @param data - The data received from fetchPoke() querying PókeAPI. 
 */
async function renderPoke(data){
  // Create the Pokemon display elements
  let pokeContainer = document.createElement('figure');
  let image = document.createElement('img');
  let pokesubtitle = document.createElement('figcaption')
  var pokeName = document.createTextNode(data.name);

  //Assign each element their respectives displays
  pokesubtitle.setAttribute('class','name'); // for CSS
  image.src = data['sprites']['front_default'];
  pokesubtitle.appendChild(pokeName);
  //Insert image and captions to figure tag and, then, the latter to #list
  pokeContainer.appendChild(image);
  pokeContainer.appendChild(pokesubtitle);
  list.appendChild(pokeContainer);
  return console.log(`Renderizing ${data.name}`);
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
  let x = document.querySelectorAll('figure')
  for (let i = 0; i < x.length; i++) {
    x[i].remove()
  }
}