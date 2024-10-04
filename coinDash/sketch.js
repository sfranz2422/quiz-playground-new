let player,
  hero,
  coin,
  coinLocations,
  enemy,
  groundSensor,
  topDetect,
  bottomDetect,
  topRightDetect,
  topLeftDetect,
  bottomRightDetect,
  bottomLeftDetect;
let highScore = 0;
let score = 0;
let rnum1 = 0;
let rnum2 = 0;
let rnum3 = 0;
let enemyVelocity = 3;
let toggle = true;
let scene = 1;
let timer = 0;
let cnv;

function preload() {
  soundFormats("mp3");
  coinSound = loadSound("coin");
  jumpSound = loadSound("jump");
  deadSound = loadSound("dead");
  coinsImg = loadImage("coin2.png");
  hero = new Sprite();
  hero.x = 361;
  hero.y = 382;
  hero.width = 20;
  hero.height = 20;
  hero.spriteSheet = "player2-1.png";
  hero.anis.offset.x = 0;
  hero.anis.frameDelay = 8;
  hero.addAnis({
    stand: { row: 0, frames: 0 },
    right: { row: 0, frames: [1, 2] },
    left: { row: 0, frames: [3, 4] },
  });
  hero.changeAni("stand");
  hero.visible = false;
}
function setup() {
  let canvasWidth = 700;
  let canvasHeight = 600;
  cnv = createCanvas(canvasWidth, canvasHeight);
  background(220);


  let newCanvasX = (windowWidth/2)-(canvasWidth/2);
  let newCanvasY = windowHeight/2-(canvasHeight/2);


  cnv.position(newCanvasX, newCanvasY)




}

function draw() {
  background(220);

  if (scene == 1) {
    textSize(28);
    textAlign(CENTER, CENTER);
    text("COIN DASH", 350, height / 2);
    fill("black");
    text("Space to Begin", width / 2, height / 2 + 50);

    if (keyboard.presses("space")) {
      allSprites.pixelPerfect = true;
      coinLocations = [
        [125, 264],
        [592, 255],
        [126, 523],
        [583, 504],
      ];

      // mouseCoordinates();
      world.gravity.y = 20;
      makeWorld1();
      setupPlayer();
      makeCoin();
      setupEnemy();
      setupBoard();
      hero.visible = true;
      scene = 2;
    }
  }

  if (scene == 2) {
    // displayCoordinates();
    movePlayer();
    pickUpCoin();
    displayScore();
    enemyMovement();
    playerEnemyCollision();
  }

  if (scene == 3) {
    textSize(28);
    textAlign(CENTER, CENTER);
    if (myTimer() <= 0) {
      text("TIMES UP!", width / 2, height / 2 - 50);
    }
    text("GAME OVER", width / 2, height / 2);
    textSize(28);
    text("High Score " + highScore, width / 2, height / 2 + 50);
    fill("black");
    text("Space to Begin", width / 2, height / 2 + 90);

    if (keyboard.presses("space")) {
      floors.visible = true;
      coin.visible = true;
      enemy.visible = true;
      walls.visible = true;
      hero.visible = true;
      enemy.x = 350;
      enemy.y = 10;
      hero.x = 361;
      hero.y = 382;
      score = 0;
      rnum1 = 0;
      rnum2 = 0;
      rnum3 = 0;
      enemyVelocity = 3;
      hero.layer = 200;
      world.autoStep = true;
      timer = 0;
      scene = 2;
    }
  }
}
function setupPlayer() {
  hero.collider = "none";
  hero.bounciness = 0;
  hero.rotationLock = true;
  hero.width = 40;
  hero.height = 40;
  hero.scale = 2.5;
  // hero.debug = true
  hero.removeColliders();
  hero.addCollider(0, 0, 50, 50);
  hero.friction = 0;
  // This groundSensor sprite is used to check if the player
  // is close enough to the ground to jump. But why not use
  // `player.colliding(grass)`? Because then the player could
  // jump if they were touching the side of a wall!
  // Also the player's collider bounces a bit when it hits
  // the ground, even if its bounciness is set to 0. When
  // making a platformer game, you want the player to
  // be able to jump right after they land.
  // This approach was inspired by this tutorial:
  // https://www.iforce2d.net/b2dtut/jumpability
  groundSensor = new Sprite(hero.x, hero.y + 20, 6, 35, "n");
  groundSensor.visible = false;
  groundSensor.mass = 0.0;
  new GlueJoint(hero, groundSensor);
}
function setupEnemy() {
  enemyVelocity += 0.4;
  rnum1 = Math.floor(Math.random() * 10);
  rnum2 = Math.floor(Math.random() * 10);
  enemy = new Sprite();
  enemy.img = "tile_0012.png";
  enemy.x = 350;
  enemy.y = 10;
  enemy.collider = "dynamic";
  enemy.friction = 0;
  enemy.rotationLock = true;
  enemy.width = 60;
  enemy.height = 60;
  enemy.scale = 3.0;
  // enemy.debug = true
  enemy.pixelPerfect = true;
  enemy.removeColliders();
  enemy.addCollider(0, 0, 50, 50);
  enemy.mass = 7;
  enemyBottomSensor = new Sprite(enemy.x, enemy.y + 20, 6, 40, "n");
  enemyBottomSensor.visible = false;
  enemyBottomSensor.mass = 0.0;
  new GlueJoint(enemy, enemyBottomSensor);
  leftSensor = new Sprite(enemy.x - 20, enemy.y, 55, 6, "n");
  leftSensor.visible = false;
  leftSensor.mass = 0.01;
  new GlueJoint(enemy, leftSensor);
  rightSensor = new Sprite(enemy.x + 20, enemy.y, 55, 6, "n");
  rightSensor.visible = false;
  rightSensor.mass = 0.01;
  new GlueJoint(enemy, rightSensor);
}
function movePlayer() {
  // console.log(`${hero.x}, ${hero.y}`);
  // console.log(hero.visible);
  if (groundSensor.overlapping(floors)) {
    if (kb.pressing("up") || kb.pressing("space")) {
      hero.vel.y = -10.5;
      jumpSound.play();
    }
  }
  if (kb.pressing("right")) {
    hero.vel.x = 5.5;
    hero.changeAni("right");
  } else if (kb.pressing("left")) {
    hero.vel.x = -5.5;
    hero.changeAni("left");
  } else {
    hero.vel.x = 0;
    hero.changeAni("stand");
  }
  if (hero.y < 35) {
    hero.y = 35;
  }
  if (hero.y > 550) {
    deadSound.play();
    gameOver();
  }
}

