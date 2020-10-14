let song, analyzer;
let asian = [];
let white = [];
let other = [];
var video;
var button;
var snapshots = [];
var dur;

function preload() {
  //asian
  puppet = loadSound('static/Sound/Asian/Puppet.mp3');
  assembly_line = loadSound("static/Sound/Asian/Assembly_Line.mp3");
  iphones = loadSound("static/Sound/Asian/Iphones.mp3");

  //black
  black = loadSound("static/Sound/Black/black.mp3");

  //hispanic
  hispanic = loadSound("static/Sound/Hispanic/hispanic.mp3");

  //other
  no_idea = loadSound("static/Sound/Other/No_idea.mp3");
  what = loadSound("static/Sound/Other/What.mp3");

  //white
  meth = loadSound("static/Sound/White/white_meth.mp3");
  south = loadSound("static/Sound/White/white_south.mp3");

  asian = [puppet, assembly_line, iphones];
  white = [meth, south];
  other = [no_idea, what];

  elmo1 = loadImage("static/elmo_face/elmo.png");
  elmo2 = loadImage("static/elmo_face/elmo2.png");
}

function setup() {
  createCanvas(1250, 620);
  video = createCapture(VIDEO);
  video.size(320, 240);
  button = createButton('snap');
  button.position(0,250);
  image(elmo2,400,155);
  // create a new Amplitude analyzer
  analyzer = new p5.Amplitude();
  // Patch the input to an volume analyzer
  analyzer.setInput(song);
}

function draw() {
  background(0);
  button.mousePressed(function playaudio() {
  button.hide();

  snapshots.push(video.get());
  video.loadPixels();
  var data_uri = video.canvas.toDataURL();
  video.hide();
  document.getElementById("base64").src = data_uri
  document.getElementById('race').innerHTML = "<p>Loading...</p>";
  

  $.ajax({
    url : "/photocap",
    data : {"photo": data_uri},
    success : function(response){
        console.log(response);

        document.getElementById('race').innerHTML = "<p>Asian: "+response.race.asian+"<br>Black: "+response.race.black+"<br>Hispanic: "+response['race']['latino hispanic']+"<br>White: "+response.race.white+"<br>Indian: "+response.race.indian+"<br>Middle eastern: "+response['race']['middle eastern']+"<br><br>Race: "+response.dominant_race+"</p>";

        if (response.dominant_race == "asian"){
          song = asian[Math.floor(Math.random() * asian.length)];
        } else if (response.dominant_race == "black"){
          song = black;
        } else if (response.dominant_race == "latino hispanic"){
          song = hispanic;
        } else if (response.dominant_race == "white"){
          song = white[Math.floor(Math.random() * white.length)];
        } else if (response.dominant_race == "?"){
          song = other[Math.floor(Math.random() * other.length)];
        } 

        song.play();
        var dur = song.duration();

        setTimeout(function pausing(){
          button.show();
          document.getElementById('race').innerHTML = "<p></p>";
          video.show();
        },dur*1000)
        
      }
    })
  })

  // Get the average (root mean square) amplitude
  let rms = analyzer.getLevel();

  if (rms > 0.02){
    elmo = elmo1
  } else{
    elmo = elmo2
  };
  image(elmo,400,155);
}
function touchStarted() {
  getAudioContext().resume()
}
