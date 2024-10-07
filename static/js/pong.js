kaplay({
    background: [255, 255, 128],
    height:650,
    width:1000,
});

// add paddles
add([
    pos(40, 0),
    rect(20, 80),
    outline(4),
    anchor("center"),
    area(),
    "paddle",
]);

add([
    pos(width() - 40, 0),
    rect(20, 80),
    outline(4),
    anchor("center"),
    area(),
    "paddle",
]);

// move paddles with mouse
onUpdate("paddle", (p) => {
    p.pos.y = mousePos().y;
});

// score counter
let score = 0;

add([
    text(score),
    color([0,0,0]),
    pos(center()),
    anchor("center"),
    z(50),
    {
        update() {
            this.text = score;
        },
    },
]);

// ball
let speed = 500;

const ball = add([
    pos(center()),
    circle(16),
    outline(4),
    area({ shape: new Rect(vec2(-16), 32, 32) }),
    { vel: Vec2.fromAngle(rand(-20, 20)) },
]);

// move ball, bounce it when touche horizontal edges, respawn when touch vertical edges
ball.onUpdate(() => {
    ball.move(ball.vel.scale(speed));
    if (ball.pos.x < 0 || ball.pos.x > width()) {
        score = 0;
        ball.pos = center();
        ball.vel = Vec2.fromAngle(rand(-20, 20));
        speed = 500;


        
        // Example usage: Calling the function to display a question
        displayQuestion(
          "What is the capital of France?", 
          ["Berlin", "Madrid", "Paris", "Rome"], 
          2 // Index of the correct answer (Paris)
       
        );

         ball.paused = true;
        
    }
    if (ball.pos.y < 0 || ball.pos.y > height()) {
        ball.vel.y = -ball.vel.y;
        speed += 10;
    }
});

// bounce when touch paddle
ball.onCollide("paddle", (p) => {
    speed += 80;
    ball.vel = Vec2.fromAngle(ball.pos.angle(p.pos));
    score++;
    speed += 10;
});


// const modal = document.getElementById("myModal");
// const btn = document.getElementById("openModal");
// const span = document.getElementsByClassName("close")[0];
// const submitBtn = document.getElementById("submitAnswer");

// // btn.onclick = function() {
// //   modal.style.display = "block";
// // }


// function displayQuestion(){
//       modal.style.display = "block";

// }

// span.onclick = function() {
//   modal.style.display = "none";
// }

// window.onclick = function(event) {
//   if (event.target == modal) {
//     modal.style.display = "none";
//     ball.cancel();
//   }
// }

// submitBtn.onclick = function() {
//   const selectedAnswer = document.querySelector('input[name="answer"]:checked');
//   if (selectedAnswer) {
//     const answerValue = selectedAnswer.id;
//     if (answerValue === "a") {
//       alert("Correct!");
//     } else {
//       alert("Incorrect!");
//     }
//     modal.style.display = "none";
//   } else {
//     alert("Please select an answer!");
//   }
// }




// Store references to dynamically added elements
let elements = [];

// Function to display a question
function displayQuestion(questionText, options, correctAnswerIndex) {
  // Clear previous question elements from the screen
  elements.forEach((element) => destroy(element));
  elements = [];

  // Display the question text
  const question = add([
    text(questionText, { size: 32 }),
    pos(100, 100),
      color([0,0,0]),
      "question"
  ]);
  elements.push(question);

  // Function to add options as clickable text
  function addOption(optionText, index, yPos) {
    const option = add([
      text(optionText, { size: 24 }),
      pos(100, yPos),
      area(),
           color([0,0,0]),
      "option",
    ]);

    elements.push(option); // Track option for clearing later

    option.onClick(() => {
      // Clear any previous feedback
      elements.forEach((el) => {
        if (el.is("feedback")) destroy(el);
      });

      // Show feedback
      if (index === correctAnswerIndex) {
        const feedback = add([
          text("Correct!"), // Green text
            color([0,255,0]),
            pos(center()),
          "feedback",
        ]);
          // make a correct get request
          
          // fetch("https://jsonplaceholder.typicode.com/posts/1")
          //   .then((response) => response.json())
          //   .then((json) => console.log(json));
          
        elements.push(feedback);
      } else {
        const feedback = add([
          text("Wrong!"), // Red text
            color([255,0,0]),
          pos(center()),
          "feedback",
        ]);

            // make a wrong get request

            // fetch("https://jsonplaceholder.typicode.com/posts/1")
            //   .then((response) => response.json())
            //   .then((json) => console.log(json));
          
        elements.push(feedback);
      }

        wait(3, () => {
            destroyAll("option")
             destroyAll("feedback")
             destroyAll("question")
             ball.paused = false;
        });
    });
  }

  // Add the options to the screen
  let yPosition = 200;
  options.forEach((optionText, index) => {
    addOption(optionText, index, yPosition);
    yPosition += 50; // Move each option down a bit
  });
}

