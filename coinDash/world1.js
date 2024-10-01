function makeWorld1() {
  walls = new Group();
  walls.w = 32;
  walls.color = "blue";
  walls.h = 32;
  walls.tile = "=";
  walls.collider = "static";
  walls.pixelPerfect = true;
  floors = new Group();
  floors.w = 32;
  floors.color = "blue";
  floors.h = 32;
  floors.tile = "-";
  floors.collider = "static";

  new Tiles(
    [
      "=======-...-=======",
      "=.................=",
      "=.................=",
      "=.................=",
      "=...-----------...=",
      "=.................=",
      "=.................=",
      "=.................=",
      "=------.....-------",
      "=.................=",
      "=.................=",
      "=.................=",
      "=...-----------...=",
      "=.................=",
      "=.................=",
      "=.................=",
      "=-------...-------=",
    ],
    64,
    40,
    walls.w,
    walls.h
  );
}
