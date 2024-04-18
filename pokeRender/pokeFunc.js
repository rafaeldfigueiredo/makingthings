const list = document.querySelector("#list");
var stopIt = false;
/**
 * Interact with PókeAPI to get pokemons data
 * @param pokemon - ID of the Pokemon. Default is 1(Bulbasaur)
 * @returns data - A JSON file containing Pokemon characteristics
 */
async function fetchPoke(pokemon = 1) {
  const response = await fetch(`https://pokeapi.co/api/v2/pokemon/${pokemon}`).catch(err => console.log(err));
  const data = await response.json();
  return data;
}

/**
 * Render a Pokemon image and name based on fetchPoke return of data.
 * @param data - The data received from fetchPoke() querying PókeAPI.
 */
async function renderPoke(data) {
  // Create the Pokemon display elements. In hierachic order: Figure > Img(imgUrl) - Figcaption
  let pokeContainer = document.createElement("figure");
  let pokeImage = document.createElement("img");
  let pokesubtitle = document.createElement("figcaption");
  var pokeName = document.createTextNode(capit(data.name));

  //Assign each element their respectives displays and classes
  pokesubtitle.setAttribute("class", "name"); // for CSS
  pokeImage.setAttribute("class", "pokeImage"); // for CSS
  pokeImage.src = data["sprites"]["front_default"];
  pokesubtitle.appendChild(pokeName);
  //Insert image and captions to figure tag and, then, the latter to #list
  pokeContainer.appendChild(pokeImage);
  pokeContainer.appendChild(pokesubtitle);
  list.appendChild(pokeContainer);
  return console.log(`Renderizing ${data.name}`);
}

async function getPoke() {
  // main safe func
  clearList();
  let value = document.querySelector("#input").value; //gets input value
  let data = await fetchPoke(value); // Being numeric, fetchPoke get from db
  renderPoke(data);
}

async function keepDis() {
  clearList();
  stopIt = false;
  while (stopIt == false) {
    for (let value = 1; value <= 100; value++) {
      if (stopIt == true) {break}
      const data = await fetchPoke(value);
      renderPoke(data);
      await new Promise((resolve) => setTimeout(resolve, 1000)); // Wait 1 second
    }
  }
  console.log("All Pokemons displayed!");
}

async function getPokeRand() {
  // Get random one
  clearList();
  renderPoke(await fetchPoke(Math.floor(Math.random() * 1000)));
}

function clearList() {
  stopIt = true;
  list.innerHTML = ''
}
/**
 * Just capitalizing first letter.
 */
function capit(text) {
  return text[0].toUpperCase() + text.slice(1);
}
/**
 * This class is meant to encapsulate the same logic of keepDisplaying() but
 * with defined initial/end values based on the NationalDex ID of each
 * region.
 */
class PokemonRegion {
  /**
   *
   * @param {String} regionName - The Pokemon official region' name.
   * @param {Number} startId - The first NationalDex entry of the respective region
   * @param {Number} endId - The first NationalDex entry of the respective region
   */
  constructor(regionName, startId, endId, fetchPoke, renderPoke,clearList) {
    this.startId = startId;
    this.endId = endId;
    this.regionName = regionName;
    this.fetchPoke = fetchPoke;
    this.renderPoke = renderPoke;
    this.clearList = clearList;
  }

  async getRegPokes() {
    clearList()
    stopIt = false;
    console.log(`Now rendering:${this.regionName}`);
    while (stopIt == false) {
      for (let value = this.startId; value <= this.endId; value++) {
        if (stopIt == true){break}
        const data = await this.fetchPoke(value);        
        this.renderPoke(data);
      }
    }
  }
}

function getKantoPoke() {
  let kanto = new PokemonRegion("Kanto", 1, 151, fetchPoke, renderPoke,clearList);
  kanto.getRegPokes();
}

function getJohtoPoke() {
  let johto = new PokemonRegion("Johto", 152, 251, fetchPoke, renderPoke,clearList);
  johto.getRegPokes();
}

function getHoennPoke() {
  let hoenn = new PokemonRegion("Hoenn", 252, 386, fetchPoke, renderPoke,clearList);
  hoenn.getRegPokes();
}