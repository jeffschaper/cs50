//This should change the text when the page is loaded
window.onload = getText();

//Calls API using async/await
//Async - Function always returns a promise 
async function getText(){
    
    let passageParam = randomPassage();

    let params = '&include-passage-references=false&include-verse-numbers=false';

    //API credit
    let Url = 'https://api.esv.org/v3/passage/text?q=' + passageParam + params;
    console.log(Url);
    //Await - Used with Async
    //Suspend function exeeuction until the Async promise settles and returns its result
    let response = await fetch(Url, {
        method: 'GET',
        headers: {
            'Authorization': '975a7fa1cb2ea9fa98d0c12b4f229860c58abf61'
         }
    });

    if(response.ok){ // if HTTP-status is 200-299
        // get the response body
        let passage = await response.json();
        
        populateUI(passageParam, passage.passages[0]);
        //console.log(passage);
     } else{
        alert("HTTP-Error: " + response.status);
     }

     //Function to input json response to HTML
     function populateUI(ref, verse){
        //strip verse
        document.getElementById('reference').innerHTML = ref;
        document.getElementById('verse').innerHTML = verse;
    }

}

//Get a random passage from Proverbs
//API needs to pass a passage with chapter and verse
//Is there a way to dynamically get books, chapters and verses?
function randomPassage(){
    //Chapter lengths of each chapter in Proverbs
    const chapterLengths = [
        33, 22, 35, 27, 23, 35, 27, 36, 18, 32,
        31, 28, 25, 35, 33, 33, 28, 24, 29, 30,
        31, 29, 35, 34, 28, 28, 27, 28, 27, 33,
        31
    ];
    
    let min = 0;
    //Get max number of chapters
    let max = (chapterLengths.length);
    //Get random chapter
    let chapter = Math.floor(Math.random() * max);
    //console.log(chapter);
    //Get random verse
    let verse = Math.floor(Math.random() * chapterLengths[chapter]);
    //console.log(verse);
    return `Proverbs ${chapter}:${verse}`;
}