function makeCoin() {
  const randomLocation =
    coinLocations[Math.floor(Math.random() * coinLocations.length)];
  coin = new Sprite();
  coin.spriteSheet = coinsImg;
  coin.addAni({ w: 16, h: 16, row: 0, frames: 14 });
  coin.scale = 3;
  coin.x = randomLocation[0];
  coin.y = randomLocation[1];
}
function pickUpCoin() {
  if (hero.collides(coin)) {
    coin.remove();
    score += 1;
    makeCoin();
    coinSound.play();
  }
  if (enemy.collides(coin)) {
    coin.remove();

    makeCoin();
  }
}
function displayScore() {
  textSize(18);
  text("Score: " + score, 82, 17);
  text("Time Remaining: " + myTimer(), 552, 17);
  if (myTimer() <= 0) {
    deadSound.play();
    gameOver();
  }
}
function gameOver() {
  // console.log("game over");
  highScore = updateHighscore(score);
  world.autoStep = false;
  // allSprites.remove();
  floors.visible = false;
  coin.visible = false;
  enemy.visible = false;
  hero.visible = false;
  walls.visible = false;
  scene = 3;
}

function setupBoard() {
  //          	( x,  y,  w,  h, collider)
  topDetect = new Sprite(342, 113, 400, 60, "none");
  topDetect.visible = false;
  bottomDetect = new Sprite(355, 373, 400, 60, "none");
  bottomDetect.visible = false;
  topRightDetect = new Sprite(530, 227, 200, 60, "none");
  topRightDetect.visible = false;

  topLeftDetect = new Sprite(175, 242, 200, 60, "none");
  topLeftDetect.visible = false;
  bottomRightDetect = new Sprite(520, 486, 220, 60, "none");
  bottomRightDetect.visible = false;
  bottomLeftDetect = new Sprite(180, 494, 220, 60, "none");
  bottomLeftDetect.visible = false;
}
function enemyMovement() {
  if (enemyBottomSensor.overlapping(topDetect)) {
    if (rnum1 > 5) {
      enemy.vel.x = -enemyVelocity;
    } else {
      enemy.vel.x = enemyVelocity;
    }
  }
  if (enemyBottomSensor.overlapping(topRightDetect)) {
    enemy.vel.x = -enemyVelocity;
  }
  if (enemyBottomSensor.overlapping(topLeftDetect)) {
    enemy.vel.x = enemyVelocity;
  }
  if (enemyBottomSensor.overlapping(bottomDetect)) {
    if (rnum2 > 5) {
      enemy.vel.x = enemyVelocity;
    } else {
      enemy.vel.x = -enemyVelocity;
    }
  }
  if (enemyBottomSensor.overlapping(bottomRightDetect)) {
    enemy.vel.x = -enemyVelocity;
  }
  if (enemyBottomSensor.overlapping(bottomLeftDetect)) {
    enemy.vel.x = enemyVelocity;
  }
  if (leftSensor.overlapping(floors)) {
    enemy.vel.y = 20;
  }
  if (rightSensor.overlapping(floors)) {
    enemy.vel.y = 20;
  }
  if (leftSensor.overlapping(bottomLeftDetect)) {
    enemy.vel.x = enemyVelocity;
  }
  if (rightSensor.overlapping(bottomRightDetect)) {
    enemy.vel.x = -enemyVelocity;
  }

  if (enemy.y > 550) {
    setupEnemy();
  }
}
function playerEnemyCollision() {
  if (enemy.overlapping(hero)) {
    deadSound.play();
    gameOver();
    window.location.href = "{{ url_for('videoQuestions') }}";
  }
}
function myTimer() {
  timer += 1;
  return 30 - Math.floor(timer / 60);
}
function updateHighscore(newScore) {
  // get current highscore
  const oldHighscore = parseFloat(localStorage.getItem("score"));
  if (
    oldHighscore !== oldHighscore || // if it doesn't exist yet
    oldHighscore < newScore
  ) {
    // or if it's smaller than the new score (I assume bigger means better here)
    // current highscore needs to be updated
    localStorage.setItem("score", newScore);
    return newScore;
  }
  return oldHighscore;
}
